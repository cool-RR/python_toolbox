from garlicsim.general_misc.weak_key_default_dict import WeakKeyDefaultDict


class EmittingWeakKeyDefaultDict(WeakKeyDefaultDict):
    # tododoc: make __repr__
    def __init__(self, emitter, *args, **kwargs):
        super(EmittingWeakKeyDefaultDict, self).__init__(*args, **kwargs)
        self.emitter = emitter

    def set_emitter(self, emitter):
        self.emitter = emitter
        
    def __setitem__(self, key, value):
        result = \
            super(EmittingWeakKeyDefaultDict, self).__setitem__(key, value)
        if self.emitter:
            self.emitter.emit()
        return result
    
    def __delitem__(self, key):
        result = super(EmittingWeakKeyDefaultDict, self).__delitem__(key)
        if self.emitter:
            self.emitter.emit()
        return result
            
    def pop(self, key, *args):
        result = super(EmittingWeakKeyDefaultDict, self).pop(key, *args)
        if self.emitter:
            self.emitter.emit()
        return result
    
    def popitem(self):
        result = super(EmittingWeakKeyDefaultDict, self).popitem()
        if self.emitter:
            self.emitter.emit()
        return result
    
    def clear(self):
        result = super(EmittingWeakKeyDefaultDict, self).clear()
        if self.emitter:
            self.emitter.emit()
        return result
    
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
            
        return (type(self), parameters, None, None, self.iteritems())