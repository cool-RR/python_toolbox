import weakref
import UserDict

from garlicsim.general_misc.third_party import inspect


__all__ = ['CuteSleekValueDictionary', 'SleekRef']

class Ref(weakref.ref):
    pass

class SleekRef(object):
    def __init__(self, thing, callback=None):
        self.callback = callback
        if callback and not callable(callback):
            raise Exception('%s is not a callable object.' % callback)
        try:
            self.ref = Ref(thing, callback)
        except TypeError:
            self.ref = None
            self.thing = thing
        else:
            self.thing = None
            
    def __call__(self):
        return self.ref() if self.ref else self.thing


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
        def remove(wr, selfref=weakref.ref(self)):
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

    def __new__(type, ob, callback, key):
        self = SleekRef.__new__(type)
        return self

    def __init__(self, ob, callback, key):
        super(KeyedSleekRef, self).__init__(ob, callback)
        if self.ref:
            self.ref.key = key


    
class SleekCallArgs(object):
    def __init__(self, containing_dict, function, *args, **kwargs):
        
        self.containing_dict = containing_dict
        
        args_spec = inspect.getargspec(function)
        star_args_name, star_kwargs_name = \
                      args_spec.varargs, args_spec.keywords
        
        call_args = inspect.getcallargs(function, *args, **kwargs)
        del args, kwargs
        
        self.star_args_refs = []
        if star_args_name:
            star_args = call_args.pop(star_args_name, None)
            if star_args:
                self.star_args_refs = [SleekRef(star_arg, self.destroy) for
                                       star_arg in star_args]
        
        self.star_kwargs_refs = {}
        if star_kwargs_name:            
            star_kwargs = call_args.pop(star_kwargs_name, {})
            if star_kwargs:
                self.star_kwargs_refs = CuteSleekValueDictionary(self.destroy,
                                                                star_kwargs)
        
        self.args_refs = CuteSleekValueDictionary(self.destroy, call_args)
    
    args = property(lambda self: dict(self.args_refs))
    
    star_args = property(
        lambda self:
            tuple((star_arg_ref() for star_arg_ref in self.star_args_refs))
    )
    
    star_kwargs = property(lambda self: dict(self.star_kwargs_refs))
    
        
    def destroy(self, _=None):
        if self.containing_dict:
            try:
                del self.containing_dict[self]
            except KeyError:
                pass
        
    def __hash__(self):
        return hash(
            (
                tuple(sorted(tuple(self.args))),
                self.star_args,
                tuple(sorted(tuple(self.star_kwargs)))
            )
        )
    
    def __eq__(self, other):
        if not isinstance(other, SleekCallArgs):
            return NotImplemented
        return self.args == other.args and \
               self.star_args == other.star_args and \
               self.star_kwargs == other.star_kwargs