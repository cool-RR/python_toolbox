from garlicsim.state.node import Node
import garlicsim.misc.binary_search as binary_search

def get_item(path, end_node, index):
    if index >= 0:
        return get_item_positive(path, end_node, index)
    else: # index < 0
        return get_item_negative(path, end_node, index)
    
def get_item_positive(path, end_node, index):
    result = path[index]
    if result.state.clock > end_node.state.clock:
        raise IndexError
    
def get_item_negative(path, end_node, index):
    return path._Path__get_item_negative(index, starting_at=end_node)


def get_node_by_monotonic_function(path, end_node,
                                   function, value,
                                   rounding="Closest"):
    
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
    get_clock = lambda node: node.state.clock
    return get_node_by_monotonic_function(path, end_node,
                                          get_clock, clock,
                                          rounding=rounding)

def length(path, end_node):
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