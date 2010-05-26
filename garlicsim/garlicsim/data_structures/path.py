# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
A module that defines the Path class and a few related exceptions.

See its documentation for more information.
'''

import copy as copy_module # Avoiding name clash.
import __builtin__

from garlicsim.general_misc import binary_search
from garlicsim.general_misc import misc_tools
from garlicsim.general_misc import cute_iter_tools

from garlicsim.misc import GarlicSimException

from node import Node
from block import Block
# We are doing `from tree import Tree` in the bottom of the file.


__all__ = ['Path', 'PathError', 'PathOutOfRangeError', 'EndNotReached',
           'StartNotReached']


class PathError(GarlicSimException):
    '''Path-related exception.'''

class PathLookupError(PathError, LookupError):
    '''Path-related exception.'''    
    
class PathOutOfRangeError(PathError, IndexError):
    '''Nodes are requested from the path which are out of its range.'''

class EndNotReached(PathError):
    '''
    An end node/block is specified but it turns out not to be on the path.
    '''
    # todo: consider subclass from one of the obscure exceptions like
    # LookupError

class StartNotReached(PathError):
    '''
    A start node/block is specified but it turns out not to be on the path.
    '''
    

class Path(object):
    '''
    A path represents a line of nodes in a tree.
    
    A tree may be complex and contain many junctions, but a path is a direct
    line through it. Therefore, a path object contains information about which
    child to choose when going through a node which has multiple children.
    
    Some of Path's method accept `start` and `end` parameters for specifying a
    sub-range inside the path. It should be noted that this range will include
    both endpoints.
    '''
    
    def __init__(self, tree, root=None, decisions={}):
        '''
        Construct the path.
        
        `tree` is the tree that this path is on. `root` is the node from which
        the path begins. `decisions` is a dictionary of the form
        {node_which_forks: node_to_continue_to, ... }. It usually contains as
        keys only nodes that have more than one child.
        '''

        self.tree = tree
        '''The tree that this path is on.'''
        
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
        
        You can optionally specify `start` and/or `end`, which may be either
        nodes or blocks.
        '''
        if start is None and self.root is None:
            return 0
            
        return sum(len(thing) for thing in 
                   self.iterate_blockwise(start=start, end=end))


    def __iter__(self, start=None, end=None):
        '''
        Iterate over the nodes in the path.
        
        You can optionally specify `start` and/or `end`, which may be either
        nodes or blocks.
        '''
        if start is None:
            if self.root is None:
                raise StopIteration
            current = self.root
        else:
            current = start
        
        current = current if isinstance(current, Node) else current[0]
            
        while True:
            
            yield current
            
            if end is not None:
                if current is end:
                    raise StopIteration
                elif isinstance(end, Block) and (current in end):
                    if current.is_last_on_block():
                        raise StopIteration
                        
            try:
                current = self.next_node(current)           
            except PathOutOfRangeError:
                if end is not None:
                    raise EndNotReached
                raise StopIteration

            
    def __reversed__(self):
        '''Iterate on the nodes in the path from end to start.'''
        # todo: may add start and end
        current_node = self[-1]
        while current_node is not None:
            yield current_node
            current_node = current_node.parent
            
            
    def iterate_blockwise(self, start=None, end=None):
        '''
        Iterate on the path, yielding blocks when possible.
        
        You can optionally specify `start` and/or `end`, which may be either
        nodes or blocks.
        '''

        if start is None:
            if self.root is None:
                raise StopIteration
            current = self.root
        else: # start is not None
            current = start
            if isinstance(start, Node) and start.block is not None and \
               start.is_first_on_block() is False:
                # We are starting iteration on a node in a block. (And it's not
                # the first one on the block.) We will not yield its block at
                # all. We'll yield all the nodes one by one until the next
                # node/block in the tree.
                index_of_start = start.block.index(start)
                for current in start.block[index_of_start:]:
                    yield current
                    if current is end:
                        raise StopIteration
                    
                assert current is start.block[-1]
                
                try:
                    current = self.next_node(current)
                except PathOutOfRangeError:
                    if end is not None:
                        raise EndNotReached
                    raise StopIteration
                
        while True:
            if current.block is not None:
                if end is not None:
                    if end is current.block:
                        yield current.block
                        raise StopIteration
                    elif end in current.block:
                        index_of_end = current.block.index(end)
                        for thing in current.block[ 0 : (index_of_end + 1) ]:
                            yield thing
                        raise StopIteration
                    else: # end isn't here
                        current = current.block
                        yield current    
                else: # end is None
                    current = current.block
                    yield current
            else: # current.block is None
                yield current
                if current.is_overlapping(end):
                    raise StopIteration
            try:
                current = self.next_node(current)
            except PathOutOfRangeError:
                if end is not None:
                    raise EndNotReached
                raise StopIteration
    
            
    def iterate_blockwise_reversed(self, end, start=None):
        '''
        Iterate backwards on the path, yielding blocks when possible.
        
        You must specify an `end`. You may optionally specify a `start`. Both of
        these may be either nodes or blocks.
        '''
        current = end
        if isinstance(end, Node) and end.block is not None and \
           end.is_last_on_block() is False:
            # We are starting iteration on a node in a block. (And it's not the
            # last one on the block.) We will not yield its block at all. We'll
            # yield all the nodes one by one until the previous node/block in
            # the tree.
            index_of_end = end.block.index(end)
            for current in end.block[ index_of_end : : -1 ]:
                yield current
                if current is start:
                    raise StopIteration

            assert current is end.block[0]
            
            if isinstance(current, Node):
                current = current.parent
            else: # isinstance(current, Block)
                current = current[0].parent
            if current is None:
                if start is not None:
                    raise StartNotReached
                raise StopIteration
                
        while True:
            if current.block is not None:
                if start is not None:
                    if start is current.block:
                        yield current.block
                        raise StopIteration
                    elif start in current.block:
                        index_of_start = current.block.index(start)
                        for thing in current.block[ : (index_of_start - 1) : -1 ]:
                            yield thing
                        raise StopIteration
                else: # start is None
                    current = current.block
                    yield current
            else: # current.block is None
                yield current
                if current.is_overlapping(start):
                    raise StopIteration

            if isinstance(current, Node):
                current = current.parent
            else: # isinstance(current, Block)
                current = current[0].parent
            if current is None:
                if start is not None:
                    raise StartNotReached
                raise StopIteration
            

    def __contains__(self, thing, start=None, end=None):
        '''Return whether the path contains the specified node/block.'''
        
        assert isinstance(thing, Node) or isinstance(thing, Block)

        for candidate in self.iterate_blockwise(start=start, end=end):
            if candidate is thing:
                return True
            elif isinstance(candidate, Block) and thing in candidate:
                return True
            
        return False


    def next_node(self, thing):
        '''
        Return the node on the path which is next after `thing`.
        
        If we've come to a fork for which we have no key in the decisions dict,
        we choose the first child node in the parent node's `children`, and
        update the decisions dict to point to it as well.
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
            kid = kids[0]
            # Whether it should take `kids[0]` or `kids[-1]` is a subject for
            # debate. The question is, when you update the tree, do you want the
            # old paths to point to the new nodes or the old?
            self.decisions[real_thing] = kid
            return kid

        else: # no kids
            raise PathOutOfRangeError

    

    def __getitem__(self, index, end=None):
        '''
        Get a node by its index number in the path.

        You can optionally specify an end node in which the path ends.
        '''
        #todo: allow slicing? make Path.states for this and for iterating?
        #todo: generalize `end` to blocks
        assert isinstance(index, int)
        
        
        if index >= 0:
            return self.__get_item_positive(index, end=end)
        else:
            return self.__get_item_negative(index, end=end)

        
    def __get_item_negative(self, index, end=None):
        '''
        Get a node by its index number in the path. Negative indices only.

        You can optionally specify an end node in which the path ends.
        '''
        if end is None:
            end = self.get_last_node()
        else:
            assert isinstance(end, Node) or isinstance(end, Block)
        if index == -1:
            return end
        
        my_index = -1
        
        if end.block:
            block = end.block
            index_of_end = block.index(end)
            
            my_index -= (index_of_end)
            
            if my_index <= index:
                return block[index - my_index]
            
            end = end.block[0]
        
        my_index += 1
            
        for thing in self.iterate_blockwise_reversed(end=end):
            my_index -= len(thing)
            if my_index <= index:
                if isinstance(thing, Block):
                    return thing[(index - my_index)]
                else:
                    assert my_index == index
                    return thing
                
        raise PathOutOfRangeError
        
    
    def __get_item_positive(self, index, end=None):
        '''
        Get a node by its index number in the path. Positive indices only.

        You can optionally specify an end node in which the path ends.
        '''
        # todo: supports blocks?
        my_index = -1
        answer = None
        for thing in self.iterate_blockwise(end=end):
            my_index += len(thing)
            if my_index >= index:
                if isinstance(thing, Block):
                    answer = thing[(index-my_index) - 1]
                    break 
                else:
                    assert my_index == index
                    answer = thing
                    break
        if answer is not None:
            return answer
        raise PathOutOfRangeError

    def get_last_node(self, start=None):
        '''
        Get the last node in the path.
        
        You can optionally specify `start`, which may be either a node or block.
        '''

        thing = None # Setting to None before loop, so we know if loop was empty
        
        for thing in self.iterate_blockwise(start=start):
            pass

        if isinstance(thing, Block):
            return thing[-1]
        elif isinstance(thing, Node):
            return thing
        else: # thing is None
            raise PathOutOfRangeError('''You asked for the last node in the \
