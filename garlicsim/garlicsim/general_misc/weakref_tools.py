from weakref import (getweakrefcount, getweakrefs, ref, proxy,
                     CallableProxyType, ProxyType, ReferenceType)
from garlicsim.general_misc.sleek_ref import SleekRef
import UserDict

__all__ = ['CuteSleekValueDictionary']

class CuteSleekValueDictionary(UserDict.UserDict):
    """Mapping class that references values weakly.

    Entries in the dictionary will be discarded when no strong
    reference to the value exists anymore
    """
    # We inherit the constructor without worrying about the input
    # dictionary; since it uses our .update() method, we get the right
    # checks (if the other dictionary is a WeakValueDictionary,
    # objects are unwrapped on the way out, and we always wrap on the
    # way in).

    def __init__(self, callback, *args, **kw):
        self.callback = callback
        def remove(wr, selfref=ref(self)):
            self = selfref()
            if self is not None:
                del self.data[wr.key]
                self.callback()
        self._remove = remove
        UserDict.UserDict.__init__(self, *args, **kw)

    def __getitem__(self, key):
        o = self.data[key]()
        if o is None:
            raise KeyError, key
        else:
            return o

    def __contains__(self, key):
        try:
            o = self.data[key]()
        except KeyError:
            return False
        return o is not None

    def has_key(self, key):
        try:
            o = self.data[key]()
        except KeyError:
            return False
        return o is not None

    def __repr__(self): # tododoc
        return "<WeakValueDictionary at %s>" % id(self)

    def __setitem__(self, key, value):
        self.data[key] = KeyedSleekRef(value, self._remove, key)

    '''def copy(self):
        new = WeakValueDictionary()
        for key, wr in self.data.items():
            o = wr()
            if o is not None:
                new[key] = o
        return new''' # tododoc

    def get(self, key, default=None):
        try:
            wr = self.data[key]
        except KeyError:
            return default
        else:
            o = wr()
            if o is None:
                # This should only happen
                return default
            else:
                return o

    def items(self):
        L = []
        for key, wr in self.data.items():
            o = wr()
            if o is not None:
                L.append((key, o))
        return L

    def iteritems(self):
        for wr in self.data.itervalues():
            value = wr()
            if value is not None:
                yield wr.key, value

    def iterkeys(self):
        return self.data.iterkeys()

    def __iter__(self):
        return self.data.iterkeys()

    def itervaluerefs(self):
        """Return an iterator that yields the weak references to the values.

        The references are not guaranteed to be 'live' at the time
        they are used, so the result of calling the references needs
        to be checked before being used.  This can be used to avoid
        creating references that will cause the garbage collector to
        keep the values around longer than needed.

        """
        return self.data.itervalues()

    def itervalues(self):
        for wr in self.data.itervalues():
            obj = wr()
            if obj is not None:
                yield obj

    def popitem(self):
        while 1:
            key, wr = self.data.popitem()
            o = wr()
            if o is not None:
                return key, o

    def pop(self, key, *args):
        try:
            o = self.data.pop(key)()
        except KeyError:
            if args:
                return args[0]
            raise
        if o is None:
            raise KeyError, key
        else:
            return o

    def setdefault(self, key, default=None):
        try:
            wr = self.data[key]
        except KeyError:
            self.data[key] = KeyedSleekRef(default, self._remove, key)
            return default
        else:
            return wr()

    def update(self, dict=None, **kwargs):
        d = self.data
        if dict is not None:
            if not hasattr(dict, "items"):
                dict = type({})(dict)
            for key, o in dict.items():
                d[key] = KeyedSleekRef(o, self._remove, key)
        if len(kwargs):
            self.update(kwargs)

    def valuerefs(self):
        """Return a list of weak references to the values.

        The references are not guaranteed to be 'live' at the time
        they are used, so the result of calling the references needs
        to be checked before being used.  This can be used to avoid
        creating references that will cause the garbage collector to
        keep the values around longer than needed.

        """
        return self.data.values()

    def values(self):
        L = []
        for wr in self.data.values():
            o = wr()
            if o is not None:
                L.append(o)
        return L


class KeyedSleekRef(SleekRef):
    """Specialized reference that includes a key corresponding to the value.

    This is used in the WeakValueDictionary to avoid having to create
    a function object for each key stored in the mapping.  A shared
    callback object can use the 'key' attribute of a KeyedSleekRef instead
    of getting a reference to the key from an enclosing scope.

    """

    __slots__ = "key",

    def __new__(type, ob, callback, key):
        self = SleekRef.__new__(type, ob, callback)
        self.key = key
        return self

    def __init__(self, ob, callback, key):
        super(KeyedSleekRef, self).__init__(ob, callback)