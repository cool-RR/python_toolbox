# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
This module defines a variable Infinity which simply stands for float("inf"). TODO
The only reason for this alias is to make code more readable.
"""

import copy
import numbers

is_a_number = lambda thing: isinstance(thing, numbers.Number)

Infinity = float("inf")

class FunnyInfinityClass(object):
    def __init__(self):
        self.added = 0
        self.sign = 1
    def __add__(self, other):
        if is_a_number(other):
            result = copy.deepcopy(self)
            result.added += other
            return result
        elif isinstance(other, FunnyInfinityClass):
            if self.sign == other.sign:
                raise NotImplementedError
            else:
                return self.added + other.added
        else:
            raise NotImplementedError
    def __cmp__(self, other):
        if is_a_number(other):
            return 1
        elif isinstance(other, FunnyInfinityClass):
            sign_comparison = cmp(self.sign, other.sign)
            if sign_comparison != 0:
                return sign_comparison
            else:
                return cmp(self.added, other.added)
        else:
            raise NotImplementedError
    def __neg__(self):
        result = copy.deepcopy(self)
        result.sign *= -1
    def __repr__(self):
        if self.added == 0:            
            return "FunnyInfinity" 
        else:
            return "(FunnyInfinity + %s)" % self.added
    
        
FunnyInfinity = FunnyInfinityClass()
        
        