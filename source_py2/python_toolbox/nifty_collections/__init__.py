# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various data types, similarly to the stdlib's `collections`.'''

from .ordered_dict import OrderedDict
from .ordered_set import OrderedSet
from .weak_key_default_dict import WeakKeyDefaultDict
from .weak_key_identity_dict import WeakKeyIdentityDict
from .lazy_tuple import LazyTuple
from .frozen_dict import FrozenDict
from .frozen_counter import FrozenCounter

from .emitting_ordered_set import EmittingOrderedSet
from .emitting_weak_key_default_dict import EmittingWeakKeyDefaultDict