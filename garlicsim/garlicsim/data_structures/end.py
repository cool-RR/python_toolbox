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
        Get `{}`.
        
        (This method was invented for nodes and blocks and makes sense for them;
        There are no leaves, or anything else for that matter, that come after
        an end.)
        '''
        
        return {}

    
    def get_ancestor(self, generations=1, round=False):
        '''
        Get an ancestor of this end.
        
        `generations` specifies the number of generation that the returned
        ancestor should be above the current end. `round` determines how this
        method will behave if it was asked for too many generations back, and
        not enough existed. If `round` is True, it will return the root. If
        `round` is False, it will raise a LookupError.
        '''

        assert generations >= 0
        if generations == 0:
            return self
        if generations >= 1:
            return self.parent(generations - 1, round)

            
    def get_root(self):
        '''
        Get the root of this end.
        
        This means the node which is the parent of the parent of the parent
        of... the parent of this end.
        '''
        return self.parent.get_root()
    
    
    
    def is_overlapping(self, other):
        '''
        Return whether this end overlaps with the given entity.
        
        Returns True only if `other` is the same end.
        '''
        return self is other
    
    
    def __repr__(self):
        '''
        Get a string representation of the end.
        
        Example output:        
        <garlicsim.data_structures.End from state with clock 6.5, crunched with
        StepProfile(t=0.1), at 0x1ffde70>
        '''
        
        return '<%s from state with clock %s, crunched with %s, at %s>' % \
            (
                misc_tools.shorten_class_address(
                    self.__class__.__module__,
                    self.__class__.__name__
                    ),
                self.parent.state.clock,
                self.step_profile,
                hex(id(self))
            )
        

from block import Block

