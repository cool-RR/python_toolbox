# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the NodeRange class.

See its documentation for more info.
'''

from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc import misc_tools

from node import Node
from block import Block

class NodeRange(object):
    '''A consecutive range of nodes.'''

    def __init__(self, start, end):
        '''
        Construct a NodeRange.
        
        `start` is the node or block in which this range starts.
        
        `end` is the node or block in which this range ends.
        '''
        
        self.start = start
        '''The node or block in which this range starts.'''
        
        self.end = end
        '''The node or block in which this range ends.'''
    
        
    def make_path(self):
        '''Make a path that goes through this node range.'''
        node_around_end = self.end if isinstance(self.end, Node) else \
                          self.end[0]
        return node_around_end.make_containing_path()

    
    def _sanity_check(self):
        '''
        Assert there are no obvious problems with this node range.
        
        This checks that the end node/block is a descendent of the start
        node/block.
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
        '''
        Get all the non-member children nodes of nodes which are members.
        
        This returns every node which is (a) a child of a node in this node
        range and (b) not in this node range itself.
        '''
        outside_children = []
        for thing in self.iterate_blockwise():
            candidate = thing if isinstance(thing, Node) else thing[-1]
            outside_children += [child for child in candidate.children if child
                                 not in self]
        return outside_children
            
    def copy(self):
        '''Shallow-copy the node range.'''
        klass = type(self)
        return klass(self.start, self.end)

    __copy__ = copy
    
    def __repr__(self):
        '''
        Get a string representation of the node range.
        
        Example output:
        <garlicsim.data_structures.NodeRange, from node with clock 2 to block
        that ends at clock 102, containing 101 nodes total, at 0x291c550>
        '''
        return '<%s, from %s %s to %s %s, containing %s nodes total, at %s>' \
               % (
                   
                   misc_tools.shorten_class_address(
                       self.__class__.__module__,
                       self.__class__.__name__
                       ),
                   
                   'block that starts at clock' if isinstance(self.start, Block) \
                   else 'node with clock',
                   
                   self.start[0].state.clock if isinstance(self.start, Block) \
                   else self.start.state.clock,
                   
                   'block that ends at clock' if \
                   isinstance(self.end, Block) else 'node with clock',
                   
                   self.end[-1].state.clock if isinstance(self.end, Block) \
                   else self.end.state.clock,
                   
                cute_iter_tools.get_length(self),
                
                hex(id(self))
               )
    
    def __eq__(self, other):
        if not isinstance(other, NodeRange):
            return False
        r1 = self.clone_with_blocks_dissolved()
        r2 = other.clone_with_blocks_dissolved()
        return (r1.start is r2.start) and (r1.end is r2.end)
    
    def __req__(self, other):
        return self.__eq__(other)