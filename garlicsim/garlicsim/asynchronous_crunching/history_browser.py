# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the HistoryBrowser class.

See its documentation for more info.
'''

from __future__ import with_statement

import threading

import garlicsim.general_misc.binary_search as binary_search
import garlicsim.general_misc.queue_tools as queue_tools
import garlicsim.general_misc.third_party.decorator

import garlicsim.misc
from obsolete_cruncher_error import ObsoleteCruncherError

__all__ = ["HistoryBrowser"]

@garlicsim.general_misc.third_party.decorator.decorator
def with_self(method, *args, **kwargs):
    '''Decorator for using the history browser as a context manager.'''
    self = args[0]
    with self:
        return method(*args, **kwargs)

class HistoryBrowser(garlicsim.misc.BaseHistoryBrowser):
    '''
    A device for requesting information about the history of the simulation.
    
    A HistoryBrowser is a device for requesting information about the history of
    the simulation. It is intended to be used by CruncherThread in simulations
    that are history-dependent.
    
    With a HistoryBrowser one can request states from the simulation's timeline.
    States can be requested by clock time or position in the timeline or by
    other measures; See documentation for this class's methods.
    
    Since we do not know whether the states we request have been implemented in
    the tree already, or they are still in the work_queue, it's the job of the
    HistoryBrowser to find that out. This is done transperantly for the user.
    
    When using a HistoryBroswer, the lock of the project's tree is acquired for
    reading. That acquiring action can also be invoked by using HistoryBrowser
    as a context manager.
    '''
    
    def __init__(self, cruncher):
        self.cruncher = cruncher
        self.project = cruncher.project
        self.tree = self.project.tree
        self.tree_lock = self.project.tree.lock
    
    def __enter__(self, *args, **kwargs):
        '''Acquire the lock of the project's tree for reading.'''
        self.tree_lock.acquireRead()
    
    def __exit__(self, *args, **kwargs):
        '''Release the project's tree_lock.'''
        self.tree_lock.release()
     
    @with_self
    def get_last_state(self):
        '''Get the last state in the timeline. Identical to __getitem__(-1).'''
        return self[-1]
    
    @with_self
    def __getitem__(self, index):
        '''Get a state by its position in the timeline.'''
        assert isinstance(index, int)
        if index < 0:
            return self.__get_item_negative(index)
        else: # index >= 0
            return self.__get_item_positive(index)
    
    @with_self
    def __get_item_negative(self, index):
        '''
        Get a state by its position in the timeline. Negative indices only.
        '''
        try:
            return self.__get_item_from_queue(index)
        except IndexError:
            # The requested state is in the tree
            queue_size = self.cruncher.work_queue.qsize()
            new_index = index + queue_size
            our_node = self.__get_our_node()
            path = our_node.make_containing_path()
            result_node = path.__getitem__(new_index, end=our_node)
            return result_node.state
            
    
    @with_self
    def __get_item_positive(self, index):
        '''
        Get a state by its position in the timeline. Positive indices only.
        '''
        our_node = self.__get_our_node()
        path = our_node.make_containing_path()
        try:
            result_node = path.__getitem__(index, end=our_node)
            return result_node.state
        
        except IndexError:
            path_length = path.__len__(end=our_node)
            # todo: Probably inefficient: We're plowing through the path again.
            new_index = index - path_length
            try:
                return self.__get_item_from_queue(new_index)
            except IndexError:
                queue_length = self.cruncher.work_queue.qsize()
                timeline_length = queue_length + path_length
                message = "You asked for node number " + str(index) + \
                          " while the timeline has only " + timeline_length + \
                          " states, comprised by " + path_length + \
                          " states in the tree and " + queue_length + \
                          " states in the queue."
                raise IndexError(message)
        
    @with_self
    def __get_item_from_queue(self, index):
        '''
        Obtain an item by index number from the work_queue of our cruncher.
        '''
        item = queue_tools.get_item(self.cruncher.work_queue, index)
        return item
        
    @with_self
    def get_state_by_monotonic_function(self, function, value,
                                        rounding=binary_search.CLOSEST):
        '''
        Get a state by specifying a measure function and a desired value.
        
        The function must be a monotonic rising function on the timeline.
        
        See documentation of binary_search.roundings for details about rounding
        options.
        '''
        
        assert issubclass(rounding, binary_search.Rounding)
        
        tree_result = self.__get_both_states_by_monotonic_function_from_tree \
                      (function, value)
        
        if tree_result[1] is not None:
            # Then there is no need to check the queue even.
            return binary_search.make_both_data_into_preferred_rounding\
                   (tree_result, function, value, rounding)
        
        else:
            queue_result = self.__get_state_by_monotonic_function_from_queue \
                           (function, value, rounding=binary_search.BOTH)
            none_count = list(queue_result).count(None)
            if none_count == 0:
                # The result is entirely in the queue
                return binary_search.make_both_data_into_preferred_rounding\
                       (queue_result, function, value, rounding)
            elif none_count == 1:
                # The result is either before the past edge of the queue or after its future edge.
                if queue_result[1] is None:
                    # The result is beyond the future edge of the queue.
                    return binary_search.make_both_data_into_preferred_rounding\
                           (queue_result, function, value, rounding)
                else: # queue_result[0] == None
                    # Getting tricky: The result is somewhere in the middle
                    # between the queue and the tree.
                    combined_result = [tree_result[0], queue_result[1]]
                    return binary_search.make_both_data_into_preferred_rounding\
                           (combined_result, function, value, rounding)
    
            else:
                assert none_count == 2
                # The queue is just totally empty.
                return binary_search.make_both_data_into_preferred_rounding \
                       (tree_result, function, value, rounding)
            
    @with_self   
    def __get_both_states_by_monotonic_function_from_tree(self, function, value):
        '''
        Get two states from the tree with value surrounding the desired value.

        The function must be a monotonic rising function on the timeline.
        
        This uses the binary_search.BOTH rounding. See its documentation.        
        '''
        our_node = self.__get_our_node()
        path = our_node.make_containing_path()
        new_function = lambda node: function(node.state)
        
        result_in_nodes = path.get_node_by_monotonic_function \
            (new_function, value, binary_search.BOTH, end_node=our_node)
        
        result = [(node.state if node is not None else None) \
                  for node in result_in_nodes]
        
        return result
    
    @with_self
    def __get_state_by_monotonic_function_from_queue(
        self, function, value, rounding=binary_search.CLOSEST):
        '''
        Get a state from the queue only by measure function and desired value.
        
        The function must by a monotonic rising function on the timeline.
        
        See documentation of garlicsim.general_misc.binary_search.roundings for
        details about rounding options.
        '''
        assert issubclass(rounding, binary_search.Rounding)
        queue = self.cruncher.work_queue
        queue_as_list = queue_tools.queue_as_list(queue)
        # todo: Probably inefficient, should access them one by one
        
        return binary_search.binary_search\
               (queue_as_list, function, value, rounding)
    
    @with_self
    def __len__(self):
        '''
        Get the length of the timeline in nodes.
        
        This means the sum of:
        1. The length of the work_queue of our cruncher.
        2. The length of the path in the tree which leads to our node, up to
           our node.
        '''
        queue_length = self.cruncher.work_queue.qsize()
        
        our_node = self.__get_our_node()
        our_path = our_node.make_containing_path()
        path_length = our_path.__len__(end = our_node)
        
        return queue_length + path_length
    
    @with_self
    def __get_our_node(self):
        '''Get the node that the current cruncher is assigned to work on.'''
        jobs_to_crunchers = self.project.crunching_manager.crunchers.items()
        
        nodes_that_are_us = \
            [job.node for (job, cruncher) in jobs_to_crunchers \
             if cruncher == self.cruncher]
        
        num = len(nodes_that_are_us)
        assert num <= 1
        if num == 1:
            our_node = nodes_that_are_us[0]
        else: # num == 0
            raise ObsoleteCruncherError
        return our_node
        
    