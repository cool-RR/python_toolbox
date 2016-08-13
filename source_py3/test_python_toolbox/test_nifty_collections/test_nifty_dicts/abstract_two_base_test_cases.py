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


class _AbstractDoubleFrozenDictTestCase(_AbstractDoubleDictTestCase,
                                        _AbstractFrozenDictTestCase):
    pass


class _AbstractDoubleNotFrozenDictTestCase(_AbstractDoubleDictTestCase,
                                           _AbstractNotFrozenDictTestCase):
    pass


class _AbstractNotDoubleFrozenDictTestCase(_AbstractFrozenDictTestCase,
                                           _AbstractNotDoubleDictTestCase):
    pass


class _AbstractNotDoubleNotFrozenDictTestCase(_AbstractNotDoubleDictTestCase,
                                              _AbstractNotFrozenDictTestCase):
    pass


###############################################################################


class _AbstractDoubleOrderedDictTestCase(_AbstractDoubleDictTestCase,
                                         _AbstractOrderedDictTestCase):
    pass

class _AbstractDoubleNotOrderedDictTestCase(_AbstractDoubleDictTestCase,
                                            _AbstractNotOrderedDictTestCase):
    pass


class _AbstractNotDoubleOrderedDictTestCase(_AbstractOrderedDictTestCase,
                                            _AbstractNotDoubleDictTestCase):
    pass


class _AbstractNotDoubleNotOrderedDictTestCase(_AbstractNotDoubleDictTestCase,
                                               _AbstractNotOrderedDictTestCase):
    pass


###############################################################################


class _AbstractFrozenOrderedDictTestCase(_AbstractFrozenDictTestCase,
                                         _AbstractOrderedDictTestCase):
    pass


class _AbstractFrozenNotOrderedDictTestCase(_AbstractFrozenDictTestCase,
                                            _AbstractNotOrderedDictTestCase):
    pass


class _AbstractNotFrozenOrderedDictTestCase(_AbstractOrderedDictTestCase,
                                            _AbstractNotFrozenDictTestCase):
    pass


class _AbstractNotFrozenNotOrderedDictTestCase(_AbstractNotFrozenDictTestCase,
                                               _AbstractNotOrderedDictTestCase):
    pass


