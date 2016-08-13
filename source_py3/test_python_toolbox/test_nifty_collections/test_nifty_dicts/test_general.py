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


def test_base_double_dict():
    from nifty_collections.nifty_dicts.abstract import BaseDoubleDict
    assert isinstance(DoubleDict(), BaseDoubleDict)
    assert isinstance(DoubleFrozenDict(), BaseDoubleDict)
    assert isinstance(DoubleOrderedDict(), BaseDoubleDict)
    assert isinstance(DoubleFrozenOrderedDict(), BaseDoubleDict)
    assert not isinstance({}, BaseDoubleDict)
    assert not isinstance(OrderedDict(), BaseDoubleDict)
    assert not isinstance(FrozenDict(), BaseDoubleDict)
    assert not isinstance(FrozenOrderedDict(), BaseDoubleDict)
    assert not isinstance(["haha I'm not even related"], BaseDoubleDict)
    