# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

import operator
import heapq
import itertools
import numbers
import collections
import functools
import copy

from python_toolbox import math_tools

from .lazy_tuple import LazyTuple
from .ordered_dict import OrderedDict
from .ordered_set import OrderedSet
from .frozen_dict_and_frozen_ordered_dict import FrozenDict, FrozenOrderedDict
from .abstract import Ordered, DefinitelyUnordered

try:                                    # Load C helper function if available
    from _collections import _count_elements
except ImportError:
    def _count_elements(mapping, iterable):
        '''Bag elements from the iterable.'''
        mapping_get = mapping.get
        for element in iterable:
            mapping[element] = mapping_get(element, 0) + 1
            
            
class _NO_DEFAULT: 
    pass
            
class _ZeroCountAttempted(Exception):
    pass
        

def _process_count(count):
    if not math_tools.is_integer(count):
        raise TypeError(
            'You passed %s as a count, while a `Bag` can only handle integer '
            'counts.' % count
        )
    if count < 0:
        raise TypeError(
            "You passed %s as a count, while `Bag` doesn't support negative "
            "amounts." % count
        )
    
    if count == 0:
        raise _ZeroCountAttempted
    
    return int(count)
    
    

class _BaseBagMixin:
    '''Mixin for `FrozenBag` and `FrozenOrderedBag`.'''
    
    def __init__(self, iterable={}):
        from python_toolbox import math_tools
        
        super().__init__()
        
        if isinstance(iterable, collections.Mapping):
            for key, value, in iterable.items():
                try:
                    self._dict[key] = _process_count(value)
                except _ZeroCountAttempted:
                    continue
        else:
            _count_elements(self._dict, iterable)


    __getitem__ = lambda self, key: self._dict.get(key, 0)

    def most_common(self, n=None):
        '''
        List the `n` most common elements and their counts, sorted.
        
        Results are sorted from the most common to the least. If `n is None`,
        then list all element counts.

            >>> FrozenBag('abcdeabcdabcaba').most_common(3)
            [('a', 5), ('b', 4), ('c', 3)]

        '''
        # Emulate Bag.sortedByCount from Smalltalk
        if n is None:
            return sorted(self.items(), key=operator.itemgetter(1),
                          reverse=True)
        return heapq.nlargest(n, self.items(),
                               key=operator.itemgetter(1))

    def elements(self):
        '''
        Iterate over elements repeating each as many times as its count.

            >>> c = FrozenBag('ABCABC')
            >>> sorted(c.elements())
            ['A', 'A', 'B', 'B', 'C', 'C']
    
            # Knuth's example for prime factors of 1836:  2**2 * 3**3 * 17**1
            >>> prime_factors = FrozenBag({2: 2, 3: 3, 17: 1})
            >>> product = 1
            >>> for factor in prime_factors.elements():     # loop over factors
            ...     product *= factor                       # and multiply them
            >>> product
            1836

        Note, if an element's count has been set to zero or is a negative
        number, `.elements()` will ignore it.
        '''
        # Emulate Bag.do from Smalltalk and Multiset.begin from C++.
        return itertools.chain.from_iterable(
            itertools.starmap(itertools.repeat, self.items())
        )
    
    def __contains__(self, item):
        return (self[item] >= 1)
    
    def __or__(self, other):
        '''
        Get the maximum of value in either of the input bags.

            >>> FrozenBag('abbb') | FrozenBag('bcc')
            FrozenBag({'b': 3, 'c': 2, 'a': 1})
            
        '''
        if not isinstance(other, _BaseBagMixin):
            return NotImplemented
        return type(self)(self._dict_type(
            (key, max(self[key], other[key]))
            for key in OrderedSet(self) | OrderedSet(other))
        )
    
    def __and__(self, other):
        '''

        Get the minimum of corresponding counts.
            >>> FrozenBag('abbb') & FrozenBag('bcc')
            FrozenBag({'b': 1})
            
        '''
        if not isinstance(other, _BaseBagMixin):
            return NotImplemented
        return type(self)(self._dict_type(
            (key, min(self[key], other[key]))
            for key in OrderedSet(self) & OrderedSet(other))
        )


    def __add__(self, other):
        if not isinstance(other, _BaseBagMixin):
            return NotImplemented
        return type(self)(self._dict_type(
            (key, self[key] + other[key])
            for key in OrderedSet(self) & OrderedSet(other))
        )

    def __sub__(self, other):
        '''
        blocktododoc
        Negative counts are truncated to zero.        
        '''
        if not isinstance(other, _BaseBagMixin):
            return NotImplemented
        return type(self)(self._dict_type(
            (key, max(self[key] - other[key], 0)) for key in self)
        )

    def __mul__(self, other):
        if not math_tools.is_integer(other):
            return NotImplemented
        return type(self)(self._dict_type((key, count * other) for
                                          key, count in self.items()))
    def __floordiv__(self, other):
        if math_tools.is_integer(other):
            return (
                type(self)(self._dict_type((key, count // other) for
                                           key, count in self.items()))
            )
        elif isinstance(other, _BaseBagMixin):
            for key in other:
                if key not in self:
                    assert other[key] >= 1
                    return 0
            division_results = []
            for key in self:
                if other[key] >= 1:
                    division_results.append(self[key] // other[key])
            if division_results:
                return min(division_results)
            else:
                raise ZeroDivisionError
        else:
            return NotImplemented
        
    def __mod__(self, other):
        if math_tools.is_integer(other):
            return (
                type(self)(self._dict_type((key, count % other) for
                                           key, count in self.items()))
            )
        elif isinstance(other, _BaseBagMixin):
            return divmod(self, other)[1]
        else:
            return NotImplemented
        
    def __divmod__(self, other):
        if math_tools.is_integer(other):
            return (
                type(self)(self._dict_type((key, count // other) for
                                           key, count in self.items())), 
                type(self)(self._dict_type((key, count % other) for
                                           key, count in self.items())), 
            )
        elif isinstance(other, _BaseBagMixin):
            
            floordiv_result = self // other
            mod_result = type(self)(
                self._dict_type((key, count - other[key] * floordiv_result) for
                                key, count in self.items())
            )
            return (floordiv_result, mod_result)
            
        else:
            return NotImplemented

    def __pow__(self, other, modulo=None):
        if not math_tools.is_integer(other):
            return NotImplemented
        if modulo is None:
            return type(self)(self._dict_type((key, count ** other) for
                                              key, count in self.items()))
        else:
            return type(self)(self._dict_type(
                (key, pow(count, other, modulo)) for
                key, count in self.items())
            )

    __bool__ = lambda self: any(True for element in self.elements())
    
    
    _n_elements = None
    @property
    def n_elements(self):
        # Implemented as a poor man's `CachedProperty` because we can't use the
        # real `CachedProperty` due to circular import.
        if self._n_elements is None:
            self._n_elements = sum(self.values())
        return self._n_elements
    _n_elements = None
    
    
    _frozen_bag_bag = None
    @property
    def frozen_bag_bag(self):
        # Implemented as a poor man's `CachedProperty` because we can't use the
        # real `CachedProperty` due to circular import.
        from .frozen_bag_bag import FrozenBagBag
        if self._frozen_bag_bag is None:
            self._frozen_bag_bag = FrozenBagBag(self.values())
        return self._frozen_bag_bag
        
    
    # We define all the comparison methods manually instead of using
    # `total_ordering` because `total_ordering` assumes that >= means (> and
    # ==) while we, in `FrozenOrderedBag`, don't have that hold because ==
    # takes the items' order into account.
    
    def __lt__(self, other):
        if not isinstance(other, _BaseBagMixin):
            return NotImplemented
        found_strict_difference = False # Until challenged.
        for element, count in self.items():
            try:
                other_count = other[element]
            except KeyError:
                return False
            if not (count <= other_count):
                return False
            elif count < other_count:
                found_strict_difference = True
        return found_strict_difference
    
    def __le__(self, other):
        if not isinstance(other, _BaseBagMixin):
            return NotImplemented
        for element, count in self.items():
            try:
                other_count = other[element]
            except KeyError:
                return False
            if not (count <= other_count):
                return False
        return True
    
    def __gt__(self, other):
        if not isinstance(other, _BaseBagMixin):
            return NotImplemented
        found_strict_difference = False # Until challenged.
        for element, count in self.items():
            try:
                other_count = other[element]
            except KeyError:
                continue
            if not (count >= other_count):
                return False
            elif count > other_count:
                found_strict_difference = True
        return found_strict_difference
    
    def __ge__(self, other):
        if not isinstance(other, _BaseBagMixin):
            return NotImplemented
        for element, count in self.items():
            try:
                other_count = other[element]
            except KeyError:
                continue
            if not (count >= other_count):
                return False
        return True
            
    def __repr__(self):
        # Overridden in `_OrderedBagMixin`.
        if not self:
            return '%s()' % type(self).__name__
        return '%s(%s)' % (
            type(self).__name__,
            self._dict if self._dict else ''
        )

    __deepcopy__ = lambda self, memo: type(self)(
                                               copy.deepcopy(self._dict, memo))
    
    def __reversed__(self):
        # Gets overridden in `_OrderedBagMixin`.
        raise TypeError("Can't reverse an unordered bag.")
        
        

class _MutableBagMixin(_BaseBagMixin):
    def __setitem__(self, i, count):
        try:
            super().__setitem__(i, _process_count(count))
        except _ZeroCountAttempted:
            del self[i]
        
    
    
    def setdefault(self, key, default):
        current_count = self[key]
        if current_count > 0:
            return current_count
        else:
            self[key] = default
            return default

    def __delitem__(self, key):
        # We're making `__delitem__` not raise an exception on missing or
        # zero-count elements because we're automatically deleting zero-count
        # elements even though they seem to exist from the outside, so we're
        # avoiding raising exceptions where someone would try to explicitly
        # delete them.
        try:
            del self._dict[key]
        except KeyError:
            pass
        
    def pop(self, key, default=_NO_DEFAULT):
        '''D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
          If key is not found, d is returned if given, otherwise KeyError is raised.
        '''
        value = self[key]
        if value == 0 and default is not _NO_DEFAULT:
            return default
        else:
            del self[key]
            return value

    def __ior__(self, other):
        '''
        Get the maximum of value in either of the input bags.

            >>> FrozenBag('abbb') | FrozenBag('bcc')
            FrozenBag({'b': 3, 'c': 2, 'a': 1})
            
        '''
        if not isinstance(other, _BaseBagMixin):
            return NotImplemented
        for key, other_count in tuple(other.items()):
            self[key] = max(self[key], other_count)
        return self
            
    
    def __iand__(self, other):
        '''

        Get the minimum of corresponding counts.
            >>> FrozenBag('abbb') & FrozenBag('bcc')
            FrozenBag({'b': 1})
            
        '''
        if not isinstance(other, _BaseBagMixin):
            return NotImplemented
        for key, count in tuple(self.items()):
            self[key] = min(count, other[key])
        return self
            

    def __iadd__(self, other):
        if not isinstance(other, _BaseBagMixin):
            return NotImplemented
        for key, other_count in tuple(other.items()):
            self[key] += other_count
        return self
            

    def __isub__(self, other):
        '''
        blocktododoc
        Negative counts are truncated to zero.        
        '''
        if not isinstance(other, _BaseBagMixin):
            return NotImplemented
        for key, other_count in tuple(other.items()):
            self[key] = max(self[key] - other_count, 0)
        return self


    def __imul__(self, other):
        if not math_tools.is_integer(other):
            return NotImplemented
        for key in tuple(self):
            self[key] *= other
        return self
            
            
    def __ifloordiv__(self, other):
        if not math_tools.is_integer(other):
            return NotImplemented
        for key in tuple(self):
            self[key] //= other
        return self
            
        
    def __imod__(self, other):
        if math_tools.is_integer(other):
            for key in tuple(self):
                self[key] %= other
            return self
        elif isinstance(other, _BaseBagMixin):
            floordiv_result = self // other
            self %= floordiv_result
            return self
        else:
            return NotImplemented
            

    def __ipow__(self, other, modulo=None):
        if not math_tools.is_integer(other):
            return NotImplemented
        for key in tuple(self):
            self[key] = pow(self[key], other, modulo)
        return self
    
    def popitem(self):
        return self._dict.popitem()
      


class _OrderedBagMixin(Ordered):
    def __repr__(self):
        if not self:
            return '%s()' % type(self).__name__
        return '%s(%s)' % (
            type(self).__name__,
            '[%s]' % ', '.join('%s' % (item,) for item in self.items())
        )
    __reversed__ = lambda self: reversed(self._dict)
    
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        for item, other_item in itertools.zip_longest(self.items(),
                                                      other.items()):
            if item != other_item:
                return False
        else:
            return True
        
    

class _BaseDictDelegator(collections.MutableMapping):

    # Start by filling-out the abstract methods
    def __init__(self, dict=None, **kwargs):
        self._dict = self._dict_type()
        if dict is not None:
            self.update(dict)
        if len(kwargs):
            self.update(kwargs)
    def __len__(self): return len(self._dict)
    def __getitem__(self, key):
        if key in self._dict:
            return self._dict[key]
        if hasattr(self.__class__, "__missing__"):
            return self.__class__.__missing__(self, key)
        raise KeyError(key)
    def __setitem__(self, key, item): self._dict[key] = item
    def __delitem__(self, key): del self._dict[key]
    def __iter__(self):
        return iter(self._dict)

    # Modify __contains__ to work correctly when __missing__ is present
    def __contains__(self, key):
        return key in self._dict

    # Now, add the methods in dicts but not in MutableMapping
    def __repr__(self): return repr(self._dict)
    def copy(self):
        if self.__class__ is _OrderedDictDelegator:
            return _OrderedDictDelegator(self._dict.copy())
        import copy
        data = self._dict
        try:
            self._dict = self._dict_type()
            c = copy.copy(self)
        finally:
            self._dict = data
        c.update(self)
        return c
    @classmethod
    def fromkeys(cls, iterable, value=None):
        d = cls()
        for key in iterable:
            d[key] = value
        return d

class _OrderedDictDelegator(Ordered, _BaseDictDelegator):
    _dict_type = OrderedDict

class _DictDelegator(DefinitelyUnordered, _BaseDictDelegator):
    _dict_type = dict

                
class Bag(_MutableBagMixin, _DictDelegator):
    '''
    A bag that counts items.
    
    This is a mapping between items and their count:
    
        >>> Bag('aaabcbc')
        Bag({'a': 3, 'b': 2, 'c': 2})
    
    It can be created from either an iterable like above, or from a `dict`. 
    
    This is similar to Python's builtin `collections.Counter`, except unlike
    `collections.Counter`, we don't think of it as a "dict that happens to
    count objects" but as an object that is absolutely intended for counting
    objects. This means we do not allow arbitrary values for counts like
    `collections.Counter` and we don't have to deal with all the complications
    that follow. Only positive integers are allowed as counts.
    
    '''                
    
                
class OrderedBag(_OrderedBagMixin, _MutableBagMixin, _OrderedDictDelegator):
    '''
    An ordered bag that counts items.
    
    This is a ordered mapping between items and their count:
    
        >>> OrderedBag('aaabcbc')
        OrderedBag((('a', 3), ('b', 2), ('c', 2)))
    
    It can be created from either an iterable like above, or from a `dict`. 
    
    This is similar to Python's builtin `collections.Counter`, except unlike
    `collections.Counter`, we don't think of it as a "dict that happens to
    count objects" but as an object that is absolutely intended for counting
    objects. This means we do not allow arbitrary values for counts like
    `collections.Counter` and we don't have to deal with all the complications
    that follow. Only positive integers are allowed as counts.
    
    Also, unlike `collections.Counter`, items have an order. (Simliarly to
    `collections.OrderedDict`.)
    
    '''
    def popitem(self, last=True):
        return self._dict.popitem(last=last)
      
    
                
class FrozenBag(_BaseBagMixin, FrozenDict):
    '''
    An immutable bag that counts items.
    
    This is an immutable mapping between items and their count:
    
        >>> FrozenBag('aaabcbc')
        FrozenBag({'a': 3, 'b': 2, 'c': 2})
    
    It can be created from either an iterable like above, or from a `dict`. 
    
    This is similar to Python's builtin `collections.Counter`, except unlike
    `collections.Counter`, we don't think of it as a "dict that happens to
    count objects" but as an object that is absolutely intended for counting
    objects. This means we do not allow arbitrary values for counts like
    `collections.Counter` and we don't have to deal with all the complications
    that follow. Only positive integers are allowed as counts.
    
    Also, unlike `collections.Counter`, it's immutable, therefore it's also
    hashable, and thus it can be used as a key in dicts and sets.

    '''
    def __hash__(self):
        return hash((type(self), frozenset(self.items())))
      
                
class FrozenOrderedBag(_OrderedBagMixin, _BaseBagMixin,
                       FrozenOrderedDict):
    '''
    An immutable, ordered bag that counts items.
    
    This is an ordered mapping between items and their count:
    
        >>> FrozenOrderedBag('aaabcbc')
        FrozenOrderedBag((('a', 3), ('b', 2), ('c', 2)))
    
    It can be created from either an iterable like above, or from a `dict`. 
    
    This is similar to Python's builtin `collections.Counter`, except unlike
    `collections.Counter`, we don't think of it as a "dict that happens to
    count objects" but as an object that is absolutely intended for counting
    objects. This means we do not allow arbitrary values for counts like
    `collections.Counter` and we don't have to deal with all the complications
    that follow. Only positive integers are allowed as counts.
    
    Also, unlike `collections.Counter`:
     - Items have an order. (Simliarly to `collections.OrderedDict`.)
     - It's immutable, therefore it's also hashable, and thus it can be used as
       a key in dicts and sets.
       
    '''
    def __hash__(self):
        return hash((type(self), tuple(self.items())))
        
