# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

import abc
import numbers

infinity = float('inf')
infinities = (infinity, -infinity)


class _PossiblyInfiniteIntegralType(abc.ABCMeta):
    # blocktodo: use everywhere in python_toolbox
    def __instancecheck__(self, thing):
        return isinstance(thing, numbers.Integral) or (thing in infinities)
class PossiblyInfiniteIntegral(numbers.Number):
    __metaclass__ = _PossiblyInfiniteIntegralType

class _PossiblyInfiniteRealType(abc.ABCMeta):
    # blocktodo: use everywhere in python_toolbox
    def __instancecheck__(self, thing):
        return isinstance(thing, numbers.Real) or (thing in infinities)
class PossiblyInfiniteReal(numbers.Number):
    __metaclass__ = _PossiblyInfiniteRealType


