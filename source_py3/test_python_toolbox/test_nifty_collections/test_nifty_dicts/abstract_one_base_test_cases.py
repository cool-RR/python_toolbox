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

from tools import get_pseudo_random_strings
from abstract_dict_test_case import AbstractDictTestCase


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
        with cute_testing.RaiseAssertor(ValueError, text='repeating value'):
            self.d_type((('a', 'b'), ('c', 'd',), ('e', 'b',)))
        with cute_testing.RaiseAssertor(ValueError, text='repeating value'):
            self.d_type(foo=7, bar=7)
        with cute_testing.RaiseAssertor(ValueError, text='repeating value'):
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
        
    def test_frozen(self):
        d = self.d_type(((1, 2), (3, 4)))
        with cute_testing.RaiseAssertor(TypeError):
            d[5] = 6
        with cute_testing.RaiseAssertor(TypeError):
            del d[1]
        assert not hasattr(d, 'setdefault')
        assert not hasattr(d, 'pop')
        assert not hasattr(d, 'popitem')
        assert not hasattr(d, 'update')
        

        
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
        
    def test_notfrozen(self):
        d = self.d_type(((1, 2), (3, 4)))
        assert len(d) == 2

        d[5] = 6
        assert len(d) == 3

        del d[5]
        assert len(d) == 2

        d.setdefault(5, 6)
        assert len(d) == 3

        value = d.pop(5)
        assert value == 6
        assert len(d) == 2

        d[5] = 6
        assert len(d) == 3

        item = d.popitem()
        assert item in {(1, 2), (3, 4), (5, 6)}
        assert item[0] not in d
        assert len(d) == 2

        d.update({'foo': 'bar',})
        assert len(d) == 3
        

###############################################################################


class AbstractOrderedDictTestCase(AbstractDictTestCase):
    
    def make_big_dict(self):
        pseudo_random_strings = get_pseudo_random_strings(100)
        pairs = tuple(sequence_tools.partitions(pseudo_random_strings, 2))
        d = self.d_type(pairs)
        assert len(d) == 50
        assert tuple(d.items()) == pairs
        return d
    
    
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
        d = self.make_big_dict()
        assert d.index(tuple(d.items())[7][0]) == 7
        with cute_testing.RaiseAssertor(ValueError):
            d.index('meow')
            
        assert tuple(zip(d.keys(), d.values())) == tuple(d.items())
        
        assert tuple(reversed(d)) == next(zip(*tuple(d.items())[::-1]))

    def test_index(self):
        d = self.d_type(((1, 2), (3, 4)))
        assert d.index(3)
        with cute_testing.RaiseAssertor(ValueError):
            d.index('foo')
        

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


