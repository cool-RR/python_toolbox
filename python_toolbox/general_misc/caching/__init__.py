# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines various caching tools.'''

# todo: examine thread-safety

from .cache import cache
from .cached_type import CachedType
from .cached_property import CachedProperty