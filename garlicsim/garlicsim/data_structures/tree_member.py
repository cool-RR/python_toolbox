# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
A module that defines the Node class and the related NodeError exception.

See documentation of Node for more information.
'''

from garlicsim.general_misc.third_party import abc

    
    
class TreeMember(object):
    '''
    
    '''
    __metaclass__ = abc.ABCMeta
  
    @abc.abstractmethod
    def __len__(self):
        raise NotImplementedError

        
    @abc.abstractmethod
    def soft_get_block(self):
        '''
        If this node is a member of a block, return the block.
        
        Otherwise, return the node itself.
        '''
        raise NotImplementedError

    
    @abc.abstractmethod
    def make_containing_path(self):
        '''
        Create a path that contains this node.
        
        There may be multiple different paths that contain this node. This will
        return the one which points to the newest possible forks.
        Returns the path.
        '''
        raise NotImplementedError
        
    
    @abc.abstractmethod
    def all_possible_paths(self):
        '''
        Get a list of all possible paths that contain this node.
        
        Note: There may be paths that contain this node which will not be
        identical to one of the paths given here, because these other paths
        may specify decisions that are not even on the same root as these
        paths.
        '''
        raise NotImplementedError
    
    
    @abc.abstractmethod
    def make_past_path(self):
        '''
        Create a path that contains this node.
        
        There may be multiple different paths that contain this node. This will
        return a path that doesn't specify any decisions after this node.
        '''
        raise NotImplementedError


    @abc.abstractmethod
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
        raise NotImplementedError

    
    @abc.abstractmethod
    def get_ancestor(self, generations=1, round=False):
        ''''''
        raise NotImplementedError

    
    @abc.abstractmethod
    def get_root(self):
        '''
        Get the root of this node.
        
        This means the node which is the parent of the parent of the parent
        of... the parent of this node.
        '''
        raise NotImplementedError
    
    
    @abc.abstractmethod
    def is_overlapping(self, other):
        '''
        Return whether this node overlaps with the given entity.
        
        `other` may be a node, in which case overlapping means being the same
        node. `other` can also be a block, in which case overlapping means this
        node is contained in the block.
        '''
        raise NotImplementedError
    
        



