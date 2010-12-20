# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `Infinity` class and related exceptions.

See their documentation for more info.
'''

from garlicsim.general_misc.exceptions import CuteException
from garlicsim.general_misc import math_tools


__all__ = ['infinity', 'InfinityError', 'InfinityRaceError']


def is_floatable(x):
    try:
        float(x)
        return True
    except Exception:
        return False

    
def is_nonfractional(x):
    try:
        int(x)
        return int(x) == x
    except Exception:
        return False
        
    
class InfinityRaceError(CuteException):
    '''
    An "infinity race" between two infinite sizes.
    
    A calculation is being made between two quantities that involve infinity,
    and the two infinities are "pitted" against each other in a way which makes
    it impossible to determine what the result of the computation would be.
    '''

    
class InfinityError(CuteException):
    '''infinity-related exception.'''

    
class Infinity(object):
    '''
    A class for infinity numbers.
    
    There are only two distinct instances of this class: infinity and
    (-infinity).
    '''
    #todo: add __assign__ or whatever it's called
    #todo: add more interoperability with float(inf). (Need to detect its
    #existance)    
    #todo: calling it Infinity is a bit wrong./
    
    def __init__(self, direction=1):
        self.direction = direction
        
    def __abs__(self):
        return infinity
    
    def __add__(self, other):
        if isinstance(other, Infinity):
            if self.direction == other.direction:
                return self
            else:
                raise InfinityRaceError
        elif is_floatable(other):
            return self
        
    def __sub__(self, other):
        return self.__add__(-other)
    
    def __cmp__(self, other):
        if isinstance(other, Infinity):
            d_cmp = cmp(self.direction, other.direction)
            if d_cmp != 0:
                return d_cmp
            else:
                raise InfinityRaceError
        elif is_floatable(other):
            return self.direction
        else:
            raise NotImplementedError
    def __div__(self, other):
        if isinstance(other, Infinity):
            raise InfinityRaceError
        elif is_floatable(other):
            s = math_tools.sign(other)
            if s==0:
                raise InfinityRaceError
            else:
                return Infinity(direction=self.direction * s)
            
    def __float__(self):
        raise ValueError("Can't convert infinite number to float")
    
    def __mul__(self, other):
        if isinstance(other, Infinity):
            return Infinity(self.direction * other.direction)
        elif is_floatable(other):
            s = math_tools.sign(other)
            if s==0:
                raise InfinityRaceError
            else:
                return Infinity(direction=self.direction * s)
            
    def __neg__(self):
        return Infinity(-self.direction)
    
    def __nonzero__(self):
        return True
    
    def __pos__(self):
        return self
    
    def __pow__(self, other):
        if isinstance(other, Infinity):
            raise object # todo
        elif is_floatable(other):
            s = math_tools.sign(other)
            if s==0:
                raise InfinityRaceError
            else:
                if self.direction==1:
                    if s==1:
                        return self
                    if s==-1:
                        return 0
                else: #self.direction == -1
                    if is_nonfractional(other):
                        if s==-1:
                            return 0
                        if s==1:
                            if s % 2 == 0:                                
                                return Infinity()
                            else:                    
                                return Infinity(-1)                            
                    else: # is_nonfractional(other) is False
                        raise ValueError("Negative number cannot be raised "
                                         "to a fractional power")            
          
                
    def __rpow__(self, other):
        if isinstance(other, Infinity):
            return other.__pow__(self)
        elif not is_floatable(other):
            raise NotImplementedError
        else: # is_floatable(number) is True
            raise NotImplementedError # todo
        
    def __radd__(self, other):
        return self.__add__(other)
    
    def __rsub__(self, other):
        return ( - self.__sub__(other))
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    __truediv__ = __floordiv__ = __div__
    
    def __eq__(self, other):

        if isinstance(other, Infinity):
            return other.direction == self.direction
        
        elif isinstance(other, float):
            # We're checking to see if `other` is equal to `float('inf')` or
            # `-float('inf')`. But we must `try` it carefully, because in Python
            # 2.5 there is no `float('inf')`.
            #
            # Todo: It seems this takes precedence over `float.__eq__`,
            # fortunately. How come this happens?
            try:
                float_inf = float('inf')
            except ValueError:
                return False
            
            if other == float_inf:
                return self.direction == 1
            elif other == -float_inf:
                return self.direction == -1
            else:
                return False
            
        else: # `other` is not any kind of infinity
            return False
        
    
    def __neq__(self, other):
        return not self.__eq__(other)
    
    def __repr__(self):
        if self.direction==1:
            suffix=''
        else: # self.direction == -1
            suffix='-'
        return suffix + 'infinity'
        

infinity = Infinity()


