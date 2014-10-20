# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines the `SleekRef` class.

See its documentation for more info.
'''

import weakref

from python_toolbox import cute_inspect

from .exceptions import SleekRefDied


__all__ = ['SleekRef']


class Ref(weakref.ref):
    '''
    A weakref.
    
    What this adds over `weakref.ref` is the ability to add custom attributes.
    '''


class SleekRef(object):
    '''
    Sleekref tries to reference an object weakly but if can't does it strongly.
    
    The problem with weakrefs is that some objects can't be weakreffed, for
    example `list` and `dict` objects. A sleekref tries to create a weakref to
    an object, but if it can't (like for a `list`) it creates a strong one
    instead.
    
    Thanks to sleekreffing you can avoid memory leaks when manipulating
    weakreffable object, but if you ever want to use non-weakreffable objects
    you are still able to. (Assuming you don't mind the memory leaks or stop
    them some other way.)
    
    When you call a dead sleekref, it doesn't return `None` like weakref; it
    raises `SleekRefDied`. Therefore, unlike weakref, you can store `None` in a
    sleekref.
    '''
    def __init__(self, thing, callback=None):
        '''
        Construct the sleekref.
        
        `thing` is the object we want to sleekref. `callback` is the callable
        to call when the weakref to the object dies. (Only relevant for
        weakreffable objects.)
        '''
        self.callback = callback
        if callback and not callable(callback):
            raise TypeError('%s is not a callable object.' % callback)
        
        self.is_none = (thing is None)
        '''Flag saying whether `thing` is `None`.'''
        
        if self.is_none:
            self.ref = self.thing = None
            
        else: # not self.is_none (i.e. thing is not None)
            try:
                self.ref = Ref(thing, callback)
                '''The weak reference to the object. (Or `None`.)'''
            except TypeError:
                self.ref = None
                self.thing = thing
                '''The object, if non-weakreffable.'''
            else:
                self.thing = None
                
            
    def __call__(self):
        '''
        Obtain the sleekreffed object. Raises `SleekRefDied` if reference died.
        '''
        if self.ref:
            result = self.ref()
            if result is None:
                raise SleekRefDied
            else:
                return result
        elif self.thing is not None:
            return self.thing
        else:
            assert self.is_none
            return None