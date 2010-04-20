'''tododoc'''

from node import Node
from block import Block

class NodeRange(object):
    '''A consecutive range of nodes.'''

    def __init__(self, start, end):
        
        self.start = start
        '''The node in which this range starts.'''
        
        self.end = end
        '''The node in which this range ends.'''
    
        
    def make_path(self):
        '''Make a path that goes through this node range.'''
        node_around_end = self.end if isinstance(self.end, Node) else \
                          self.end[0]
        return node_around_end.make_containing_path()

    
    def _sanity_check(self):
        '''
        Assert there are no obvious problems with this node range.
        
        This checks that the end node is a descendent of the start node.
        '''
        path = self.make_path()
        assert (self.start in path.__iter__(end=self.end))
        
    def __iter__(self):
        '''Iterate on the nodes in this range.'''
        return self.make_path().__iter__(start=self.start, end=self.end)
    
    def iterate_blockwise(self):
        '''
        Iterate on the nodes in this range, returning blocks where possible.
        '''
        path = self.make_path()
        return path.iterate_blockwise(start=self.start, end=self.end)

    def __contains__(self, node):
        path = self.make_path()
        return path.__contains__(node, start=self.start, end=self.end)
    
    def clone_with_blocks_dissolved(self):
        '''
        Make a node range that is specified with nodes and not blocks.
        
        A node range will be constructed that in this point of time is
        equivalent to the original node range, but whose `start` and `end` are
        specified as nodes and not as blocks.
        '''
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
            
        
        