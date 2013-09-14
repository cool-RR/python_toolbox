# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines the `CrossProcessPersistent` class.

See its documentation for more information.



Note: This module is still experimental.

todo: need to lock library to avoid thread trouble?
'''

import uuid
import weakref

from python_toolbox import caching
from python_toolbox import copy_tools

from .copy_modes import DontCopyPersistent
from .persistent import Persistent
from .personality import Personality


library = weakref.WeakValueDictionary()


class UuidToken(object):
    '''Token which contains a uuid with its attribute `.uuid`'''
    def __init__(self, uuid):
        self.uuid = uuid

        
class CrossProcessPersistent(Persistent):
    '''
    Object that sometimes shouldn't really be duplicated.

    Say some plain object references a `CrossProcessPersistent` object. Then
    that plain object gets deepcopied with the `DontCopyPersistent` copy mode.
    The plain object will get deepcopied, but the `CrossProcessPersistent`
    object under it will not! The new copy of the plain object will refer to
    the same old copy of the `CrossProcessPersistent` object.
    
    This is useful for objects which are read-only and possibly heavy. You may
    use `CrossProcessPersistent` as a base class for these kinds of objects.
    
    Keep in mind that a `CrossProcessPersistent` is read-only. This means that
    starting from the first time that it is copied or put in a queue, it should
    not be changed.

    There is no mechanism that enforces that the user doesn't change the
    object, so the user must remember not to change it.
    
    What this class adds over `Persistent`, is that when a
    `CrossProcessPersistent` is passed around between processes in queues, each
    process retains only one copy of it.
    
    Note: This class is still experimental.
    '''
    
    _is_atomically_pickleable = True
    
    
    def __new__(cls, *args, **kwargs):
        
        # Here we need to check in what context `__new__` was called.
        # There are two options:
        #   1. The object is being created.
        #   2. The object is being unpickled.
        # We check whether we are getting a uuid token. If we are, it's
        # unpickling. If we don't, it's creation.
        
        if len(args) == 1 and (not kwargs) and isinstance(args[0], UuidToken):
            received_uuid = args[0].uuid
        else:
            received_uuid = None
            
        if received_uuid: # The object is being unpickled
            thing = library.get(received_uuid, None)
            if thing:
                thing._CrossProcessPersistent__skip_setstate = True
                return thing
            else: # This object does not exist in our library yet; let's add it
                thing = super(CrossProcessPersistent, cls).__new__(cls)
                thing._CrossProcessPersistent__uuid = received_uuid
                library[received_uuid] = thing
                return thing
                
        else: # The object is being created
            thing = super(CrossProcessPersistent, cls).__new__(cls)
            new_uuid = uuid.uuid4()
            thing._CrossProcessPersistent__uuid = new_uuid
            library[new_uuid] = thing
            return thing

        
    def has_same_uuid_as(self, other):
        '''Does `other` have the same uuid as us?'''
        if not isinstance(other, CrossProcessPersistent):
            return NotImplemented
        return self.__uuid == other.__uuid

    
    def __getstate__(self):
        my_dict = dict(self.__dict__)
        del my_dict['_CrossProcessPersistent__uuid']
        return my_dict

    
    def __getnewargs__(self):
        return (UuidToken(self._CrossProcessPersistent__uuid),)

    
    def __setstate__(self, state):
        if self.__dict__.pop('_CrossProcessPersistent__skip_setstate', None):
            return
        else:
            self.__dict__.update(state)

            
    def __reduce_ex__(self, protocol):
        if protocol < 2:
            raise Exception(
                "You're trying to pickle a `CrossProcessPersistent` object "
                "using protocol %s. You must use protocol 2 or "
                "upwards." % protocol
            )
        else:
            return object.__reduce_ex__(self, protocol)
            
        
    def __deepcopy__(self, memo):
        '''
        Deepcopy the object. If `DontCopyPersistent` is given, only mock-copy.
        
        When this method receieves an instance of `DontCopyPersistent` as a
        memo dictionary, it will not actually `deepcopy` the object but only
        return a reference to the original object.
        '''
        if isinstance(memo, DontCopyPersistent):
            memo[id(self)] = self
            return self
        else:
            new_copy = copy_tools.deepcopy_as_simple_object(self, memo)
            new_copy._Persistent__uuid = uuid.uuid4()
            try:
                del self.personality
            except AttributeError:
                pass
            return new_copy

        
    personality = caching.CachedProperty(
        Personality,
        doc='''Personality containing a human name and two colors.'''
    )



