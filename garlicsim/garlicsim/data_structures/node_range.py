# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `NodeRange` class.

See its documentation for more info.
'''

from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc import misc_tools
from garlicsim.general_misc import address_tools

from .node import Node
from .block import Block


class NodeRange(object):
    '''A consecutive range of nodes.'''

    def __init__(self, head, tail):
        '''
        Construct a NodeRange.
        
        `head` is the node or block in which this range starts.
        
        `tail` is the node or block in which this range ends.
        '''
        
        self.head = head
        '''The node or block in which this range starts.'''
        
        self.tail = tail
        '''The node or block in which this range ends.'''
    
        
    def make_path(self):
        '''Make a path that goes through this node range.'''
        node_around_tail = self.tail if isinstance(self.tail, Node) else \
                           self.tail[0]
        return node_around_tail.make_containing_path()

    
    def _sanity_check(self):
        '''
        Assert there are no obvious problems with this node range.
        
        This checks that the tail node/block is a descendent of the head
        node/block.
        '''
        path = self.make_path()
        assert (self.head in path.__iter__(tail=self.tail))
        
        
    def __iter__(self):
        '''Iterate on the nodes in this range.'''
        return self.make_path().__iter__(head=self.head, tail=self.tail)

    
    def iterate_blockwise(self):
        '''
        Iterate on the nodes in this range, returning blocks where possible.
        '''
        path = self.make_path()
        return path.iterate_blockwise(head=self.head, tail=self.tail)

    
    def __contains__(self, node):
        '''Return whether `node` is in this node range.'''
        # todo: can do blocks?
        path = self.make_path()
        return path.__contains__(node, head=self.head, tail=self.tail)

    
    def clone_with_blocks_dissolved(self):
        '''
        Make a node range that is specified with nodes and not blocks.
        
        A node range will be constructed that in this point of time is
        equivalent to the original node range, but whose `head` and `tail` are
        specified as nodes and not as blocks.
        '''
        if isinstance(self.head, Block):
            new_head = self.head[0]
        else:
            new_head = self.head
        if isinstance(self.tail, Block):
            new_tail = self.tail[-1]
        else:
            new_tail = self.tail
        
        return NodeRange(new_head, new_tail)

    
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
        return type(self)(self.head, self.tail)

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
                   
                   address_tools.describe(type(self), shorten=True),
                   
                   'block that starts at clock' if isinstance(self.head, Block)
                   else 'node with clock',
                   
                   self.head[0].state.clock if isinstance(self.head, Block)
                   else self.head.state.clock,
                   
                   'block that ends at clock' if \
                   isinstance(self.tail, Block) else 'node with clock',
                   
                   self.tail[-1].state.clock if isinstance(self.tail, Block) \
                   else self.tail.state.clock,
                   
                   cute_iter_tools.get_length(self),
                
                   hex(id(self))
               )
    
    
    def __eq__(self, other):
        if not isinstance(other, NodeRange):
            return False
        r1 = self.clone_with_blocks_dissolved()
        r2 = other.clone_with_blocks_dissolved()
        return (r1.head is r2.head) and (r1.tail is r2.tail)

    
    def __req__(self, other):
        return self.__eq__(other)
    