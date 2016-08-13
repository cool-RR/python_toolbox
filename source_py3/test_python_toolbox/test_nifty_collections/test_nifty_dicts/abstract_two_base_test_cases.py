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

from abstract_one_base_test_cases import * 


###############################################################################


class AbstractDoubleFrozenDictTestCase(AbstractDoubleDictTestCase, 
                                       AbstractFrozenDictTestCase):
    pass


class AbstractDoubleNotFrozenDictTestCase(AbstractDoubleDictTestCase,
                                          AbstractNotFrozenDictTestCase):
    pass


class AbstractNotDoubleFrozenDictTestCase(AbstractFrozenDictTestCase,
                                          AbstractNotDoubleDictTestCase):
    pass


class AbstractNotDoubleNotFrozenDictTestCase(AbstractNotDoubleDictTestCase,
                                             AbstractNotFrozenDictTestCase):
    pass


###############################################################################


class AbstractDoubleOrderedDictTestCase(AbstractDoubleDictTestCase,
                                        AbstractOrderedDictTestCase):
    pass

class AbstractDoubleNotOrderedDictTestCase(AbstractDoubleDictTestCase,
                                           AbstractNotOrderedDictTestCase):
    pass


class AbstractNotDoubleOrderedDictTestCase(AbstractOrderedDictTestCase,
                                           AbstractNotDoubleDictTestCase):
    pass


class AbstractNotDoubleNotOrderedDictTestCase(AbstractNotDoubleDictTestCase,
                                              AbstractNotOrderedDictTestCase):
    pass


###############################################################################


class AbstractFrozenOrderedDictTestCase(AbstractFrozenDictTestCase,
                                        AbstractOrderedDictTestCase):
    pass


class AbstractFrozenNotOrderedDictTestCase(AbstractFrozenDictTestCase,
                                           AbstractNotOrderedDictTestCase):
    pass


class AbstractNotFrozenOrderedDictTestCase(AbstractOrderedDictTestCase,
                                           AbstractNotFrozenDictTestCase):
    pass


class AbstractNotFrozenNotOrderedDictTestCase(AbstractNotFrozenDictTestCase,
                                              AbstractNotOrderedDictTestCase):
    pass


