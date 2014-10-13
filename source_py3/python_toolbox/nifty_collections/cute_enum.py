# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

import enum
import functools

from python_toolbox import caching


class EnumType(enum.EnumMeta):
    def __dir__(cls):
        return type.__dir__(cls) + cls._member_names_
    
    __getitem__ = lambda self, i: self._values_tuple[i]
    # This `__getitem__` is important, so we could feed enum types straight
    # into `ProductSpace`.
    
    _values_tuple = caching.CachedProperty(tuple)
    
    
    
@functools.total_ordering
class _OrderableEnumMixin:
    '''
    
    We're defining a mixin rather than defining these things on `CuteEnum`
    because we can't use `functools.total_ordering` on Enum, because it has
    exception-raising comparison methods, so `functools.total_ordering` doesn't
    override them.
    '''
    number = caching.CachedProperty(
        lambda self: type(self)._values_tuple.index(self)
    )
    __lt__ = lambda self, other: isinstance(other, CuteEnum) and \
                                                   (self.number < other.number)
    
    
class CuteEnum(_OrderableEnumMixin, enum.Enum, metaclass=EnumType):
    
    pass