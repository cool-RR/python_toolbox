# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import collections
import operator
import functools
import itertools

from python_toolbox import comparison_tools

from .ordered_dict import OrderedDict
from . import abstract


class DoubleDict(abstract._UnorderedDictDelegator,
                 abstract._AbstractMutableDoubleDict):
    '''
    blocktododoc'''    
    
    
class FrozenDict(abstract._UnorderedDictDelegator,
                 abstract._AbstractFrozenDict):
    '''
    An immutable `dict`.
    
    A `dict` that can't be changed. The advantage of this over `dict` is mainly
    that it's hashable, and thus can be used as a key in dicts and sets.
    
    In other words, `FrozenDict` is to `dict` what `frozenset` is to `set`.
    '''    
    

class DoubleFrozenDict(abstract._UnorderedDictDelegator,
                       abstract.BaseDoubleDict,
                       abstract._AbstractFrozenDict):
    '''blocktododoc'''
    

class DoubleOrderedDict(abstract._OrderedDictDelegator,
                        abstract._AbstractMutableDoubleDict,
                        abstract._AbstractFrozenDict):
    '''blocktododoc'''
    
            
    def move_to_end(self, key, last=True):
        '''
        Move an existing element to the end (or beginning if `last is False`.)

        Raises `KeyError` if the element does not exist.
        
        When `last is True`, acts like a fast version of `self[key] =
        self.pop(key)`.
        '''
        self._assert_valid()
        value = self._dict[key] # Propagate `KeyError`.
        self._dict.move_to_end(key, last=last)    
        self.inverse._dict.move_to_end(value, last=last)
        self._assert_valid()
    

class FrozenOrderedDict(abstract._OrderedDictDelegator,
                        abstract._AbstractFrozenDict):
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
    
    __hash__ = abstract._AbstractFrozenDict.__hash__
    # (Gotta manually carry `__hash__` over from the base class because setting
    # `__eq__` resets it. )

    
    # Poor man's caching because we can't import `CachedProperty` due to import
    # loop:
    _reversed = None
    def __reversed__(self):
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
    
    
    
class DoubleFrozenOrderedDict(abstract._OrderedDictDelegator,
                              abstract.BaseDoubleDict,
                              abstract._AbstractFrozenDict):
    '''blocktododoc'''
    
    
# blocktodo: Do sophisticated tests that iterate over the dict classes, see
# their attributes (defined in the tests) and do the appropriate tests. For
# example if a dict is ordered and mutable, we should test .sort and
# .move_to_end, otherwise we should test these methods don't exist.
