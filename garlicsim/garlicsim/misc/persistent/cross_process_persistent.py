# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the CrossProcessPersistent class.

See its documentation for more information.



Note: This module is still experimental.

todo: need to lock library to avoid thread trouble?
'''


import uuid
import weakref
import colorsys

from copy_modes import DontCopyPersistent
from garlicsim.general_misc import copy_tools

from persistent import Persistent
# Doing `from personality import Personality` at bottom of file


library = weakref.WeakValueDictionary()


class UuidToken(object):
    '''Token which contains a uuid with its attribute `.uuid`'''
    def __init__(self, uuid):
        self.uuid = uuid

class CrossProcessPersistent(Persistent):
    '''
    Object that sometimes shouldn't really be duplicated.

    Say some plain object references a CrossProcessPersistent object. Then that
    plain object gets deepcopied with the DontCopyPersistent copy mode. The
    plain object will get deepcopied, but the CrossProcessPersistent object
    under it will not! The new copy of the plain object will refer to the same
    old copy of the CrossProcessPersistent object.
    
    This is useful for objects which are read-only and possibly heavy. You may
    use Persistent as a base class for these kinds of objects.
    
    When copying a CrossProcessPersistent, it is not really copied; The new
    "copy" is just the same object. 
    
    Keep in mind that a CrossProcessPersistent is read-only. This means that
    starting from the first time that it is copied or put in a queue, it should
    not be changed.

    There is no mechanism that enforces that the user doesn't change the object,
    so the user must remember not to change it.
    
    What this class adds over Persistent, is that when a CrossProcessPersistent
    is passed around between processes in queues, each process retains only one
    copy of it.
    
    Note: This class is still experimental.
    '''
    def __new__(cls, *args, **kwargs):
        
        # Here we need to check in what context __new__ was called.
        # There are two options:
        #     1. The object is being created.
        #     2. The object is being unpickled.
        # We check whether we are getting a uuid token. If we are, it's
        # unpickling. If we don't, it's creation.
        
        if len(args)==1 and len(kwargs)==0 and isinstance(args[0], UuidToken):
            received_uuid = args[0].uuid
        else:
            received_uuid = None
            
        if received_uuid: # The object is being unpickled
            thing = library.pop(received_uuid, None)
            if thing:
                thing._CrossProcessPersistent__skip_setstate = True
                return thing
            else: # This object does not exist in our library yet; Let's add it
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
    
    def __getstate__(self):
        my_dict = dict(self.__dict__)
        del my_dict["_CrossProcessPersistent__uuid"]
        return my_dict
    
    def __getnewargs__(self):
        return (UuidToken(self._CrossProcessPersistent__uuid),)
    
    def __setstate__(self, state):
        if self.__dict__.pop("_CrossProcessPersistent__skip_setstate", None):
            return
        else:
            self.__dict__.update(state)
            
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
            new_copy._Persistent__uuid = uuid.uuid4()
            if hasattr(new_copy, '_CrossProcessPersistent__personality'):
                del new_copy._Persistent__personality
            return new_copy
        
    def get_personality(self):
        '''
        Get the personality of this persistent object.
        
        See documentation of class garlicsim.misc.persistent.Personality for
        more information.
        '''
         # Todo: consider doing __getattr__ thing, maybe `cache`?
        personality_exists = hasattr(self, '_CrossProcessPersistent__personality')
        
        if personality_exists is False:
            self.__personality = Personality(self)
        
        return self.__personality
        


from personality import Personality
