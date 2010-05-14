# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the HistoryBrowser class.

See its documentation for more info.
'''

import garlicsim.general_misc.binary_search as binary_search
import garlicsim.general_misc.queue_tools as queue_tools
import garlicsim.misc

__all__ = ["HistoryBrowser"]


get_state_clock = lambda state: state.clock


class HistoryBrowser(garlicsim.misc.BaseHistoryBrowser):
    '''
    A device for requesting information about the history of the simulation.
    
    A HistoryBrowser is a device for requesting information about the history of
    the simulation. It is intended to be used by CruncherThread in simulations
    that are history-dependent.
    
    This specific kind of history browser, defined in the synchronous_crunching
    package, is intended for synchronously-crunched simulations in which there
    are no worker processes/threads doing the crunching. Therefore, its job is
    quite simple; it recieves a path in its constructor and it handles all
    state requests from that path.
    '''
    def __init__(self, path, end_node=None):
        #todo: maybe not require path, just calculate from node?
        self.path = path
        '''
        This is the path, from which all states will be taken when requested.
        '''
        
        self.end_node = end_node
        '''
        An optional end node, in which the path ends.
        
        If not specified, it will be None, meaning that the path would go on
        until its natural end.
        
        If this option is specified, you will have to update the end_node of
        the history browser every time you use the step function. (That's
        because you've added a node to the tree, and that node should now be
        the end_node.)
        '''
     
    def get_last_state(self):
        '''Get the last state in the timeline. Identical to __getitem__(-1).'''
        return self.end_node.state if self.end_node else self[-1]
    
    def __getitem__(self, index):
        '''Get a state by its position in the timeline.'''
        assert isinstance(index, int)
        return self.path.__getitem__(index, end=self.end_node).state
    
    def get_state_by_monotonic_function(self, function, value,
                                        rounding=binary_search.CLOSEST):
        '''
        Get a state by specifying a measure function and a desired value.
        
        The function must be a monotonic rising function on the timeline.
        
        See documentation of binary_search.roundings for details about rounding
        options.
        '''
        assert issubclass(rounding, binary_search.Rounding)
        
        new_function = lambda node: function(node.state)
        result_in_nodes = self.path.get_node_by_monotonic_function \
                        (new_function, value, rounding, end_node=self.end_node)
        
        if rounding is binary_search.BOTH:
            result = [(node.state if node is not None else None) \
                      for node in result_in_nodes]
        else:
            result = result_in_nodes.state if result_in_nodes is not None \
                   else None
            
        return result
    
    def __len__(self):
        '''Get the length of the timeline in nodes.'''
        return self.path.__len__(end=self.end_node)
    