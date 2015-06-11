# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various data types, similarly to the stdlib's `collections`.'''

from .ordered_dict import OrderedDict
from .various_ordered_sets import OrderedSet, FrozenOrderedSet, EmittingOrderedSet
from .weak_key_default_dict import WeakKeyDefaultDict
from .weak_key_identity_dict import WeakKeyIdentityDict
from .lazy_tuple import LazyTuple
from .various_frozen_dicts import FrozenDict, FrozenOrderedDict
from .bagging import Bag, OrderedBag, FrozenBag, FrozenOrderedBag
from .frozen_bag_bag import FrozenBagBag
from .cute_enum import CuteEnum

from .emitting_weak_key_default_dict import EmittingWeakKeyDefaultDict
from .abstract import Ordered, DefinitelyUnordered