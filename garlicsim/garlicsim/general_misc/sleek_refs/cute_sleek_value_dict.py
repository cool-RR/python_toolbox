import weakref
import UserDict

from garlicsim.general_misc.third_party import inspect

from .sleek_ref import SleekRef
from .exceptions import SleekRefDied


__all__ = ['CuteSleekValueDict']


class CuteSleekValueDict(UserDict.UserDict, object):
    """Mapping class that references values weakly.

    Entries in the dictionary will be discarded when no strong
    reference to the value exists anymore
    """
    # We inherit the constructor without worrying about the input
    # dictionary; since it uses our .update() method, we get the right
    # checks (if the other dictionary is a WeakValueDictionary,
    # objects are unwrapped on the way out, and we always wrap on the
    # way in).

    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        def remove(wr, sleek_ref_to_csvd=weakref.ref(self)):
            csvd = sleek_ref_to_csvd()
            if csvd is not None:
                del csvd.data[wr.key]
                csvd.callback()
        self._remove = remove
        UserDict.UserDict.__init__(self, *args, **kwargs)

        
    def __getitem__(self, key):
        try:            
            return self.data[key]()
        except (KeyError, SleekRefDied):
            missing_method = getattr(type(self), '__missing__', None)
            if missing_method:
                return missing_method(self, key)
            else:
                raise
            
        
    def __contains__(self, key):
        try:
            self.data[key]()
        except (KeyError, SleekRefDied):
            return False
        else:
            return True

    
    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for key, value in self.iteritems():
            if other[key] != value:
                return False
        return True
            
    
    has_key = __contains__

    
    def __repr__(self): # tododoc
        return 'CuteSleekValueDict(%s, %s)' % (
            self.callback,
            dict(self)
        )

    
    def __setitem__(self, key, value):
        self.data[key] = KeyedSleekRef(value, self._remove, key)

        
    def copy(self):
        new_csvd = type(self)(self.callback)
        new_csvd.update(self)
        return new
        
    
    __copy__ = copy
        

    def get(self, key, default=None):
        try:
            return self.data[key]()
        except (KeyError, SleekRefDied):
            return default

            
    def items(self):
        L = []
        for key, wr in self.data.items():
            o = wr()
            if o is not None:
                L.append((key, o))
        return L

    
    def iteritems(self):
        for key, wr in self.data.iteritems():
            value = wr()
            if value is not None:
                yield key, value

                
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

        
    def update(self, *other_dicts, **kwargs):
        d = self.data        
        if other_dicts:
            (other_dict,) = other_dicts        
            if not hasattr(other_dict, 'items'):
                other_dict = type({})(other_dict)
            for key, o in other_dict.items():
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
    
    
    @classmethod
    def fromkeys(cls, iterable, value=None, callback=(lambda: None)):
        d = cls(callback)
        for key in iterable:
            d[key] = value
        return d


class KeyedSleekRef(SleekRef):
    """Specialized reference that includes a key corresponding to the value.

    This is used in the WeakValueDictionary to avoid having to create
    a function object for each key stored in the mapping.  A shared
    callback object can use the 'key' attribute of a KeyedSleekRef instead
    of getting a reference to the key from an enclosing scope.

    """

    def __new__(type, thing, callback, key):
        self = SleekRef.__new__(type)
        return self

    
    def __init__(self, thing, callback, key):
        super(KeyedSleekRef, self).__init__(thing, callback)
        if self.ref:
            self.ref.key = key

