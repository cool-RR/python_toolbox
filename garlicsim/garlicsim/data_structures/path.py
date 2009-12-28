# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
A module that defines the Path class and a few related exceptions.

See its documentation for more information.
'''

import copy as copy_module # Avoiding name clash.

from node import Node
from block import Block
# We are doing `from tree import Tree` in the bottom of the file.

import garlicsim.general_misc.binary_search as binary_search

__all__ = ['Path', 'PathError', 'PathOutOfRangeError', 'EndNotReached',
           'StartNotReached']

class PathError(Exception):
    '''An exception related to the class Path.'''
    pass

class PathOutOfRangeError(PathError):
    '''
    Nodes are requested from the path which are out of its range.
    '''
    pass

class EndNotReached(PathError):
    '''
    An end node/block is specified but it turns out not to be on the path.
    '''
    pass

class StartNotReached(PathError):
    '''
    A start node/block is specified but it turns out not to be on the path.
    '''
    pass

class Path(object):
    '''
    A path symbolizes a line of nodes in a tree. A tree may be complex and
    contain many junctions, but a path is a direct line through it. Therefore,
    a path object contains information about which child to choose when going
    through a node which has multiple children.
    
    The attribute ".decisions" is a dictionary of the form {node_which_forks: 
    node_to_continue_to, ... }. It usually contains as keys only nodes that
    have more than one child.
    
    The attribute ".root" says from which node the path begins.
    #tododoc say start and end are inclusive
    '''
    def __init__(self, tree, root=None, decisions={}):

        self.tree = tree
        
        self.root = root
        '''The root node.'''
        
        self.decisions = dict(decisions)
        '''
        The decisions dict says which fork of the road the path chooses.
        It's of the form {node_which_forks: node_to_continue_to, ... }
        '''
         # todo: Use shallow copy instead of dict.__init__. Will allow
         # dictoids.

         
    def __len__(self, start=None, end=None):
        '''
        Get the length of the path in nodes.
        
        You can optionally specify star end node, in which the path ends.tododoc
        '''
        if start is None and self.root is None:
            return 0
            
        return sum(len(thing) for thing in 
                   self.iterate_blockwise(start=start, end=end))


    def __iter__(self, start=None, end=None): #todo: make sure that start==end is ok
        '''Iterate over the nodes in the path.tododoc'''
        if start is None:
            if self.root is None:
                raise StopIteration
            current = self.root
        else:
            current = start if isinstance(start, Node) else start[0]
        
        yield current
        
        while True:
            try:
                current = self.next_node(current)
                yield current
                if end is not None:
                    if current is end:
                        raise StopIteration
                    elif isinstance(end, Block) and (current in end):
                        if current.is_last_on_block():
                            raise StopIteration
            except PathOutOfRangeError:
                if end is not None:
                    raise EndNotReached
                raise StopIteration
            
            
    def iterate_blockwise(self, start=None, end=None):
        '''
        Iterate on the path, yielding blocks when possible.tododoc
        
        You are allowed to specify a node/block from which to start iterating,
        using the parameter `start`.
        '''

        if start is None:
            if self.root is None:
                raise StopIteration
            current = self.root.soft_get_block()
        else: # start is not None
            current = start
            if isinstance(start, Node) and start.block is not None:
                if start.is_first_on_block():
                    current = start.block
                else: 
                    # We are starting iteration on a node in a block. We will
                    # not yield its block at all. We'll yield all the nodes one
                    # by one until the next node/block in the tree.
                    index_of_start = start.block.index(start)
                    for current in start.block[index_of_start:-1]:
                        yield current
                        if end is not None and (current is end):
                            raise StopIteration
                    current = start.block[-1]
                
        yield current

        while True:
            try:
                current = self.next_node(current)
                if current.block is not None:
                    if end is not None:
                        if end is current.block:
                            yield current.block
                            raise StopIteration
                        elif end in current.block:
                            index_of_end = current.block
                            for thing in current.block[ 0 : (index_of_end + 1) ]:
                                yield thing
                            raise StopIteration
                    else: # end is None
                        current = current.block
                        yield current
                else: # current.block is None
                    yield current
                    if end is not None and current is end:
                        raise StopIteration
            except PathOutOfRangeError:
                if end is not None:
                    raise EndNotReached
                raise StopIteration
    
            
    def iterate_blockwise_reversed(self, end, start=None):
        '''
        Iterate backwards on the path, yielding blocks when possible.
        
        You must specify a node/block from which to start iterating, using the
        parameter `end_node`.tododoc
        '''
        if isinstance(end, Node):
            if end.block is not None:
                if end.is_last_on_block() is False:
                    index_of_end = end.block.index(end)
                    for current in end.block[index_of_end::-1]:
                        yield current
                        if start is not None and (start is current):
                            raise StopIteration
        current = end_node.soft_get_block()

        yield current

        while True:
            if isinstance(current, Node):
                parent = current.parent
            else: # isinstance(current, Block)
                parent = current[0].parent
            
            if parent is None:
                raise StopIteration
            current = parent.soft_get_block()
            yield current

            
    def __contains__(self, thing):
        '''
        Return whether the path contains the specified node/block.tododoc
        '''
        assert isinstance(thing, Node) or isinstance(thing, Block)

        for candidate in self.iterate_blockwise():
            if candidate is thing:
                return True
            elif isinstance(candidate, Block) and thing in candidate:
                return True
            
        return False


    def next_node(self, thing):
        '''
        Return the node on the path which is next after `thing`.
        
        If we've come to a fork for which we have no key in the decisions dict,
        we choose the most recent child node, and update the decisions dict to
        point to it as well.
        '''
        
        # We're dealing with the case of 1 child first, because it's the most
        # common.
        real_thing = thing if isinstance(thing, Node) else thing[-1]
        kids = real_thing.children
        if len(kids) == 1:
            return kids[0]
        
        if (thing in self.decisions) or (real_thing in self.decisions):
            return self.decisions.get(thing, None) or \
                   self.decisions.get(real_thing, None)
        
        if len(kids) > 1:
            kid = kids[-1]
            self.decisions[real_thing] = kid
            return kid

        else: # no kids
            raise PathOutOfRangeError
            

    def __getitem__(self, index, end_node=None):
        '''
        Get a node by its index number in the path.

        You can optionally specify an end node in which the path ends.
        '''
        assert isinstance(index, int)
        
        if index >= 0:
            return self.__get_item_positive(index, end_node=end_node)
        else:
            return self.__get_item_negative(index, end_node=end_node)

        
    def __get_item_negative(self, index, end_node=None):
        '''
        Get a node by its index number in the path. Negative indices only.

        You can optionally specify an end node in which the path ends.
        '''
        if end_node is None:
            end_node = self.get_last_node()
        else:
            assert isinstance(end_node, Node)
        if index == -1:
            return end_node
        
        my_index = 0
        
        if end_node.block:
            block = end_node.block
            index_of_end_node = block.index(end_node)
            
            my_index -= (index_of_end_node + 1)
            
            if my_index <= index:
                return block[index - my_index]
        
        for thing in self.iterate_blockwise_reversed(end_node=end_node):
            my_index -= len(thing)
            if my_index <= index:
                if isinstance(thing, Block):
                    return thing[ (index - my_index)]
                else:
                    assert my_index == index
                    return thing
                
        raise PathOutOfRangeError
        
    
    def __get_item_positive(self, index, end_node=None):
        '''
        Get a node by its index number in the path. Positive indices only.

        You can optionally specify an end node in which the path ends.
        '''
        my_index = -1
        answer = None
        for thing in self.iterate_blockwise():
            my_index += len(thing)
            if my_index >= index:
                if isinstance(thing, Block):
                    answer = thing[(index-my_index) - 1]
                    break 
                else:
                    assert my_index == index
                    answer = thing
                    break
        if answer:
            if (not end_node) or answer.state.clock < end_node.state.clock:
                return answer
        raise PathOutOfRangeError

    def get_last_node(self, starting_at=None):
        '''
        Get the last node in the path.
        
        Optionally, you are allowed to specify a node from which to start
        searching.
        '''
        for thing in self.iterate_blockwise(starting_at=starting_at):
            pass

        if isinstance(thing, Block):
            return thing[-1]
        else:
            return thing
    
        
    def get_node_by_clock(self, clock, rounding="closest", end_node=None):
        '''
        Get a node according to its clock.
        
        See documentation of garlicsim.general_misc.binary_search.binary_search
        for details about rounding options.
        '''
        
        my_function = lambda node: node.state.clock
        return self.get_node_by_monotonic_function(function=my_function,
                                                   value=clock,
                                                   rounding=rounding,
                                                   end_node=end_node)    
        
    
    def get_node_by_monotonic_function(self, function, value,
                                       rounding="closest", end_node=None):
        '''
        Get a node by specifying a measure function and a desired value.
        
        The function must be a monotonic rising function on the timeline.
        
        See documentation of garlicsim.general_misc.binary_search.binary_search
        for details about rounding options.
        '''
        
        assert rounding in ["high", "low", "exact", "both", "closest"]        

        if end_node is None:
            correct_both_for_end_node = lambda both: both
        else:
            def correct_both_for_end_node(both):
                new_both = list(both)
                end_clock = end_node.state.clock
                if new_both[0] and new_both[0].state.clock >= end_clock:
                    new_both[0] = end_node
                if new_both[1] and new_both[1].state.clock >= end_clock:
                    new_both[1] = None
                return tuple(new_both)
        
        low = self.root
        
        if function(low) >= value:
            both = correct_both_for_end_node((None, low))
            return binary_search.make_both_data_into_preferred_rounding \
                   (both, function, value, rounding)
        
        '''
        Now we've established that the first node in the path has a lower value
        than what we're looking for.
        '''
        
        for thing in self.iterate_blockwise():
            if isinstance(thing, Block):
                first = thing[0]
                if function(first) >= value:
                    both = correct_both_for_end_node((low, first))
                    return binary_search.make_both_data_into_preferred_rounding \
                           (both, function, value, rounding)
                    
                last = thing[-1]
                if function(last) >= value:
                    # It's in the block
                    both = binary_search.binary_search(thing, function, value,
                                                       rounding="both")
                    both = correct_both_for_end_node(both)
                    return binary_search.make_both_data_into_preferred_rounding \
                           (both, function, value, rounding)
                else:
                    low = last
                    continue
            else: # thing is a Node
                if function(thing) >= value:
                    both = correct_both_for_end_node((low, thing))
                    return binary_search.make_both_data_into_preferred_rounding \
                           (both, function, value, rounding)
                else:
                    low = thing
                    continue
        
        '''
        If the flow reached here, that means that even the last node
        in the path has lower value than the value we're looking for.
        '''
        
        both = correct_both_for_end_node((low, None))
        return binary_search.make_both_data_into_preferred_rounding \
               (both, function, value, rounding)
            
    
    def get_node_occupying_timepoint(self, timepoint):
        '''
        Get the node which "occupies" the given timepoint.
        
        A node is considered to "occupy" a timepoint if it is the
        highest-clocked node before the timepoint, AND there exists another
        node which has a clock higher than timepoint (that higher node is not
        returned, it just has to exist for the first node to qualify as
        "occupying".)
        
        If no such node exists, returns None.
        '''
        temp = self.get_node_by_clock(timepoint, rounding="both")
        if list(temp).count(None) == 0:
            return temp[0]
        else:
            return None
        

    def get_existing_time_segment(self, start_time, end_time):
        '''
        Get the existing time segment between `start_time` and `end_time`.
        
        Example: In the path the first node's clock reading is 3.2, the last is
        7.6.
        `start_time` is 2 and `end_time` is 5.
        The function will return [3.2, 5].
        '''

        clock_of_first = self.root.state.clock
        clock_of_last = self.get_last_node().state.clock
        
        if clock_of_first <= end_time and clock_of_last >= start_time:            
            return [max(clock_of_first, start_time),
                    min(clock_of_last, end_time)]
        else:
            return None
    
        
    def modify_to_include_node(self, node):
        '''
        Modifiy the path to include the specified node.
        '''
        new_path = node.make_containing_path()
        self.root = new_path.root
        self.decisions.update(new_path.decisions)
    
        
    def __repr__(self):
        '''
        Get a string representation of the path.
        
        Example output:
        <garlicsim.data_structures.path.Path of length 43 at 0x1c822d0>
        '''
        return '<%s.%s of length %s at %s>' % \
               (
                   self.__class__.__module__,
                   self.__class__.__name__,
                   len(self),
                   hex(id(self))
               )
    
    
    def copy(self):
        '''
        Make a shallow copy of the path.
        '''
        
        # Most of these things don't need duplicating, but just for
        # completeness' sake:
        tree = self.tree
        root = self.root
        decisions = self.decisions.copy()
        
        path = Path(tree=tree, root=root, decisions=decisions)
        
        return path
    
    
    __copy__ = copy
    
    
from tree import Tree