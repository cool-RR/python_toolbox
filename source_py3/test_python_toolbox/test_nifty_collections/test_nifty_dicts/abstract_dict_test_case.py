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


class AbstractDictTestCase(cute_testing.TestCase):
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
        assert '1' in d
        assert 'meow' not in d
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
        
        assert set(d) == set(d.keys())
        assert tuple(map(set, zip(*d.items()))) == \
                                               (set(d.keys()), set(d.values()))
        
        
