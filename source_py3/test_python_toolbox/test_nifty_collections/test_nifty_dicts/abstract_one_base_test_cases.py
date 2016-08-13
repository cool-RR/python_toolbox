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

from .abstract_dict_test_case import _AbstractDictTestCase


class _AbstractDoubleDictTestCase(_AbstractDictTestCase):
    def test_double_dict_base_class(self):
        assert issubclass(
            self.d_type,
            nifty_collections.nifty_dicts.abstract.BaseDoubleDict
        )
        

class _AbstractNotDoubleDictTestCase(_AbstractDictTestCase):
    def test_not_double_dict_base_class(self):
        assert not issubclass(
            self.d_type,
            nifty_collections.nifty_dicts.abstract.BaseDoubleDict
        )
        
    
###############################################################################

        
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

        
class _AbstractNotFrozenDictTestCase(_AbstractDictTestCase):
    def test_not_frozen_dict_base_class(self):
        assert not issubclass(
            self.d_type,
            collections.abc.Hashable
        )
        assert issubclass(
            self.d_type,
            collections.abc.MutableMapping
        )
        

###############################################################################


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


class _AbstractNotOrderedDictTestCase(_AbstractDictTestCase):
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
