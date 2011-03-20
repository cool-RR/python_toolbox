# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

from garlicsim.general_misc import caching
from garlicsim.general_misc.persistent import CrossProcessPersistent


class HasIdentity(object):
    
    def __init__(self):
        self.__identity = CrossProcessPersistent()

        
    def same_identity(self, other):
        if not isinstance(other, HasIdentity):
            return NotImplemented
        return self.__identity.has_same_uuid_as(other.__identity)
    
    __and__ = same_identity
    
    
    @caching.CachedProperty
    def personality(self):
        '''Personality containing a human name and two colors.'''
        return self.__identity.personality
        
        