import UserDict
from weakref import ref

class WeakKeyDefaultDict(UserDict.UserDict, object): #todo: needs testing
    
    def __init__(self, *args, **kwargs):
        self.default_factory = None
        if 'default_factory' in kwargs:
            self.default_factory = kwargs.pop('default_factory')
        elif len(args) > 0 and callable(args[0]):
            self.default_factory = args[0]
            args = args[1:]
        
        self.data = {}
        def remove(k, selfref=ref(self)):
            self = selfref()
            if self is not None:
                del self.data[k]
        self._remove = remove
        if args:
            self.update(args[0])

            
    def __missing__(self, key):
        if self.default_factory is not None:
            self[key] = value = self.default_factory()
            return value
        else: # self.default_factory is None
            raise KeyError(key)

        
    def __repr__(self, recurse=set()):
        type_name = type(self).__name__
        if id(self) in recurse:
            return "%s(...)" % type_name
        try:
            recurse.add(id(self))
            return "%s(%s, %s)" % (
                type_name,
                repr(self.default_factory),
                super(WeakKeyDefaultDict, self).__repr__()
            )
        finally:
            recurse.remove(id(self))

            
    def copy(self): # todo: needs testing
        return type(self)(self, default_factory=self.default_factory)
    
    __copy__ = copy

    
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

    
    def __delitem__(self, key):
        del self.data[ref(key)]

        
    def __getitem__(self, key):
        try:
            return self.data[ref(key)]
        except KeyError:
            missing_method = getattr(type(self), '__missing__', None)
            if missing_method:
                return missing_method(self, key)
            else:
                raise

            
    def __setitem__(self, key, value):
        self.data[ref(key, self._remove)] = value

        
    def get(self, key, default=None):
        return self.data.get(ref(key),default)

    
    def has_key(self, key):
        try:
            wr = ref(key)
        except TypeError:
            return 0
        return wr in self.data

    
    def __contains__(self, key):
        try:
            wr = ref(key)
        except TypeError:
            return 0
        return wr in self.data

    
    def items(self):
        L = []
        for key, value in self.data.items():
            o = key()
            if o is not None:
                L.append((o, value))
        return L

    
    def iteritems(self):
        for wr, value in self.data.iteritems():
            key = wr()
            if key is not None:
                yield key, value

                
    def iterkeyrefs(self):
        """Return an iterator that yields the weak references to the keys.

        The references are not guaranteed to be 'live' at the time
        they are used, so the result of calling the references needs
        to be checked before being used.  This can be used to avoid
        creating references that will cause the garbage collector to
        keep the keys around longer than needed.

        """
        return self.data.iterkeys()

    def iterkeys(self):
        for wr in self.data.iterkeys():
            obj = wr()
            if obj is not None:
                yield obj

    def __iter__(self):
        return self.iterkeys()

    
    def itervalues(self):
        return self.data.itervalues()

    
    def keyrefs(self):
        """Return a list of weak references to the keys.

        The references are not guaranteed to be 'live' at the time
        they are used, so the result of calling the references needs
        to be checked before being used.  This can be used to avoid
        creating references that will cause the garbage collector to
        keep the keys around longer than needed.

        """
        return self.data.keys()

    
    def keys(self):
        L = []
        for wr in self.data.keys():
            o = wr()
            if o is not None:
                L.append(o)
        return L

    
    def popitem(self):
        while 1:
            key, value = self.data.popitem()
            o = key()
            if o is not None:
                return o, value

            
    def pop(self, key, *args):
        return self.data.pop(ref(key), *args)

    
    def setdefault(self, key, default=None):
        return self.data.setdefault(ref(key, self._remove),default)

    
    def update(self, dict=None, **kwargs):
        d = self.data
        if dict is not None:
            if not hasattr(dict, "items"):
                dict = type({})(dict)
            for key, value in dict.items():
                d[ref(key, self._remove)] = value
        if len(kwargs):
            self.update(kwargs)
            
            