path, but it's completely empty.''')
    
        
    def get_node_by_clock(self, clock, rounding=binary_search.CLOSEST,
                          end_node=None):
        '''
        Get a node according to its clock.
        
        See documentation of binary_search.roundings for details about rounding
        options.
        '''
        
        my_function = lambda node: node.state.clock
        return self.get_node_by_monotonic_function(function=my_function,
                                                   value=clock,
                                                   rounding=rounding,
                                                   end_node=end_node)    
        
    
    def get_node_by_monotonic_function(self, function, value,
                                       rounding=binary_search.CLOSEST,
                                       end_node=None):
        '''
        Get a node by specifying a measure function and a desired value.
        
        The function must be a monotonic rising function on the timeline.
        
        See documentation of binary_search.roundings for details about rounding
        options.
        '''
        
        assert issubclass(rounding, binary_search.Rounding)
        
        both = \
             self.__get_node_by_monotonic_function_with_both_rounding(function,
                                                                      value)
        if end_node is not None:
            new_both = list(both)
            end_clock = end_node.state.clock
            if new_both[0] and new_both[0].state.clock >= end_clock:
                new_both[0] = end_node
            if new_both[1] and new_both[1].state.clock >= end_clock:
                new_both[1] = None
            both = new_both
            
        binary_search_profile = \
            binary_search.BinarySearchProfile(self, function, value, both)
        
        return binary_search_profile.results[rounding]
                    
    
    def __get_node_by_monotonic_function_with_both_rounding(self, function,
                                                            value):
        '''
        Get a node by specifying a measure function and a desired value.
        
        The function must be a monotonic rising function on the timeline.
        
        The rounding option used is `binary_search.BOTH`.
        
        Note that this function does not let you specify an end node. Currently
        we're not optimizing for the case where you have an end node and this
        function might waste resources exploring beyond it.
        '''
        
        root = self.root
        
        cmp_root = cmp(function(root), value)
        
        if cmp_root == 1: # function(root) > value
            return (None, root)
        if cmp_root == 0: # function(root) == value
            return (root, root)

        assert cmp_root == -1 # and function(root) < value
        
        # Now we've established that the first node in the path has a strictly
        # lower value than what we're looking for.
        
        # A rule we will strictly obey in this function: `low` will always be a
        # member whose value is lower than the desired value. (Strictly lower,
        # meaning not lower-or-equal.)
        
        low = self.root
        
        for thing in self.iterate_blockwise():
            
            # Rule: Every time we inspect a new node/block, `low` will be the
            # node that is its immediate parent. i.e. The highest node possible
            # from those that we have previously examined.
            
            if isinstance(thing, Block):
                
                block = thing
                
                first = block[0]

                cmp_first = cmp(function(first), value)
                
                if cmp_first == -1: # function(first) < value
                    low = first
                
                elif cmp_first == 0: # function(first) == value
                    return (first, first)
                    
                else: # cmp_first == 1 and function(first) > value
                    return (low, first)
                    
                
                # At this point we know that the first node in the block has a
                # strictly lower value than the target value.
                
                last = block[-1]
                
                cmp_last = cmp(function(last), value)
                
                if cmp_last == -1: # function(last) < value
                    low = last
                    continue
                
                elif cmp_last == 0: # function(last) == value                
                    return (last, last)
                
                else: # cmp_last == 1 and function(last) > value
                    # The two final results are both in the block.
                    return binary_search.binary_search(
                        block, function, value, rounding=binary_search.BOTH
                    )
                    
                
            else: # thing is a Node
                
                node = thing
                
                cmp_node = cmp(function(node), value)
                                
                if cmp_node == -1: # function(node) < value
                    low = node
                    continue
                elif cmp_node == 0: # function(node) == value
                    return (node, node)
                else: # function(node) > value
                    return (low, node)
        

        # If the flow reached here, that means that even the last node in the
        # path has lower value than the value we're looking for.
        
        return (low, None)
            
    
    def get_node_occupying_timepoint(self, timepoint):
        '''
        Get the node which "occupies" the given timepoint.
        
        A node is considered to "occupy" a timepoint if it is the
        highest-clocked node before the timepoint, AND there exists another node
        which has a clock higher than timepoint (that higher node is not
        returned, it just has to exist for the first node to qualify as
        "occupying".)
        
        If no such node exists, returns None.
        '''
        return self.get_node_by_clock(timepoint,
                                      rounding=binary_search.LOW_IF_BOTH)
    

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
        Modify the path to include the specified node.
        
        Optimization note: Don't try to check whether `node in path` before
        calling this method. It's more efficient to just call this method
        without checking first.
        '''
        new_path = node.make_past_path()
        self.root = new_path.root
        self.decisions.update(new_path.decisions)
    
    
    def states(self):
        '''Iterate over the states of the nodes in this path.'''
        # todo: Make fancier, like dict.keys in Py3. Probably create as object
        # in __init__
        for node in self:
            yield node.state
        
            
    def _get_lower_path(self, node):
        '''
        Get a lower path than this one.
        
        "Lower" means that in some point in the past the other path goes through
        a child node with a lower index number (in `children`) than this path.
        
        This method will return the highest path that is just below this path.
        '''
        return self._get_higher_path(node, reverse=True)
                
    
    def _get_higher_path(self, node, reverse=False):
        '''
        Get a higher path than this one.
        
        "Higher" means that in some point in the past the other path goes
        through a child node with a higher index number (in `children`) than
        this path.
        
        This method will return the lowest path that is just above this path.
        '''

        my_iter = __builtin__.reversed if reverse else iter
        
        wanted_clock = node.state.clock
        
        for (kid, parent) in cute_iter_tools.consecutive_pairs(reversed(self)):
            if len(parent.children) == 1:
                continue
            my_index = parent.children.index(kid)

            if reverse:
                if my_index > 0:
                    kids_to_try = parent.children[:my_index]
                    break
            
            if not reverse:
                if my_index < len(parent.children) -1:
                    kids_to_try = parent.children[my_index+1:]
                    break
        else:
            raise PathLookupError('This path is the %s one.' % \
                                  ('lowest' if reverse else 'highest'))
        
        for node in my_iter(kids_to_try):
            paths = node.all_possible_paths() # todo: make reversed argument
            for path in my_iter(paths):
                assert isinstance(path, Path)
                if path[-1].state.clock >= wanted_clock:
                    return path
        
        raise PathLookupError('''This path is the %s one which extends enough \
in the future to the clock of the specified node.''' % \
            ('lowest' if reverse else 'highest'))
               
            
    def __repr__(self):
        '''
        Get a string representation of the path.
        
        Example output:
        <garlicsim.data_structures.Path of length 43 at 0x1c822d0>
        '''
        return '<%s of length %s at %s>' % \
               (
                   misc_tools.shorten_class_address(
                       self.__class__.__module__,
                       self.__class__.__name__
                   ),
                   len(self),
                   hex(id(self))
               )
    
    
    def copy(self):
        '''Make a shallow copy of the path.'''
        
        # Most of these things don't need duplicating, but just for
        # completeness' sake:
        tree = self.tree
        root = self.root
        decisions = self.decisions.copy()
        
        path = Path(tree=tree, root=root, decisions=decisions)
        
        return path
    
    __copy__ = copy
    
    def __eq__(self, other):
        # Currently horribly inefficient
        assert isinstance(other, Path)
        return list(self) == list(other)
        
    def __req__(self, other):
        return self.__eq__(other)
    
    
from tree import Tree