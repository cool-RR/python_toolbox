# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.third_party import enum
from python_toolbox.third_party import functools

from python_toolbox import caching

        
# @orking around Python bug 22506 that would be fixed in Python 3.5:
del enum.EnumMeta.__dir__
# This makes enum members not appear in `dir` but it also prevents other
# important items from being deleted.


class EnumType(enum.EnumMeta):
    '''Metaclass for our kickass enum type.'''
    __getitem__ = lambda self, i: self._values_tuple[i]
    # This `__getitem__` is important, so we could feed enum types straight
    # into `ProductSpace`.
    
    _values_tuple = caching.CachedProperty(tuple)
    
        
    
@functools.total_ordering
class _OrderableEnumMixin(object):
    '''
    Mixin for an enum that has an order between items.
    
    We're defining a mixin rather than defining these things on `CuteEnum`
    because we can't use `functools.total_ordering` on `Enum`, because `Enum`
    has exception-raising comparison methods, so `functools.total_ordering`
    doesn't override them.
    '''
    number = caching.CachedProperty(
        lambda self: type(self)._values_tuple.index(self)
    )
    __lt__ = lambda self, other: isinstance(other, CuteEnum) and \
                                                   (self.number < other.number)
    
    
class CuteEnum(_OrderableEnumMixin, enum.Enum):
    '''
    An improved version of Python's builtin `enum.Enum` type.
    
    Note that on Python 2, you must include a line like this in your enum
    definition:
    
        __order__ = 'CHOCOLATE VANILLA RASPBERRY BANANA'

    This defines the order of elements. (On Python 3 you don't have to do this
    because Python 3 can figure out the order by itself.)
    
    `CuteEnum` provides the following benefits:
    
      - Each item has a property `number` which is its serial number in the
        enum.
        
      - Items are comparable with each other based on that serial number. So
        sequences of enum items can be sorted.
        
      - The enum type itself can be accessed as a sequence, and you can access
        its items like this: `MyEnum[7]`.
      
    '''
    __metaclass__ = EnumType