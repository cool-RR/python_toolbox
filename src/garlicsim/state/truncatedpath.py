
from tree import *
from node import *
from block import *
from path import *

import garlicsim.misc.binarysearch as binarysearch

class Segment(object):
    def __init__(self, path, end_node):
        self.path = path
        self.end_node = end_node
        self.length = self.calculate_length()
        
    def calculate_length(self):
        
        length = 0
        
        for thing in self.path.iterate_blockwise():
            if isinstance(thing, Block):
                if self.end_node in thing:
                    index = binarysearch.binary_search_by_index \
                                (Block, lambda node: node.state.clock,
                                 self.end_node.state.clock, rounding="Exact")
                    length += index + 1
                    return length
                else: # self.end_node is not in the block
                    length += len(thing)
            else: # thing is a node
                if thing == self.end_node:
                    length += 1
                    return length
                else: # thing != self.end_node	
                    length += 1
                    continue
            
        raise StandardError("We didn't reach the end node")
    
    def __getitem__(self, index):
        assert isinstance(index, int)
        if index < 0: return self.__get_item_negative(index)
        else: return self.__get_item_positive(index)
        
    def __get_item_negative(self, index):
        if index == -1: return self.end_node
        
        pass    
    
    def __get_item_positive(self, index):
        pass
        
        
        
        
        
        
        
        
        
        
        