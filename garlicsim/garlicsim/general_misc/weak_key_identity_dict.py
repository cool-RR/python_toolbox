import weakref


__all__ = ['WeakKeyIdentityDict']


class IdentityRef(weakref.ref):
    
    def __init__(self, *args, **kwargs):
        weakref.ref.__init__(self, *args, **kwargs)
        self._hash = None
        
        
    def __hash__(self):
        if self._hash:
            return self._hash
        thing = self()
        if thing is None:
            raise TypeError("Object was already garbage-collected and you "
                            "didn't hash it while it was alive.")
        else:
            return hash(thing)


class WeakKeyIdentityDict(UserDict.UserDict):
    """ tododoc Mapping class that references keys weakly.

    Entries in the dictionary will be discarded when there is no
    longer a strong reference to the key. This can be used to
    associate additional data with an object owned by other parts of
    an application without adding attributes to those objects. This
    can be especially useful with objects that override attribute
    accesses.
    """

    def __init__(self, dict_=None):
        self.data = {}
        def remove(k, selfref=ref(self)):
            self = selfref()
            if self is not None:
                del self.data[k]
        self._remove = remove
        if dict_ is not None: self.update(dict_)

        
    def __delitem__(self, key):
        del self.data[ref(key)]

        
    def __getitem__(self, key):
        return self.data[ref(key)]

    
    def __repr__(self):
        return "<tododocWeakKeyDictionary at %s>" % id(self)

    
    def __setitem__(self, key, value):
        self.data[ref(key, self._remove)] = value

        
    def copy(self):
        new = WeakKeyDictionary()
        for key, value in self.data.items():
            o = key()
            if o is not None:
                new[o] = value
        return new

    
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
