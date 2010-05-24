# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the End class.

See its documentation for more information.
'''

from garlicsim.general_misc import misc_tools

from tree_member import TreeMember
from node import Node

    
class End(TreeMember):
    '''
    An end of the simulation.
    
    An `End` signifies that the simulation has ended. This is relevant in only
    some simpacks; Some simpacks have a concept of ending the simulation, and
    some don't. When a simulation was crunched and reached its end on some
    timeline, the last node on that timeline will have an `End` object added to
    its `.ends` list.
    '''
    
    def __init__(self, tree, parent, step_profile=None):
        
        self.tree = tree
        '''The tree in which this end resides.'''
        
        assert isinstance(parent, Node)
        self.parent = parent
        '''
        The parent node of this end.
        
        Note that this parent node will not have this end as a child; It will
        list the end in its `.ends` attribute.
        '''
        
        self.parent.ends.append(self)
        
        self.step_profile = step_profile
        '''The step options profile with which the end was reached.'''
        
        
    def __len__(self):
        '''Just return 1. This is useful because of blocks.'''
        return 1

    
        
    def soft_get_block(self):
        '''
        Just return `self`.
        
        (This is a method of all TreeMembers that returns the block that the
        tree member belongs to, if there is one. But an end never belongs to a
        block.
        '''
        return self

    
    def make_containing_path(self):
        '''
        Create a path that leads to this end.
        
        Returns the path.
        '''
        return self.parent.make_containing_path()
    

    def all_possible_paths(self):
        '''
        Get a list of all possible paths that lead to this end.
        
        (This method was invented for nodes and blocks and makes sense for them;
        For an end, it will just return the one single path that leads to it,
        since there can't be any forks after an end.)
        
        Note: There may be paths that contain this node which will not be
        identical to one of the paths given here, because these other paths
        may specify decisions that are not even on the same root as these
        paths.
        '''
        return self.parent.all_possible_paths()
    
    
    def make_past_path(self):
        '''
        Create a path that leads to this end.
        
        (This method was invented for nodes and blocks and makes sense for them;
        For an end, the "past path" is identical to the one made by
        `make_containing_path`, since there can't be any forks after an end.)
        
        Returns the path.
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


