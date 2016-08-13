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


class _AbstractDictTestCase(cute_testing.TestCase):
    __test__ = False
    d_type = None # Filled in by subclasses
    
    def test_mapping_base_class(self):
        assert issubclass(self.d_type, collections.Mapping)
    
    def test_common(self):
        d = self.d_type(((1, 2), (3, 4), (5, 6)))
        assert len(d) == 3
        assert set(d.keys()) == {1, 3, 5}
        assert set(d.values()) == {2, 4, 6}
        assert set(d.items()) == {(1, 2), (3, 4), (5, 6)}
        assert d[1] == 2
        assert d[3] == 4
        assert d[5] == 6
        with cute_testing.RaiseAssertor(exception_type=KeyError):
            d[7]
        with cute_testing.RaiseAssertor(exception_type=KeyError):
            d[None]
        with cute_testing.RaiseAssertor(exception_type=KeyError):
            d['whatever']
            
        assert d.get(1) == 2
        assert d.get(1, 'whatever') == 2
        assert d.get(10, 'whatever') == 'whatever'
        
        assert d == d.copy() == d.copy()
        
        
class _AbstractDoubleDictTestCase(_AbstractDictTestCase):
    def test_double_dict_base_class(self):
        assert issubclass(
            self.d_type,
            nifty_collections.nifty_dicts.abstract.BaseDoubleDict
        )
        
class _AbstractFrozenDictTestCase(_AbstractDictTestCase):
    def test_frozen_dict_base_class(self):
        assert issubclass(
            self.d_type,
            collections.abc.Hashable
        )
        assert not issubclass(
            self.d_type,
            collections.abc.MutableMapping
        )
class _AbstractOrderedDictTestCase(_AbstractDictTestCase):
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
