# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import collections
import operator
import functools
import itertools

from python_toolbox import comparison_tools

from .abstract import Ordered, DefinitelyUnordered
from .ordered_dict import OrderedDict



class _AbstractMappingDelegator(collections.abc.Mapping):
    def __init__(self, *args, **kwargs):
        self._dict = self._dict_type(*args, **kwargs)

    __getitem__ = lambda self, key: self._dict[key]
    __len__ = lambda self: len(self._dict)
    __iter__ = lambda self: iter(self._dict)
        
    def copy(self, *args, **kwargs):
        base_dict = self._dict.copy()
        base_dict.update(*args, **kwargs)
        return type(self)(base_dict)

    __repr__ = lambda self: '%s(%s)' % (type(self).__name__,
                                        repr(self._dict) if self._dict else '')
    __reduce__ = lambda self: (self.__class__ , (self._dict,))


class _AbstractFrozenDict(_AbstractMappingDelegator):
    _hash = None # Overridden by instance when calculating hash.
    
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

class _AbstractDoubleSidedDict(collections.abc.Mapping):
    def __init__(self, *args, **kwargs):
        self._dict = self._dict_type(*args, **kwargs)
        self.inverse = 

    
class OrderedDict(collections.OrderedDict):
    '''
    A dictionary with an order.
    
    This is a subclass of `collections.OrderedDict` with a couple of
    improvements.
    '''
    
    def sort(self, key=None, reverse=False):
        '''
        Sort the items according to their keys, changing the order in-place.
        
        The optional `key` argument, (not to be confused with the dictionary
        keys,) will be passed to the `sorted` function as a key function.
        '''
        key_function = \
                   comparison_tools.process_key_function_or_attribute_name(key)
        sorted_keys = sorted(self.keys(), key=key_function, reverse=reverse)
        for key_ in sorted_keys[1:]:
            self.move_to_end(key_)
        
    
    def index(self, key):
        '''Get the index number of `key`.'''
        if key not in self:
            raise ValueError
        for i, key_ in enumerate(self):
            if key_ == key:
                return i
        raise RuntimeError
    
    @property
    def reversed(self):
        '''Get a version of this `OrderedDict` with key order reversed.'''
        return type(self)(reversed(tuple(self.items())))
    


class FrozenDict(DefinitelyUnordered, _AbstractFrozenDict):
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
