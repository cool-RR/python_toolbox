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
        