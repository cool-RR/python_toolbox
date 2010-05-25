# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the TreeMember class.

See its documentation for more information.
'''

from garlicsim.general_misc.third_party import abc
    
    
class TreeMember(object):
    '''
    A member of the tree.
    
    This is an abstract base class for all kinds of objects that are members of
    a tree.
    '''
    __metaclass__ = abc.ABCMeta
  
    @abc.abstractmethod
    def __len__(self):
        '''
        Get the length of the tree member.
        
        For a node or an end, this will be 1. For a block, it will be the number
        of contained nodes.
        '''
        raise NotImplementedError

        
    @abc.abstractmethod
    def soft_get_block(self):
        '''
        Get the block that this tree member is on, or itself if it's a block.
        
        If it's not a part of a block, return itself.
        '''
        raise NotImplementedError

    
    @abc.abstractmethod
    def make_containing_path(self):
        '''
        Create a path that contains this tree member.
        
        There may be multiple different paths that contain this tree member.
        This will return the one which points to the newest possible forks.
        Returns the path.
        '''
        raise NotImplementedError
        
    
    @abc.abstractmethod
    def all_possible_paths(self):
        '''
        Get a list of all possible paths that contain this tree member.
        
        Note: There may be paths that contain this tree member which will not be
        identical to one of the paths given here, because these other paths may
        specify decisions that are not even on the same root as these paths.
        '''
        raise NotImplementedError
    
    
    @abc.abstractmethod
    def make_past_path(self):
        '''
        Create a path that contains this tree member.
        
        There may be multiple different paths that contain this tree member.
        This will return a path that doesn't specify any decisions after this
        tree member.
        '''
        raise NotImplementedError


    @abc.abstractmethod
    def get_all_leaves(self, max_nodes_distance=None, max_clock_distance=None):
        '''
        Get all leaves that are descendents of this tree member.
        
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
        raise NotImplementedError

    
    @abc.abstractmethod
    def get_ancestor(self, generations=1, round=False):
        '''
        Get an ancestor of this tree member.
        
        `generations` specifies the number of generation that the returned
        ancestor should be above the current tree member. `round` determines how
        this method will behave if it was asked for too many generations back,
        and not enough existed. If `round` is True, it will return the root. If
        `round` is False, it will raise a LookupError.
        '''

        raise NotImplementedError

    
    @abc.abstractmethod
    def get_root(self):
        '''
        Get the root of this tree member.
        
        This means the node which is the parent of the parent of the parent
        of... the parent of this tree member.
        '''
        raise NotImplementedError
    
    
    @abc.abstractmethod
    def is_overlapping(self, tree_member):
        '''
        Return whether this tree member overlaps with the given tree member.
        '''
        raise NotImplementedError
    
        



