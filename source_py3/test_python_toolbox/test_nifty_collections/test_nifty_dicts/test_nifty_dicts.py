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


class DoubleDictTestCase(_AbstractDoubleNotFrozenDictTestCase,
                         _AbstractDoubleNotOrderedDictTestCase,
                         _AbstractNotFrozenNotOrderedDictTestCase):
    __test__ = True
    d_type = DoubleDict


class FrozenDictTestCase(_AbstractNotDoubleFrozenDictTestCase,
                         _AbstractFrozenNotOrderedDictTestCase,
                         _AbstractNotDoubleNotOrderedDictTestCase):
    __test__ = True
    d_type = FrozenDict

        
class OrderedDictTestCase(_AbstractNotDoubleOrderedDictTestCase,
                          _AbstractNotFrozenOrderedDictTestCase,
                          _AbstractNotDoubleNotFrozenDictTestCase):
    __test__ = True
    d_type = OrderedDict
        
        
class DoubleFrozenDictTestCase(_AbstractDoubleFrozenDictTestCase,
                               _AbstractDoubleNotOrderedDictTestCase,
                               _AbstractFrozenNotOrderedDictTestCase):
    __test__ = True
    d_type = DoubleFrozenDict
        
        
class DoubleOrderedDictTestCase(_AbstractDoubleOrderedDictTestCase,
                                _AbstractDoubleNotFrozenDictTestCase,
                                _AbstractNotFrozenOrderedDictTestCase):
    __test__ = True
    d_type = DoubleOrderedDict
        
        
class FrozenOrderedDictTestCase(_AbstractFrozenOrderedDictTestCase,
                                _AbstractNotDoubleFrozenDictTestCase,
                                _AbstractNotDoubleOrderedDictTestCase):
    __test__ = True
    d_type = FrozenOrderedDict
        
class DoubleFrozenOrderedDictTestCase(_AbstractDoubleFrozenDictTestCase,
                                      _AbstractDoubleOrderedDictTestCase,
                                      _AbstractFrozenOrderedDictTestCase):
    __test__ = True
    d_type = DoubleFrozenOrderedDict
        