# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the Persistent class.

See its documentation for more information.



Note: This module is still experimental.

todo: need to lock library to avoid thread trouble?

todo: need to raise an exception if we're getting pickled with
an old protocol?

todo: make it polite to other similar classes

todo: what happens when you want to fork-by-editing a state and change
a big 3-d model which is a PRO?
'''


import uuid
import weakref
import colorsys

from copy_modes import DoCopyPersistent, DontCopyPersistent

# Doing `from personality import Personality` at bottom of file

__all__ = ['Persistent']


library = weakref.WeakValueDictionary()


class UuidToken(object):
    '''
    A token which contains a uuid with its attribute .uuid
    '''
    def __init__(self, uuid):
        self.uuid = uuid

class Persistent(object):
    '''
    A class to use as a subclass for objects which do not change. When copying a
    Persistent, it is not really copied; The new "copy" is just the same object.
    When a Persistent is passed around between processes in queues, each process
    retains only one copy of it.
    
    What does it mean that the object is read-only? It means that starting from
    the first time that it is copied or put in a queue, it should not be
    changed.

    There is no mechanism that enforces that the user doesn't change the object.
    
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
                thing._Persistent__skip_setstate = True
                return thing
            else: # This object does not exist in our library yet; Let's add it
                thing = super(Persistent, cls).__new__(cls)
                thing._Persistent__uuid = received_uuid
                library[received_uuid] = thing
                return thing
                
        else: # The object is being created
            thing = super(Persistent, cls).__new__(cls)
            new_uuid = uuid.uuid4()
            thing._Persistent__uuid = new_uuid
            library[new_uuid] = thing
            return thing
    
    def __getstate__(self):
        my_dict = dict(self.__dict__)
        del my_dict["_Persistent__uuid"]
        return my_dict
    
    def __getnewargs__(self):
        return (UuidToken(self._Persistent__uuid),)
    
    def __setstate__(self, state):
        if self.__dict__.pop("_Persistent__skip_setstate", None):
            return
        else:
            self.__dict__.update(state)
    
    def __deepcopy__(self, memo): #todo: supposed to put thing in memo!
        '''tododoc'''
        
        
        if isinstance(memo, DontCopyPersistent):
            tododoc! ! '''how do i make sure it refers to copies of objects?'''
        else:
            tododoc ! !
    
    def __copy__(self):
        return self
    
    def get_personality(self):
        '''
        Get the personality of this persistent object.
        
        See documentation of class garlicsim.misc.persistent.Personality for
        more information.
        '''
        personality_exists = hasattr(self, '_Persistent__personality')
        
        if personality_exists is False:
            self.__personality = Personality(self)
        
        return self.__personality
        


from personality import Personality
