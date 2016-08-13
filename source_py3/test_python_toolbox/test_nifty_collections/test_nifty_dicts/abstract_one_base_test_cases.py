# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import collections.abc

from python_toolbox.third_party import unittest2
import nose

from python_toolbox import caching
from python_toolbox import math_tools
from python_toolbox import sequence_tools
from python_toolbox import cute_iter_tools
from python_toolbox import cute_testing

from python_toolbox import nifty_collections
from python_toolbox.nifty_collections import (
    DoubleDict, FrozenDict, OrderedDict,
    DoubleFrozenDict, DoubleOrderedDict,
    FrozenOrderedDict, DoubleFrozenOrderedDict
)

from abstract_dict_test_case import AbstractDictTestCase

@caching.cache()
def get_pseudo_random_strings(n):
    '''
    Get a list of random-like digit strings but ensure they're always the same.
    
    And also they're unique, i.e. no recurrences.
    '''
    some_pi_digits = str(math_tools.pi_decimal).split('.')[-1][:900]
    partitions = sequence_tools.partitions(some_pi_digits, partition_size=5)
    pseudo_random_numbers = nifty_collections.OrderedSet()
    for partition in partitions:
        if len(pseudo_random_numbers) == n:
            return pseudo_random_numbers
        pseudo_random_numbers.add(partition)
    else:
        raise RuntimeError('Not enough unique pseudo-random numbers.')
    

class AbstractDoubleDictTestCase(AbstractDictTestCase):
    def test_double_dict_base_class(self):
        assert issubclass(
            self.d_type,
            nifty_collections.nifty_dicts.abstract.BaseDoubleDict
        )
        
    def test_inverse_basics(self):
        d = self.d_type((('a', 'b'), ('c', 'd',), ('e', 'f',)))
        inverse = d.inverse
        
        assert inverse.inverse is d
        assert type(inverse) is type(d)
        assert len(inverse) == len(d)
        assert dict(inverse) == {'b': 'a', 'd': 'c', 'f': 'e',}
        assert inverse['b'] == 'a'
        
        
    def test_no_value_repeats(self):
        with cute_testing.RaiseAssertor(ValueError):
            self.d_type((('a', 'b'), ('c', 'd',), ('e', 'b',)))
        with cute_testing.RaiseAssertor(ValueError):
            self.d_type(foo=7, bar=7)
        with cute_testing.RaiseAssertor(ValueError):
            self.d_type({1: ('meow',), 2: ('meow',),})
        

class AbstractNotDoubleDictTestCase(AbstractDictTestCase):
    def test_not_double_dict_base_class(self):
        assert not issubclass(
            self.d_type,
            nifty_collections.nifty_dicts.abstract.BaseDoubleDict
        )
        
    def test_no_inverse(self):
        assert not hasattr(self.d_type(), 'inverse')
        
    
###############################################################################

        
class AbstractFrozenDictTestCase(AbstractDictTestCase):
    def test_frozen_dict_base_class(self):
        assert issubclass(
            self.d_type,
            collections.abc.Hashable
        )
        assert not issubclass(
            self.d_type,
            collections.abc.MutableMapping
        )
        
    def test_hashable(self):
        d = self.d_type(((1, 2), (3, 4)))
        assert hash(d) == hash(d)
        {d: 7,}

        
class AbstractNotFrozenDictTestCase(AbstractDictTestCase):
    def test_not_frozen_dict_base_class(self):
        assert not issubclass(
            self.d_type,
            collections.abc.Hashable
        )
        assert issubclass(
            self.d_type,
            collections.abc.MutableMapping
        )
        
    def test_not_hashable(self):
        d = self.d_type(((1, 2), (3, 4)))
        with cute_testing.RaiseAssertor(TypeError):
            hash(d)
        with cute_testing.RaiseAssertor(TypeError):
            {d: 7,}
        

###############################################################################


class AbstractOrderedDictTestCase(AbstractDictTestCase):
    def test_ordered_dict_base_class(self):
        assert issubclass(
            self.d_type,
            nifty_collections.abstract.Ordered
        )
        assert issubclass(
            self.d_type,
            nifty_collections.abstract.OrderedMapping
        )
        assert not issubclass(
            self.d_type,
            nifty_collections.abstract.DefinitelyUnordered
        )
        
    def test_ordered_on_long(self):
        pseudo_random_strings = get_pseudo_random_strings(100)
        pairs = sequence_tools.partitions(pseudo_random_strings, 2)
        d = self.d_type(pairs)
        assert len(d) == 50
        assert tuple(d.items()) == pairs
        assert d.index(pairs[7][0]) == 7
        with cute_testing.RaiseAssertor(ValueError):
            d.index('meow')
            
        assert tuple(zip(d.keys(), d.values())) == pairs
        
        assert tuple(reversed(d)) == next(zip(*pairs))


class AbstractNotOrderedDictTestCase(AbstractDictTestCase):
    def test_not_ordered_dict_base_class(self):
        assert not issubclass(
            self.d_type,
            nifty_collections.abstract.Ordered
        )
        assert not issubclass(
            self.d_type,
            nifty_collections.abstract.OrderedMapping
        )
        assert issubclass(
            self.d_type,
            nifty_collections.abstract.DefinitelyUnordered
        )

    def test_not_ordered_on_long(self):
        pseudo_random_strings = get_pseudo_random_strings(100)
        pairs = sequence_tools.partitions(pseudo_random_strings, 2)
        d = self.d_type(pairs)
        assert len(d) == 50
        assert tuple(d.items()) != pairs
        assert set(d.items()) == set(pairs)
        assert not hasattr(d, 'index')
        assert not hasattr(d, 'move_to_end')
        assert not hasattr(d, 'sort')
        assert not hasattr(d, '__reversed__')


