# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import collections.abc

from python_toolbox.third_party import unittest2

import nose

from python_toolbox import cute_iter_tools
from python_toolbox import cute_testing

from python_toolbox import nifty_collections
from python_toolbox.nifty_collections import (
    DoubleDict, FrozenDict, OrderedDict,
    DoubleFrozenDict, DoubleOrderedDict,
    FrozenOrderedDict, DoubleFrozenOrderedDict
)

from abstract_two_base_test_cases import * 


class DoubleDictTestCase(AbstractDoubleNotFrozenDictTestCase,
                         AbstractDoubleNotOrderedDictTestCase,
                         AbstractNotFrozenNotOrderedDictTestCase):
    __test__ = True
    d_type = DoubleDict


class FrozenDictTestCase(AbstractNotDoubleFrozenDictTestCase,
                         AbstractFrozenNotOrderedDictTestCase,
                         AbstractNotDoubleNotOrderedDictTestCase):
    __test__ = True
    d_type = FrozenDict

        
class OrderedDictTestCase(AbstractNotDoubleOrderedDictTestCase,
                          AbstractNotFrozenOrderedDictTestCase,
                          AbstractNotDoubleNotFrozenDictTestCase):
    __test__ = True
    d_type = OrderedDict
        
        
class DoubleFrozenDictTestCase(AbstractDoubleFrozenDictTestCase,
                               AbstractDoubleNotOrderedDictTestCase,
                               AbstractFrozenNotOrderedDictTestCase):
    __test__ = True
    d_type = DoubleFrozenDict
        
        
class DoubleOrderedDictTestCase(AbstractDoubleOrderedDictTestCase,
                                AbstractDoubleNotFrozenDictTestCase,
                                AbstractNotFrozenOrderedDictTestCase):
    __test__ = True
    d_type = DoubleOrderedDict
    
    def test_changing_order_affects_double(self):
        d = self.make_big_dict()
        assert tuple(d.inverse.keys()) == tuple(d.values())
        assert tuple(d.inverse.values()) == tuple(d.keys())
        
        old_pairs = tuple(d.items())
        d.sort()
        assert set(d.items()) == set(old_pairs)
        assert tuple(d.items()) != old_pairs
        assert tuple(d.inverse.keys()) == tuple(d.values())
        assert tuple(d.inverse.values()) == tuple(d.keys())
        
        old_pairs = tuple(d.items())
        d.inverse.sort(key=hash, reverse=True)
        assert set(d.items()) == set(old_pairs)
        assert tuple(d.items()) != old_pairs
        assert tuple(d.inverse.keys()) == tuple(d.values())
        assert tuple(d.inverse.values()) == tuple(d.keys())
        
        old_pairs = tuple(d.items())
        some_key, some_value = old_pairs[37]
        d.move_to_end(some_key)
        assert d.index(some_key) == len(d) - 1
        assert d.inverse.index(some_value) == len(d) - 1
        assert set(d.items()) == set(old_pairs)
        assert tuple(d.items()) != old_pairs
        assert tuple(d.inverse.keys()) == tuple(d.values())
        assert tuple(d.inverse.values()) == tuple(d.keys())
        
        old_pairs = tuple(d.items())
        some_other_key, some_other_value = old_pairs[23]
        d.inverse.move_to_end(some_other_value, last=False)
        assert d.index(some_key) == len
        assert d.inverse.index(some_other_value) == 0
        assert set(d.items()) == set(old_pairs)
        assert tuple(d.items()) != old_pairs
        assert tuple(d.inverse.keys()) == tuple(d.values())
        assert tuple(d.inverse.values()) == tuple(d.keys())
        
        d['foo'] == 'bar'
        assert len(d) == len(d.inverse) == len(old_pairs) + 1
        assert d.index('foo') == len(d) - 1
        assert d.inverse.index('bar') == len(d) - 1
        
        
class FrozenOrderedDictTestCase(AbstractFrozenOrderedDictTestCase,
                                AbstractNotDoubleFrozenDictTestCase,
                                AbstractNotDoubleOrderedDictTestCase):
    __test__ = True
    d_type = FrozenOrderedDict
        
class DoubleFrozenOrderedDictTestCase(AbstractDoubleFrozenDictTestCase,
                                      AbstractDoubleOrderedDictTestCase,
                                      AbstractFrozenOrderedDictTestCase):
    __test__ = True
    d_type = DoubleFrozenOrderedDict
        