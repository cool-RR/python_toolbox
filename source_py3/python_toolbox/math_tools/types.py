# Copyright 2009-2014 Ram Rachum.
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
    pass

class _PossiblyInfiniteRealType(abc.ABCMeta):
    def __instancecheck__(self, thing):
        return isinstance(thing, numbers.Real) or (thing in infinities)
class PossiblyInfiniteReal(numbers.Number,
                           metaclass=_PossiblyInfiniteRealType):
    pass


