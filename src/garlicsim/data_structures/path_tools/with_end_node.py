"""
A collection of functions for handling paths when defining an end node.
Normally, a path has no end node. But sometimes we wish to specify a node
in which the path ends. When we do that the normal methods associated with
the path are no longer relevant, since they are not designed to handle
an end node.
These function are, and they take a path and an end node as their
parameters.
"""

from garlicsim.data_structures.node import Node
import garlicsim.misc.binary_search as binary_search

def get_item(path, end_node, index):
    """
    Gets a node from the path by index number.
    
    Only releveant for paths which have an end node; See this module's
    documentation for more info.
    """
    if index >= 0:
        return get_item_positive(path, end_node, index)
    else: # index < 0
        return get_item_negative(path, end_node, index)
    
def get_item_positive(path, end_node, index):
    """
    Gets a node from the path by index number, given that the index number
    is positive.
    
    Only releveant for paths which have an end node; See this module's
    documentation for more info.
    """
    result = path[index]
    if result.state.clock > end_node.state.clock:
        raise IndexError
    
def get_item_negative(path, end_node, index):
    """
    Gets a node from the path by index number, given that the index number
    is positive.
    
    Only releveant for paths which have an end node; See this module's
    documentation for more info.
    """
    return path._Path__get_item_negative(index, starting_at=end_node)


def get_node_by_monotonic_function(path, end_node,
                                   function, value,
                                   rounding="Closest"):
    """
    Gets a node by specifying a measure function and a desired value.
    The function must be a monotonic rising function on the timeline.
    
    See documentation of garlicsim.misc.binary_search.binary_search for
    details about rounding options.
    
    Only releveant for paths which have an end node; See this module's
    documentation for more info.
    """
    both = path.get_node_by_monotonic_function(function, value,
                                               rounding="Both")
    
    new_both = both[:]
    if new_both[0].state.clock >= end_node.state.clock:
        new_both[0] = end_node
    if new_both[1].state.clock >= end_node.state.clock:
        new_both[1] = None
    
    return binary_search.make_both_data_into_preferred_rounding(new_both,
                                                                function,
                                                                value,
                                                                rounding)

def get_node_by_clock(path, end_node, clock, rounding="Closest"):
    """
    Gets a node from the path by clock reading.
    
    Only releveant for paths which have an end node; See this module's
    documentation for more info.
    """
    get_clock = lambda node: node.state.clock
    return get_node_by_monotonic_function(path, end_node,
                                          get_clock, clock,
                                          rounding=rounding)

def length(path, end_node):
    """
    Gets the length of the path.
    
    Only releveant for paths which have an end node; See this module's
    documentation for more info.
    """
    length = 0
    for thing in path.iterate_blockwise():
        if thing.block:
            if end_node in thing:
                length += thing.block.index(end_node) + 1
                return length
            else: # end_node is not in thing
                length += len(thing)
                continue
        else: # thing is a blockless node
            length += 1
            if thing == end_node: return length
        
    raise StandardError("Didn't reach end_node!")