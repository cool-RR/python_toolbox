# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import abc
import numbers

infinity = float('inf')
infinities = (infinity, -infinity)


class _PossiblyInfiniteIntegralType(abc.ABCMeta):
    def __instancecheck__(self, thing):
        return isinstance(thing, numbers.Integral) or (thing in infinities)
class PossiblyInfiniteIntegral(numbers.Number,
                               metaclass=_PossiblyInfiniteIntegralType):
    '''An integer or infinity (including negative infinity.)'''

class _PossiblyInfiniteRealType(abc.ABCMeta):
    def __instancecheck__(self, thing):
        return isinstance(thing, numbers.Real) or (thing in infinities)
class PossiblyInfiniteReal(numbers.Number,
                           metaclass=_PossiblyInfiniteRealType):
    '''A real number or infinity (including negative infinity.)'''

class _NaturalType(abc.ABCMeta):
    def __instancecheck__(self, thing):
        return isinstance(thing, numbers.Integral) and thing >= 1
class Natural(numbers.Number,
              metaclass=_NaturalType):
    '''A natural number, meaning a positive integer (0 not included.)'''
