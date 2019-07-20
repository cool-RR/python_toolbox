# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import collections
import operator
import functools
import itertools

from .abstract import Ordered
from .ordered_dict import OrderedDict


class _AbstractFrozenDict(collections.abc.Mapping):
    _hash = None # Overridden by instance when calculating hash.

    def __init__(self, *args, **kwargs):
        self._dict = self._dict_type(*args, **kwargs)

    __getitem__ = lambda self, key: self._dict[key]
    __len__ = lambda self: len(self._dict)
    __iter__ = lambda self: iter(self._dict)

    def copy(self, *args, **kwargs):
        base_dict = self._dict.copy()
        base_dict.update(*args, **kwargs)
        return type(self)(base_dict)

    def __hash__(self):
        if self._hash is None:
            self._hash = functools.reduce(
                operator.xor,
                map(
                    hash,
                    itertools.chain(
                        (h for h in self.items()),
                        (type(self), len(self))
                    )
                ),
                0
            )

        return self._hash

    __repr__ = lambda self: '%s(%s)' % (type(self).__name__,
                                        repr(self._dict))
    __reduce__ = lambda self: (self.__class__ , (self._dict,))


class FrozenDict(_AbstractFrozenDict):
    '''
    An immutable `dict`.

    A `dict` that can't be changed. The advantage of this over `dict` is mainly
    that it's hashable, and thus can be used as a key in dicts and sets.

    In other words, `FrozenDict` is to `dict` what `frozenset` is to `set`.
    '''
    _dict_type = dict


class FrozenOrderedDict(Ordered, _AbstractFrozenDict):
    '''
    An immutable, ordered `dict`.

    A `dict` that is ordered and can't be changed. The advantage of this over
    `OrderedDict` is mainly that it's hashable, and thus can be used as a key
    in dicts and sets.
    '''
    _dict_type = OrderedDict

    def __eq__(self, other):
        if isinstance(other, (OrderedDict, FrozenOrderedDict)):
            return collections.abc.Mapping.__eq__(self, other) and \
                                             all(map(operator.eq, self, other))
        return collections.abc.Mapping.__eq__(self, other)

    __hash__ = _AbstractFrozenDict.__hash__
    # (Gotta manually carry `__hash__` over from the base class because setting
    # `__eq__` resets it. )


    # Poor man's caching because we can't import `CachedProperty` due to import
    # loop:
    _reversed = None
    @property
    def reversed(self):
        '''
        Get a version of this `FrozenOrderedDict` with key order reversed.
        '''
        if self._reversed is None:
            self._reversed = type(self)(reversed(tuple(self.items())))
        return self._reversed