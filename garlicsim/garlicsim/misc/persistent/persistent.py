# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the Persistent class.

See its documentation for more information.



Note: This module is still experimental

todo: need to raise an exception if we're getting pickled with
an old protocol?

todo: make it polite to other similar classes
'''


from copy_modes import DontCopyPersistent
from garlicsim.general_misc import copy_tools

__all__ = ['Persistent']

class Persistent(object):
    '''
    Object that sometimes shouldn't really be duplicated.

    Say some plain object references a Persistent object. Then that plain object
    gets deepcopied with the DontCopyPersistent copy mode. The plain object will
    get deepcopied, but the Persistent object under it will not! The new copy of
    the plain object will refer to the same old copy of the Persistent object.
    
    This is useful for objects which are read-only and possibly heavy. You may
    use Persistent as a base class for these kinds of objects.
    
    When copying a Persistent, it is not really copied; The new "copy" is just
    the same object.
    
    Keep in mind that a Persistent is read-only. This means that starting from the
    first time that it is copied or put in a queue, it should not be changed.

    There is no mechanism that enforces that the user doesn't change the object,
    so the user must remember not to change it.
    
    Note: This class is still experimental.
    '''
    
    
    def __deepcopy__(self, memo):
        '''
        Deepcopy the object. If DontCopyPersistent is given, only mock-copy.
        
        When this method receieves an instance of DontCopyPersistent as a memo
        dictionary, it will not actually deepcopy the object but only return a
        reference to the original object.
        '''
        if isinstance(memo, DontCopyPersistent):
            memo[id(self)] = self
            return self
        else:
            new_copy = copy_tools.deepcopy_as_simple_object(self, memo)
            return new_copy
    
        
    def __copy__(self):
        return self
    