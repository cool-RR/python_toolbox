# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

import collections
import operator
import functools


class FrozenDict(collections.Mapping):
    '''
    An immutable `dict`.
    
    A `dict` that can't be changed. The advantage of this over `dict` is mainly
    that it's hashable, and thus can be used as a key in dicts and sets.
    
    In other words, `FrozenDict` is to `dict` what `frozenset` is to `set`.
    '''
    
    _hash = None # Overridden by instance when calculating hash.

    def __init__(self, *args, **kwargs):
        self._dict = dict(*args, **kwargs)

    __getitem__ = lambda self, key: self._dict[key]
    __len__ = lambda self: len(self._dict)
    __iter__ = lambda self: iter(self._dict)

    def copy(self, *args, **kwargs):
        base_dict = self._dict.copy()
        base_dict.update(*args, **kwargs)
        return type(self)(base_dict)
    
    def __hash__(self):
        if self._hash is None:
            self._hash = functools.reduce(operator.xor,
                                          map(hash, self.items()),
                                          0) ^ hash(len(self))

        return self._hash
    
    __repr__ = lambda self: '%s(%s)' % (type(self).__name__,
                                        repr(self._dict))
    __reduce__ = lambda self: (self.__class__, self._dict)

    