# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various caching tools.'''

# todo: examine thread-safety

from .decorators import cache
from .cached_type import CachedType
from .cached_property import CachedProperty