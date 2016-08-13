# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various data types, similarly to the stdlib's `collections`.'''

from .various_ordered_sets import OrderedSet, FrozenOrderedSet, EmittingOrderedSet
from .weak_key_default_dict import WeakKeyDefaultDict
from .weak_key_identity_dict import WeakKeyIdentityDict
from .lazy_tuple import LazyTuple
from .bagging import Bag, OrderedBag, FrozenBag, FrozenOrderedBag
from .frozen_bag_bag import FrozenBagBag
from .condition_list import ConditionList
from ..cute_enum import CuteEnum
from .emitting_weak_key_default_dict import EmittingWeakKeyDefaultDict
from .nifty_dicts import (DoubleDict, FrozenDict, OrderedDict,
                          DoubleFrozenDict, DoubleOrderedDict,
                          FrozenOrderedDict,
                          DoubleFrozenOrderedDict)

from .abstract import Ordered, DefinitelyUnordered