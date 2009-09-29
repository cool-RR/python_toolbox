# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
A module that defines the `Path` class. See its documentation for more
information.
"""

from node import Node
from block import Block
# Note we are doing `from tree import Tree` in the bottom of the file.

import garlicsim.misc.binary_search as binary_search

__all__ = ["Path", "PathError", "PathOutOfRangeError"]

class PathError(Exception):
    """
    An exception related to the class Path.
    """
    pass

class PathOutOfRangeError(Exception):
    """
    An exception related to the class Path, raised when nodes are requested
    from the path which are out of its range for whatever reason.
    """
    pass

class Path(object):
    """
    A path symbolizes a line of nodes in a tree. A tree may be complex and
    contain many junctions, but a path is a direct line through it. Therefore,
    a path object contains information about which child to choose when going
    through a node which has multiple children.
    
    The attribute ".decisions" is a dictionary of the form {node_which_forks: 
    node_to_continue_to, ... }. It usually contains as keys only nodes that
    have more than one child.
    
    The attribute ".root" says from which node the path begins.
    """
    def __init__(self, tree, root=None, decisions={}):
        self.tree = tree
        self.root = root # The root node
        
        self.decisions = dict(decisions)
        """
        The decisions dict says which fork of the road the path chooses.
        It's of the form {parent_node: child_node,...}
        """

    def __len__(self, end_node=None):
        """
        Returns the length of the path in nodes. You can optionally specify an
        end node, in which the path ends.
        """
        if self.root is None: return 0
        length = 0
        for thing in path.iterate_blockwise():
            if thing.block:
                if end_node and end_node in thing:
                    length += thing.block.index(end_node) + 1
                    return length
                else: # end_node is not in thing
                    length += len(thing)
                    continue
            else: # thing is a blockless node
                length += 1
                if thing == end_node: return length
        
        if end_node is None:
            return length
        else:
            raise PathError("Didn't reach end_node!")

    def __iter__(self):
        if self.root is None:
            raise StopIteration
        yield self.root
        current = self.root
        while True:
            try:
                current = self.next_node(current)
                yield current
            except PathOutOfRangeError:
                raise StopIteration
            
    def iterate_blockwise(self, starting_at=None):
        """
        Iterates on the path, returning blocks when possible. You are allowed
        to specify a node/block from which to start iterating, using the
        parameter `starting_at`.
        """
        if starting_at is None:
            if self.root is None:
                raise StopIteration
            current = self.root.soft_get_block()
        else:
            current = starting_at.soft_get_block()

        yield current

        while True:
            try:
                current = self.next_node(current).soft_get_block()
                yield current
            except PathOutOfRangeError:
                raise StopIteration
    
    def iterate_blockwise_reversed(self, end_node):
        """
        Iterates backwards on the path, returning blocks when possible.
        You must specify a node/block from which to start iterating,
        using the parameter `starting_at`.
        """
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
        """
        Returns whether the path contains `thing` which may be a node or a
        block.
        """
        assert isinstance(thing, Node) or isinstance(thing, Block)

        for x in self.iterate_blockwise():
            if x == thing:
                return True
            elif isinstance(x, Block) and thing in x:
                return True
            
        return False


    def next_node(self, thing):
        """
        Returns the next node on the path.
        
        If we've come to a fork for which we have no key in the decisions dict,
        we choose the most recent child node, and update the decisions dict to
        point to it as well.
        """
        
        # We're dealing with the case of 1 child first, because it's the most common.
        real_thing = thing if isinstance(thing, Node) else thing[-1]
        kids = real_thing.children
        if len(kids) == 1:
            return kids[0]
        
        if self.decisions.has_key(thing) or self.decisions.has_key(real_thing):
            return self.decisions.get(thing, None) or \
                   self.decisions.get(real_thing, None)
        
        if len(kids) > 1:
            kid = kids[-1]
            self.decisions[real_thing] = kid
            return kid

        else: # no kids
            raise PathOutOfRangeError
            

    def __getitem__(self, index, end_node=None):
        """
        Gets a node by its index number in the path. You can optionally specify
        an end node in which the path ends.
        """
        assert isinstance(index, int)
        
        if index >= 0:
            return self.__get_item_positive(index, end_node=end_node)
        else:
            return self.__get_item_negative(index, end_node=end_node)

    def __get_item_negative(self, index, end_node=None):
        """
        Gets a node by its index number in the path, assuming that number is
        negative.
        """
        if end_node == None:
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
        """
        Gets a node by its index number in the path, assuming that number is
        positive.
        """
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
                return thing
        raise PathOutOfRangeError

    def get_last_node(self, starting_at=None):
        """
        Returns the last node in the path.
        Optionally, you are allowed to specify a node from which to start
        searching.
        """
        for thing in self.iterate_blockwise(starting_at=starting_at):
            pass

        if isinstance(thing, Block):
            return thing[-1]
        else:
            return thing
    
    def get_node_by_clock(self, clock, rounding="Closest", end_node=None):
        """
        Gets a node according to its clock reading.
        
        See documentation of garlicsim.misc.binary_search.binary_search for
        details about rounding options.
        """
        
        my_function = lambda node: node.state.clock
        return self.get_node_by_monotonic_function(function=my_function,
                                                   value=clock,
                                                   rounding=rounding,
                                                   end_node=end_node)    
        
    def get_node_by_monotonic_function(self, function, value,
                                       rounding="Closest", end_node=None):
        """
        Gets a node by specifying a measure function and a desired value. The
        function must be a monotonic rising function on the timeline.
        
        See documentation of garlicsim.misc.binary_search.binary_search for
        details about rounding options.
        """
        
        assert rounding in ["High", "Low", "Exact", "Both", "Closest"]        

        if end_node is None:
            correct_both_for_end_node = lambda both: both
        else:
            def correct_both_for_end_node(both):
                new_both = both[:]
                if new_both[0].state.clock >= end_node.state.clock:
                    new_both[0] = end_node
                if new_both[1].state.clock >= end_node.state.clock:
                    new_both[1] = None
        
        low = self.root
        
        if function(low) >= value:
            both = correct_both_for_end_node((None, low))
            return binary_search.make_both_data_into_preferred_rounding \
                   (both, function, value, rounding)
        
        """
        Now we've established that the first node in the path has a lower value
        than what we're looking for.
        """
        
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
                                                       rounding="Both")
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
        
        """
        If the flow reached here, that means that even the last node
        in the path has lower value than the value we're looking for.
        """
        
        both = correct_both_for_end_node((low, None))
        return binary_search.make_both_data_into_preferred_rounding \
               (both, function, value, rounding)
            
        
    
    def get_node_occupying_timepoint(self, timepoint):
        """
        Takes a timepoint. Checks whether we have at least one node that is
        before this timepoint and one that is after this time point. If that
        is the case, returns the node immediately before the time point.
        Otherwise, returns None.
        """
        temp = self.get_node_by_clock(timepoint, rounding="Both")
        if temp.count(None)==0:
            return temp[0]
        else:
            return None
        

    def get_existing_time_segment(self, start_time, end_time):
        """
        Between timepoints "start_time" and "end_time", returns the segment of
        nodes that exists in the Path.
        Returns the segment like so: [start, end]
        
        Example: In the path the first node's clock reading is 3.2, the last is
        7.6. start_time is 2 and end_time is 5. The function will return
        [3.2, 5].
        """

        clock_of_first = self.root.state.clock
        clock_of_last = self.get_last_node().state.clock
        
        if clock_of_first <= end_time and clock_of_last >= start_time:            
            return [max(clock_of_first, start_time),
                    min(clock_of_last, end_time)]
        else:
            return None
    
    def modify_to_include_node(self, node):
        """
        Modifies the path so it will include the specified node.
        """
        new_path = node.make_containing_path()
        self.root = new_path.root
        self.decisions.update(new_path.decisions)
        
    
from tree import Tree