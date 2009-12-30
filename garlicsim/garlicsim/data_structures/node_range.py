'''tododoc'''

from node import Node
from block import Block

class NodeRange(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def make_path(self):
        node_around_end = self.end if isinstance(self.end, Node) else \
                          self.end[0]
        return node_around_end.make_containing_path()
        
    def is_valid(self):
        path = self.make_path()
        return (self.start in path.__iter__(end=self.end))
        
    def __iter__(self):
        return self.make_path().__iter__(start=self.start, end=self.end)
    
    def iterate_blockwise(self):
        path = self.make_path()
        return path.iterate_blockwise(start=self.start, end=self.end)

    def __contains__(self, node):
        path = self.make_path()
        return path.__contains__(node, start=self.start, end=self.end)
    
    def with_blocks_dissolved(self):
        if isinstance(self.start, Block):
            new_start = self.start[0]
        else:
            new_start = self.start
        if isinstance(self.end, Block):
            new_end = self.end[-1]
        else:
            new_end = self.end
        
        return NodeRange(new_start, new_end)
    
    def get_outside_children(self):
        outside_children = []
        for thing in self.iterate_blockwise():
            candidate = thing if isinstance(thing, Node) else thing[-1]
            outside_children += [child for child in candidate.children if child
                                 not in self]
        return outside_children
            
        
        