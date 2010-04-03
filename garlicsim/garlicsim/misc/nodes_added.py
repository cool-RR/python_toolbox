# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the NodesAdded class.

See its documentation for more information.
'''

class NodesAdded(int):
    '''
    sync_crunchers functions return a NodesAdded object instead of an int.
    
    NodesAdded is jsut a subclass of int which has a nice __repr__ saying
    '<7 nodes were added to the tree>' instead of just '7'.
    '''    
    # todo: this class is borderline redundant. Also, I think Maciej said not
    # to subclass builtin types in his pycon talk.
    def __repr__(self):
        return '<' + int.__repr__(self) + ' nodes were added to the tree>'
    
    def __add__(self, other):
        # If it's being added to another NodesAdded, keep it as a NodesAdded
        # object.
        int_result = int.__add__(self, other)
        if isinstance(other, NodesAdded):
            return NodesAdded(int_result)
        else:
            return int_result
        
    __radd__ = __add__
    
    def __sub__(self, other):
        # If it's being substracted with another NodesAdded, keep it as a
        # NodesAdded object.
        int_result = int.__sub__(self, other)
        if isinstance(other, NodesAdded):
            return NodesAdded(int_result)
        else:
            return int_result
        
    __rsub__ = __sub__
    
    def __pos__(self):
        return self
    
    def __neg__(self):
        return NodesAdded(int.__neg__(self))
            