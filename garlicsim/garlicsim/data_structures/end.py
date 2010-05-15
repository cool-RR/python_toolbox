# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
A module that defines the Node class and the related NodeError exception.

See documentation of Node for more information.
'''


from garlicsim.general_misc import misc_tools

from tree_member import TreeMember
from node import Node

    
class End(TreeMember):
    
    def __init__(self, tree, parent, step_profile=None):
        '''
        Construct the node.
        
        `tree` is the tree in which this node resides. `state` is the state it
        should contain. `parent` is its parent node in the tree, which may be
        None for a root. `step_profile` is the step profile with which the state
        was crunched, which may be None for a state that was created from
        scratch. `touched` is whether the state was modified/created from
        scratch, in contrast to having been produced by crunching.
        '''
        
        self.tree = tree
        '''The tree in which this node resides.'''
        
        assert isinstance(parent, Node)
        self.parent = parent
        '''The parent node of this node.'''
        
        self.parent.ends.append(self)
        
        self.step_profile = step_profile
        '''
        The step options profile with which the contained state was created.
        
        For an untouched node, this must be a real StepProfile, even an empty
        one. Only a touched node which was created from scratch should have
        None for its step profile.
        '''
        
  
        
    def __len__(self):
        '''Just return 1. This is useful because of blocks.'''
        return 1

    
        
    def get_block(self):
        '''
        If this node is a member of a block, return the block.
        
        Otherwise, return the node itself.
        '''
        return self

    
    def make_containing_path(self):
        '''
        Create a path that contains this node.
        
        There may be multiple different paths that contain this node. This will
        return the one which points to the newest possible forks.
        Returns the path.
        '''
        
        return self.parent.make_containing_path()
    

    
        
    def all_possible_paths(self):
        '''
        Get a list of all possible paths that contain this node.
        
        Note: There may be paths that contain this node which will not be
        identical to one of the paths given here, because these other paths
        may specify decisions that are not even on the same root as these
        paths.
        '''
        return self.parent.all_possible_paths()
    
    
    def make_past_path(self):
        '''
        Create a path that contains this node.
        
        There may be multiple different paths that contain this node. This will
        return a path that doesn't specify any decisions after this node.
        '''
        return self.parent.make_past_ath()

    
    def get_all_leaves(self, max_nodes_distance=None, max_clock_distance=None):
        '''
        Get all leaves that are descendents of this node.
        
        Only leaves with a distance of at most `max_nodes_distance` in nodes or
        `max_clock_distance` in clock are returned. (Note this is an OR
        relation between the two condintions)
        
        Returns a dict of the form:
        
        {
            leaf1: {
                'nodes_distance': nodes_distance1,
                'clock_distance': clock_distance1,
            },            
            leaf2: {
                'nodes_distance': nodes_distance2,
                'clock_distance': clock_distance2,
            },
            # ...
        }
            
        '''
        
        return {} # tododoc: I assume now that `leaves` don't include ends

    
    def get_ancestor(self, generations=1, round=False):
        ''''''

        assert generations >= 0
        if generations == 0:
            return self
        if generations >= 1:
            return self.parent(generations - 1, round)

            
    def get_root(self):
        '''
        Get the root of this node.
        
        This means the node which is the parent of the parent of the parent
        of... the parent of this node.
        '''
        return self.parent.get_root()
    
    
    
    def is_overlapping(self, other):
        '''
        Return whether this node overlaps with the given entity.
        
        `other` may be a node, in which case overlapping means being the same
        node. `other` can also be a block, in which case overlapping means this
        node is contained in the block.
        '''
        if other is None: return False
        if isinstance(other, Node):
            return (self is other)
        else:
            assert isinstance(other, Block)
            return (self in other)
    
    
    def __repr__(self):
        '''
        Get a string representation of the node.
        
        Example output:        
        <garlicsim.data_structures.Node with clock 6.5, untouched, belongs to a
        block, crunched with StepProfile(t=0.1), at 0x1ffde70>
        '''
        return 'END tododoc parent: %s' % self.parent
        """
        return '<%s%s, %s%s%s, %s, %sat %sEND tododoc>' % \
            (
                misc_tools.shorten_class_address(
                    self.__class__.__module__,
                    self.__class__.__name__
                    ),
                ' with clock %s' % self.state.clock if hasattr(self.state, 'clock') else '',
                'root, ' if (self.parent is None) else '',
                'leaf, ' if (len(self.children) == 0) else '',
                'touched' if self.touched else 'untouched',
                'belongs to a block' if self.block else 'blockless',
                'crunched with %s, ' % self.step_profile if self.step_profile else '',
                hex(id(self))
            )
        """

from block import Block


