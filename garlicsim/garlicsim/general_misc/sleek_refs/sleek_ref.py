import weakref
import UserDict

from garlicsim.general_misc import cute_inspect

from .exceptions import SleekRefDied


__all__ = ['SleekRef']


class Ref(weakref.ref):
    # To allow data attributes.
    pass


class SleekRef(object):
    def __init__(self, thing, callback=None):
        self.callback = callback
        if callback and not callable(callback):
            raise Exception('%s is not a callable object.' % callback)
        
        self.is_none = (thing is None)
        
        if self.is_none:
            self.ref = self.thing = None
            
        else: # not self.is_none (i.e. thing is not None)
            try:
                self.ref = Ref(thing, callback)
            except TypeError:
                self.ref = None
                self.thing = thing
            else:
                self.thing = None
                
            
    def __call__(self):
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