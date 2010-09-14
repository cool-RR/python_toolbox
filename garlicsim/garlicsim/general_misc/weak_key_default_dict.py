
from weakref import WeakKeyDictionary

class WeakKeyDefaultDict(WeakKeyDictionary):
    
    def __init__(self, *args, **kwargs):
        self.default_factory = None
        if 'default_factory' in kwargs:
            self.default_factory = kwargs.pop('default_factory')
        elif len(args) > 0 and callable(args[0]):
            self.default_factory = args[0]
            args = args[1:]
        super(WeakKeyDefaultDict, self).__init__(*args, **kwargs)
 
    def __missing__(self, key):
        if self.default_factory is not None:
            self[key] = value = self.default_factory()
            return value
        else: # self.default_factory is None
            raise KeyError(key)

    def __repr__(self, recurse=set()):
        if id(self) in recurse:
            return "WeakKeyDefaultDict(...)"
        try:
            recurse.add(id(self))
            return "WeakKeyDefaultDict(%s, %s)" % (
                repr(self.default_factory),
                super(WeakKeyDefaultDict, self).__repr__()
            )
        finally:
            recurse.remove(id(self))

    def copy(self):
        return type(self)(self, default_factory=self.default_factory)
    
    def __copy__(self):
        return self.copy()

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
        return (type(self), (self.default_factory,), None, None, self.iteritems())
