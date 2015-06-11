# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines the `EmittingWeakKeyDefaultDict` class.

See its documentation for more details.
'''

from .weak_key_default_dict import WeakKeyDefaultDict


class EmittingWeakKeyDefaultDict(WeakKeyDefaultDict):
    '''
    A key that references keys weakly, has a default factory, and emits.
    
    This is a combination of `weakref.WeakKeyDictionary` and
    `collections.defaultdict`, which emits every time it's modified.
    
    The keys are referenced weakly, so if there are no more references to the
    key, it gets removed from this dict.
    
    If a "default factory" is supplied, when a key is attempted that doesn't
    exist the default factory will be called to create its new value.
    
    Every time that a change is made, like a key is added or removed or gets
    its value changed, we do `.emitter.emit()`.
    '''
    
    def __init__(self, emitter, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.emitter = emitter

        
    def set_emitter(self, emitter):
        '''Set the emitter that will be emitted every time a change is made.'''
        self.emitter = emitter

        
    def __setitem__(self, key, value):
        result = super().__setitem__(key, value)
        if self.emitter:
            self.emitter.emit()
        return result

    
    def __delitem__(self, key):
        result = super().__delitem__(key)
        if self.emitter:
            self.emitter.emit()
        return result

    
    def pop(self, key, *args):
        """ D.pop(k[,d]) -> v, remove specified key and return the 
        corresponding value. If key is not found, d is returned if given,
        otherwise KeyError is raised """
        result = super().pop(key, *args)
        if self.emitter:
            self.emitter.emit()
        return result

    
    def popitem(self):
        """ D.popitem() -> (k, v), remove and return some (key, value) 
        pair as a 2-tuple; but raise KeyError if D is empty """
        result = super().popitem()
        if self.emitter:
            self.emitter.emit()
        return result

    
    def clear(self):
        """ D.clear() -> None.  Remove all items from D. """
        result = super().clear()
        if self.emitter:
            self.emitter.emit()
        return result

    
    def __repr__(self):
        return '%s(%s, %s, %s)' % (
            type(self).__name__,
            self.emitter,
            self.default_factory,
            dict(self)
        )

    
    def __reduce__(self):
        """
        __reduce__ must return a 5-tuple as follows:

           - factory function
           - tuple of args for the factory function
           - additional state (here None)
           - sequence iterator (here None)
           - dictionary iterator (yielding successive (key, value) pairs

           This API is used by pickle.py and copy.py.
        """
        if self.default_factory:
            parameters = (self.emitter, self.default_factory)
        else: # not self.default_factory
            parameters = (self.emitter)
            
        return (type(self), parameters, None, None, iter(self.items()))