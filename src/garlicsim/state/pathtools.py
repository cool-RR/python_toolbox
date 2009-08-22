from node import *

def get_item_with_end_node(path, end_node, index):
    if index >= 0:
        return __get_item_with_end_node_positive(path, end_node, index)
    else: # index < 0
        return __get_item_with_end_node_negative(path, end_node, index)
    
def __get_item_with_end_node_positive(path, end_node, index):
    result = path[index]
    if result.state.clock > end_node.state.clock:
        raise IndexError
    
def __get_item_with_end_node_negative(path, end_node, index):
    return path.__get_item_negative(index, starting_at=end_note)

def get_node_by_monotonic_function_with_end_node(path, end_node, function, value, rounding="Closest"):
    pass

def get_node_by_clock_with_end_node(path, end_node, clock, rounding="Closest"):
    pass

