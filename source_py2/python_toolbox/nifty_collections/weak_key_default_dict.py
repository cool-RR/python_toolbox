# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines the `WeakKeyDefaultDict` class.

See its documentation for more details.
'''
# todo: revamp

import collections
import UserDict
from weakref import ref


#todo: needs testing
class WeakKeyDefaultDict(UserDict.UserDict, object):
    '''
    A weak key dictionary which can use a default factory.
    
    This is a combination of `weakref.WeakKeyDictionary` and
    `collections.defaultdict`.
    
    The keys are referenced weakly, so if there are no more references to the
    key, it gets removed from this dict.
    
    If a "default factory" is supplied, when a key is attempted that doesn't
    exist the default factory will be called to create its new value.
    '''
    
    def __init__(self, *args, **kwargs):
        '''
        Construct the `WeakKeyDefaultDict`.
        
        You may supply a `default_factory` as a keyword argument.
        '''
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
        '''Get a value for a key which isn't currently registered.'''
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
        return (type(self), (self.default_factory,), None, None,
                self.iteritems())

    
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

    
    def __contains__(self, key):
        try:
            wr = ref(key)
        except TypeError:
            return 0
        return wr in self.data


    has_key = __contains__

    
    def items(self):
        """ D.items() -> list of D's (key, value) pairs, as 2-tuples """
        L = []
        for key, value in self.data.items():
            o = key()
            if o is not None:
                L.append((o, value))
        return L

    
    def iteritems(self):
        """ D.iteritems() -> an iterator over the (key, value) items of D """
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
        """ D.iterkeys() -> an iterator over the keys of D """
        for wr in self.data.iterkeys():
            obj = wr()
            if obj is not None:
                yield obj

                
    def __iter__(self):
        return self.iterkeys()

    
    def itervalues(self):
        """ D.itervalues() -> an iterator over the values of D """
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
        """ D.keys() -> list of D's keys """
        L = []
        for wr in self.data.keys():
            o = wr()
            if o is not None:
                L.append(o)
        return L

    
    def popitem(self):
        """ D.popitem() -> (k, v), remove and return some (key, value) pair 
        as a 2-tuple; but raise KeyError if D is empty """
        while 1:
            key, value = self.data.popitem()
            o = key()
            if o is not None:
                return o, value

            
    def pop(self, key, *args):
        """ D.pop(k[,d]) -> v, remove specified key and return the 
        corresponding value. If key is not found, d is returned if given,
        otherwise KeyError is raised """
        return self.data.pop(ref(key), *args)

    
    def setdefault(self, key, default=None):
        """D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D"""
        return self.data.setdefault(ref(key, self._remove),default)

    
    def update(self, dict=None, **kwargs):
        """D.update(E, **F) -> None. Update D from E and F: for k in E: D[k] =
        E[k] (if E has keys else: for (k, v) in E: D[k] = v) then: for k in F:
        D[k] = F[k] """
        
        d = self.data
        if dict is not None:
            if not hasattr(dict, "items"):
                dict = type({})(dict)
            for key, value in dict.items():
                d[ref(key, self._remove)] = value
        if len(kwargs):
            self.update(kwargs)
            
            
    def __len__(self):
        return len(self.data)
              