"""
A module that defines the `Path` class. See
its documentation for more information.
"""

from node import Node
from block import Block
import path_tools
# Note we are doing `from tree import Tree` in the bottom of the file
# to avoid problems with circular imports.

import garlicsim.misc.binary_search as binary_search

__all__ = ["Path"]

class Path(object):
    """
    A path symbolizes a line of nodes in a tree.
    A tree may be a complex tree with many junctions,
    but a path is a direct line. Therefore, a path object contains
    information about which child to choose when going through
    a node which has multiple children.
    """
    def __init__(self, tree, root=None, decisions={}):
        
        self.tree = tree

        self.root = root # The root node

        self.decisions = decisions.copy()
        """
        The decisions dict says which fork of the road the path chooses.
        It's of the form {parent_node: child_node,...}
        """


    def __len__(self, end_node=None):
        if end_node is not None:
            return path_tools.with_end_node.length(self, end_node)
        if self.root is None:
            return 0

        result = 0
        for j in self.iterate_blockwise():
            result += len(j)

        return result

    def __iter__(self):
        if self.root is None:
            raise StopIteration
        yield self.root
        current = self.root
        while True:
            try:
                current = self.next_node(current)
                yield current
            except IndexError:
                raise StopIteration
            
    def iterate_blockwise(self, starting_at=None):
        """
        Iterates on the Path, returning Blocks when possible.
        You are allowed to specify a node/block from
        which to start iterating, using the parameter `starting_at`.
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
            except IndexError:
                raise StopIteration("Ran out of tree")
    
    def iterate_blockwise_reversed(self, starting_at):
        """
        Iterates backwards on the Path, returning Blocks when possible.
        You must specify a node/block from which to start iterating,
        using the parameter `starting_at`.
        """
        current = starting_at.soft_get_block()

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
        Returns whether the path contains `thing`.
        `thing` may be a Node or a Block.
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
        """
        if self.decisions.has_key(thing):
            next = self.decisions[thing]
            assert isinstance(next, Node)
            return self.decisions[thing]
        
        if isinstance(thing, Block):
            if self.decisions.has_key(thing[-1]):
                return self.decisions[thing[-1]]

        else:
            if isinstance(thing, Block):
                kids = thing[-1].children
            else:
                kids = thing.children
            if len(kids) > 0:
                kid = kids[-1]
                self.decisions[thing] = kid
                return kid

        raise IndexError("Ran out of tree")


    def __getitem__(self, index, end_node=None):
        """
        Gets a node by its index number in the path.
        You can optionally specify an end node in which the path ends.
        """

        if end_node is not None:
            return path_tools.with_end_node.get_item(self, end_node, index)
        
        assert isinstance(index, int)
        
        if index >= 0:
            return self.__get_item_positive(index)
        else:
            return self.__get_item_negative(index)

    def __get_item_negative(self, index, starting_at=None):
        """
        Gets a node by its index number in the path, assuming that number is
        negative.
        """
        if starting_at == None:
            starting_at = self.get_last_node()
        else:
            assert isinstance(starting_at, Node)
        if index == -1:
            return starting_at
        
        my_index = 0
        
        if starting_at.block:
            block = starting_at.block
            index_of_starting_at = block.index(starting_at)
            
            my_index -= (index_of_starting_at + 1)
            
            if my_index <= index:
                return block[index - my_index]
        
        for thing in self.iterate_blockwise_reversed(starting_at=starting_at):
            my_index -= len(thing)
            if my_index <= index:
                if isinstance(thing, Block):
                    return thing[ (index - my_index)]
                else:
                    assert my_index == index
                    return thing
        raise IndexError
        
        
    def __get_item_positive(self, index):
        """
        Gets a node by its index number in the path, assuming that number is
        positive.
        """
        my_index = -1
        for thing in self.iterate_blockwise():
            my_index += len(thing)
            if my_index >= index:
                if isinstance(thing, Block):
                    return thing[(index-my_index) - 1]
                else:
                    assert my_index == index
                    return thing
        raise IndexError

    def get_last_node(self, starting_at=None):
        """
        Returns the last node in the path.
        Optionally, you are allowed to specify a node from
        which to start searching.
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
        if end_node is not None:
            return path_tools.with_end_node.get_node_by_clock(self, end_node,
                                                                clock,
                                                                rounding)
        
        my_function = lambda node: node.state.clock
        return self.get_node_by_monotonic_function(function=my_function,
                                                   value=clock,
                                                   rounding=rounding)    
        
    def get_node_by_monotonic_function(self, function, value,
                                       rounding="Closest", end_node=None):
        """
        Gets a node by specifying a measure function and a desired value.
        The function must be a monotonic rising function on the timeline.
        
        See documentation of garlicsim.misc.binary_search.binary_search for
        details about rounding options.
        """
        if end_node is not None:
            return path_tools.with_end_node.\
                   get_node_by_monotonic_function(self, end_node, function,
                                                  value, rounding=rounding)
        
        assert rounding in ["High", "Low", "Exact", "Both", "Closest"]        
        
        low = self.root
        
        if function(low) >= value:
            return binary_search.make_both_data_into_preferred_rounding \
                   ((None, low), function, value, rounding)
        
        """
        Now we've established that the first node in the path has a lower value
        than what we're looking for.
        """
        
        for thing in self.iterate_blockwise():
            if isinstance(thing, Block):
                first = thing[0]
                if function(first) >= value:
                    return binary_search.make_both_data_into_preferred_rounding \
                           ((low, first), function, value, rounding)
                    
                last = thing[-1]
                if function(last) >= value:
                    # It's in the block
                    return binary_search.binary_search(thing, \
                           function, value, rounding)
                else:
                    low = last
                    continue
            else: # thing is a Node
                if function(thing) >= value:
                    return binary_search.make_both_data_into_preferred_rounding \
                           ((low, thing), function, value, rounding)
                else:
                    low = thing
                    continue
        
        """
        If the flow reached here, that means that even the last node
        in the path has lower value than the value we're looking for.
        """
        
        return binary_search.make_both_data_into_preferred_rounding \
               ((low, None), function, value, rounding)
            
        
    
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
        Between timepoints "start_time" and "end_time", returns the segment of nodes that
        exists in the Path.
        Returns the segment like so: [start, end]
        Example: In the path the first node's clock reading is 3.2, the last is 7.6.
        start_time is 2 and end_time is 5. The function will return [3.2, 5]
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
        Modifies the path so it will include the mentioned node.
        """
        new_path = node.make_containing_path()
        self.root = new_path.root
        self.decisions.update(new_path.decisions)
        
    
    

from tree import Tree
