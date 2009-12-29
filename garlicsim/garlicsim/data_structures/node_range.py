'''tododoc'''

from node import Node

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

    def __contains__(self, node):
        path = self.make_path()
        return path.__contains__(node, start=self.start, end=self.end)
        