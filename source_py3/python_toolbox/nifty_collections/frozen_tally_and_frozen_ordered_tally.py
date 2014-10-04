# Copyright 2009-2014 Ram Rachum.,
# This program is distributed under the MIT license.

import operator
import heapq
import itertools
import numbers
import collections
import functools

from .lazy_tuple import LazyTuple
from .ordered_dict import OrderedDict
from .frozen_dict_and_frozen_ordered_dict import FrozenDict, FrozenOrderedDict

try:                                    # Load C helper function if available
    from _collections import _count_elements
except ImportError:
    def _count_elements(mapping, iterable):
        '''Tally elements from the iterable.'''
        mapping_get = mapping.get
        for element in iterable:
            mapping[element] = mapping_get(element, 0) + 1

class _FrozenTallyMixin:
    '''Mixin for `FrozenTally` and `FrozenOrderedTally`.'''
    
    def __init__(self, iterable={}):
        from python_toolbox import math_tools
        
        super().__init__()
        
        if isinstance(iterable, collections.Mapping):
            for key, value, in iterable.items():
                if not math_tools.is_integer(value):
                    raise TypeError(
                        'You passed %s as the count of %s, while '
                        'a `Tally` can only handle integer counts.' %
                                                                   (value, key)
                    )
                if value < 0:
                    raise TypeError(
                        "You passed %s as the count of %s, while "
                        "a `Tally` doesn't support negative amounts." %
                                                                   (value, key)
                    )
                    
                if value == 0:
                    continue
                
                self._dict[key] = int(value)
        else:
            _count_elements(self._dict, iterable)


    __getitem__ = lambda self, key: self._dict.get(key, 0)

    def most_common(self, n=None):
        '''
        List the `n` most common elements and their counts, sorted.
        
        Results are sorted from the most common to the least. If `n is None`,
        then list all element counts.

            >>> FrozenTally('abcdeabcdabcaba').most_common(3)
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

            >>> c = FrozenTally('ABCABC')
            >>> sorted(c.elements())
            ['A', 'A', 'B', 'B', 'C', 'C']
    
            # Knuth's example for prime factors of 1836:  2**2 * 3**3 * 17**1
            >>> prime_factors = FrozenTally({2: 2, 3: 3, 17: 1})
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
    

    __pos__ = lambda self: self

    def __add__(self, other):
        '''
        Add counts from two tallies.

            >>> FrozenTally('abbb') + FrozenTally('bcc')
            FrozenTally({'b': 4, 'c': 2, 'a': 1})
            
        '''
        if not isinstance(other, _FrozenTallyMixin):
            return NotImplemented
        
        # Using `OrderedDict` to store interim results because
        # `FrozenOrderedTally` inherits from this class and it needs to have
        # items in order.
        result = OrderedDict()
        
        for element, count in self.items():
            new_count = count + other[element]
            assert new_count > 0
            result[element] = new_count
        for element, count in other.items():
            assert count > 0
            if element not in self:
                result[element] = count
        return type(self)(result)

    def __sub__(self, other):
        '''
        Subtract count, but keep only results with positive counts.

            >>> FrozenTally('abbbc') - FrozenTally('bccd')
            FrozenTally({'b': 2, 'a': 1})
            
        '''
        if not isinstance(other, _FrozenTallyMixin):
            return NotImplemented
        
        # Using `OrderedDict` to store interim results because
        # `FrozenOrderedTally` inherits from this class and it needs to have
        # items in order.
        result = OrderedDict()
        
        for element, count in self.items():
            new_count = count - other[element]
            result[element] = new_count
        return type(self)(result)

    def __or__(self, other):
        '''
        Get the maximum of value in either of the input tallies.

            >>> FrozenTally('abbb') | FrozenTally('bcc')
            FrozenTally({'b': 3, 'c': 2, 'a': 1})
            
        '''
        if not isinstance(other, _FrozenTallyMixin):
            return NotImplemented

        # Using `OrderedDict` to store interim results because
        # `FrozenOrderedTally` inherits from this class and it needs to have
        # items in order.
        result = OrderedDict()

        for element, count in self.items():
            other_count = other[element]
            new_count = other_count if count < other_count else count
            assert new_count > 0
            result[element] = new_count
        for element, count in other.items():
            assert count > 0
            if element not in self:
                result[element] = count
        return type(self)(result)

    def __and__(self, other):
        '''
        Get the minimum of corresponding counts.

            >>> FrozenTally('abbb') & FrozenTally('bcc')
            FrozenTally({'b': 1})
            
        '''
        if not isinstance(other, _FrozenTallyMixin):
            return NotImplemented

        # Using `OrderedDict` to store interim results because
        # `FrozenOrderedTally` inherits from this class and it needs to have
        # items in order.
        result = OrderedDict()

        for element, count in self.items():
            other_count = other[element]
            new_count = count if count < other_count else other_count
            result[element] = new_count
        return type(self)(result)


    __bool__ = lambda self: any(True for element in self.elements())
    
    
    _n_elements = None
    @property
    def n_elements(self):
        # Implemented as a poor man's `CachedProperty` because we can't use the
        # real `CachedProperty` due to circular import.
        if self._n_elements is None:
            self._n_elements = sum(self.values())
        return self._n_elements
        
    
    # We define all the comparison methods manually instead of using
    # `total_ordering` because `total_ordering` assumes that >= means (> and
    # ==) while we, in `FrozenOrderedTally`, don't have that hold because ==
    # takes the items' order into account.
    
    def __lt__(self, other):
        if not isinstance(other, _FrozenTallyMixin):
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
        if not isinstance(other, _FrozenTallyMixin):
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
        if not isinstance(other, _FrozenTallyMixin):
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
        if not isinstance(other, _FrozenTallyMixin):
            return NotImplemented
        for element, count in self.items():
            try:
                other_count = other[element]
            except KeyError:
                continue
            if not (count >= other_count):
                return False
        return True
            
                
class FrozenTally(_FrozenTallyMixin, FrozenDict):
    '''
    An immutable tally.
    
    A tally that (a) can't be changed and (b) has only positive integer values.
    This is like `collections.Counter`, except:
    
     - Because it's immutable, it's also hashable, and thus it can be used as a
       key in dicts and sets.
     
     - Unlike `collections.Counter`, we don't think of it as a "dict who
       happens to count objects" but as an object that is absolutely intended
       for counting objects. This means we do not allow arbitrary values for 
       counts like `collections.Counter` and we don't have to deal with a 
       class that has an identity crisis and doesn't know whether it's a
       counter or a dict.
     
    '''                
                
class FrozenOrderedTally(_FrozenTallyMixin, FrozenOrderedDict):
    '''
    An immutable, ordered tally.
    
    A tally that (a) can't be changed and (b) has only positive integer values.
    This is like `collections.Counter`, except:
    
     - Because it's immutable, it's also hashable, and thus it can be used as a
       key in dicts and sets.
     
     - Unlike `collections.Counter`, we don't think of it as a "dict who
       happens to count objects" but as an object that is absolutely intended
       for counting objects. This means we do not allow arbitrary values for 
       counts like `collections.Counter` and we don't have to deal with a 
       class that has an identity crisis and doesn't know whether it's a
       counter or a dict.
       
     - It has an order to its elements, like `collections.OrderedDict`.
     
    '''
    def __repr__(self):
        if not self:
            return '%s()' % type(self).__name__
        return '%s(%s)' % (
            type(self).__name__,
            '[%s]' % ', '.join('%s' % (item,) for item in self.items())
        )
