# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import collections
import operator
import functools
import itertools

from python_toolbox import comparison_tools

from python_toolbox.nifty_collections.abstract import (Ordered,
                                                       DefinitelyUnordered)
from . import abstract


class FrozenDict(DefinitelyUnordered, abstract.):
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
    
    def __repr__(self):
        if self._dict:
            inner = '[%s]' % ', '.join(
                '(%s, %s)' % item for item in self._dict.items()
            )
        else:
            inner = ''
        return '%s(%s)' % (type(self).__name__, inner)
    
    
        
    
class DoubleSidedFrozenDict:
    1 / 0
    
class DoubleSidedOrderedDict:
    1 / 0
    
class DoubleSidedFrozenOrderedDict:
    1 / 0
