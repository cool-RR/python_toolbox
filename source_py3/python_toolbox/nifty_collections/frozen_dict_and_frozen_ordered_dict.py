# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import collections
import operator
import functools
import itertools

from .abstract import Ordered, DefinitelyUnordered
from .ordered_dict import OrderedDict


class _AbstractFrozenDict(collections.Mapping):
    is_frozen = True
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

    
class FrozenDict(DefinitelyUnordered, _AbstractFrozenDict):
    '''
    An immutable `dict`.
    
    A `dict` that can't be changed. The advantage of this over `dict` is mainly
    that it's hashable, and thus can be used as a key in dicts and sets.
    
    In other words, `FrozenDict` is to `dict` what `frozenset` is to `set`.
    '''    
    _dict_type = dict
        

class FrozenOrderedDict(Ordered, _AbstractFrozenDict):
    _dict_type = OrderedDict
    
    def __eq__(self, other):
        if isinstance(other, (OrderedDict, FrozenOrderedDict)):
            return collections.Mapping.__eq__(self, other) and \
                                             all(map(operator.eq, self, other))
        return collections.Mapping.__eq__(self, other)
    
    __hash__ = _AbstractFrozenDict.__hash__
    # (Gotta manually carry `__hash__` over from the base class because setting
    # `__eq__` resets it. )

