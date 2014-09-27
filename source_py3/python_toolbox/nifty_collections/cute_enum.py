# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

import enum
import functools

from python_toolbox import caching


@functools.total_ordering
class CuteEnum(enum.Enum):
    
    number = caching.CachedProperty(
        lambda self: type(self)._member_names_.index(self.name)
    )
    __lt__ = lambda self, other: isinstance(other, CuteEnum) and \
                                                  (self.number <= other.number)