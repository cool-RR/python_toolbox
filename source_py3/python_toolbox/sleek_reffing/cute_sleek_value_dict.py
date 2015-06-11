# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines the `CuteSleekValueDict` class.

See its documentation for more details.
'''

import weakref
import collections

from .sleek_ref import SleekRef
from .exceptions import SleekRefDied


__all__ = ['CuteSleekValueDict']


class CuteSleekValueDict(collections.UserDict):
    """
    A dictionary which sleekrefs its values and propagates their callback.
    
    When a value is garbage-collected, it (1) removes itself from this dict and
    (2) calls the dict's own `callback` function.
    
    This class is like `weakref.WeakValueDictionary`, except (a) it uses
    sleekrefs instead of weakrefs and (b) when a value dies, it calls a
    callback.
    
    See documentation of `python_toolbox.sleek_reffing.SleekRef` for more
    details about sleekreffing.
    """
    
    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        def remove(sleek_ref, weak_ref_to_csvd=weakref.ref(self)):
            csvd = weak_ref_to_csvd()
            if csvd is not None:
                del csvd.data[sleek_ref.key]
                csvd.callback()
        self._remove = remove
        collections.UserDict.__init__(self, *args, **kwargs)

        
    def __getitem__(self, key):
        try:            
            return self.data[key]()
        except (KeyError, SleekRefDied):
            missing_method = getattr(type(self), '__missing__', None)
            if missing_method:
                return missing_method(self, key)
            else:
                raise KeyError(key)
            
        
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
        for key, value in self.items():
            if other[key] != value:
                return False
        return True


    def __ne__(self, other):
        return not self == other
    
    
    has_key = __contains__

    
    def __repr__(self):
        return 'CuteSleekValueDict(%s, %s)' % (
            self.callback,
            dict(self)
        )

    
    def __setitem__(self, key, value):
        self.data[key] = KeyedSleekRef(value, self._remove, key)

        
    def copy(self):
        '''Shallow copy the `CuteSleekValueDict`.'''
        new_csvd = type(self)(self.callback)
        new_csvd.update(self)
        return new_csvd
        
    
    __copy__ = copy
        

    def get(self, key, default=None):
        """ D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None. """
        try:
            return self.data[key]()
        except (KeyError, SleekRefDied):
            return default

            
    def items(self):
        """ D.items() -> list of D's (key, value) pairs, as 2-tuples """
        my_items = []
        for key, sleek_ref in list(self.data.items()):
            try:
                thing = sleek_ref()
            except SleekRefDied:
                pass
            else:
                my_items.append((key, thing))
        return my_items

    
    def iteritems(self):
        """ D.iteritems() -> an iterator over the (key, value) items of D """
        for key, sleek_ref in self.data.items():
            try:
                thing = sleek_ref()
            except SleekRefDied:
                pass
            else:
                yield key, thing

                
    def iterkeys(self):
        """ D.iterkeys() -> an iterator over the keys of D """
        return iter(self.data.keys())

    
    def __iter__(self):
        return iter(self.data.keys())

    
    def itervaluerefs(self):
        """Return an iterator that yields the weak references to the values.

        The references are not guaranteed to be 'live' at the time
        they are used, so the result of calling the references needs
        to be checked before being used.  This can be used to avoid
        creating references that will cause the garbage collector to
        keep the values around longer than needed.

        """
        return iter(self.data.values())

    
    def itervalues(self):
        """ D.itervalues() -> an iterator over the values of D """
        for sleek_ref in self.data.values():
            try:
                yield sleek_ref()
            except SleekRefDied:
                pass

                
    def popitem(self):
        """ D.popitem() -> (k, v), remove and return some (key, value) pair 
        as a 2-tuple; but raise KeyError if D is empty """
        while True:
            key, sleek_ref = self.data.popitem()
            try:
                return key, sleek_ref()
            except SleekRefDied:
                pass

            
    def pop(self, key, *args):
        """ D.pop(k[,d]) -> v, remove specified key and return the 
        corresponding value. If key is not found, d is returned if given,
        otherwise KeyError is raised """
        try:
            return self.data.pop(key)()
        except (KeyError, SleekRefDied):
            if args:
                (default,) = args
                return default
            raise KeyError(key)
        
        
    def setdefault(self, key, default=None):
        """D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D"""
        try:
            return self[key]
        except KeyError:
            self[key] = default
            return default

        
    def update(self, *other_dicts, **kwargs):
        """D.update(E, **F) -> None. Update D from E and F: for k in E: D[k] =
        E[k] (if E has keys else: for (k, v) in E: D[k] = v) then: for k in F:
        D[k] = F[k] """
        if other_dicts:
            (other_dict,) = other_dicts        
            if not hasattr(other_dict, 'items'):
                other_dict = dict(other_dict)
            for key, value in list(other_dict.items()):
                self[key] = value
                
        if kwargs:
            self.update(kwargs)

            
    def valuerefs(self):
        """Return a list of weak references to the values.

        The references are not guaranteed to be 'live' at the time
        they are used, so the result of calling the references needs
        to be checked before being used.  This can be used to avoid
        creating references that will cause the garbage collector to
        keep the values around longer than needed.

        """
        return list(self.data.values())

    
    def values(self):
        """ D.values() -> list of D's values """
        my_values = []
        for sleek_ref in list(self.data.values()):
            try:
                my_values.append(sleek_ref())
            except SleekRefDied:
                pass
        return my_values
    
    
    @classmethod
    def fromkeys(cls, iterable, value=None, callback=(lambda: None)):
        """ dict.fromkeys(S[,v]) -> New csvdict with keys from S and values
        equal to v. v defaults to None. """
        new_csvd = cls(callback)
        for key in iterable:
            new_csvd[key] = value
        return new_csvd


class KeyedSleekRef(SleekRef):
    """Sleekref whose weakref (if one exists) holds reference to a key."""

    def __new__(cls, thing, callback, key):
        self = SleekRef.__new__(cls)
        return self

    
    def __init__(self, thing, callback, key):
        super().__init__(thing, callback)
        if self.ref:
            self.ref.key = key

