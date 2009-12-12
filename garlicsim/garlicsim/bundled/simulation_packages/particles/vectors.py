'''tododoc'''

from __future__ import division

import math
import itertools



class VectorError(Exception):
    pass


class Vector(object):
    
    def __init__(self, list_):
        self.__list = list(list_)
        
    def __add__(self, other):
        if isinstance(other, Vector) is False:
            raise VectorError("right hand side is not a vector")
        return Vector((x + y for (x, y) in itertools.izip(self.__list, other.__list)))

    def __neg__(self):
        return Vector(-x for x in self.__list)

    def __pos__(self):
        return self

    def __sub__(self, other):
        if isinstance(other, Vector) is False:
            raise VectorError("right hand side is not a vector")
        return Vector((x - y for (x, y) in itertools.izip(self.__list, other.__list)))

    def __mul__(self, other):        
        return Vector(x * other for x in self.__list)

    def __rmul__(self, other):
        return (self*other)

    def __div__(self, other):
        return Vector(x / other for x in self.__list)

    def __rdiv__(self, other):
        raise VectorError("you sick pervert! you tried to divide something by a vector!")

    def __and__(self, other):
        """
        This is a dot product, done like this: a&b
        must use () around it because of fucked up operator precedence.
        """
        if isinstance(other, Vector) is False:
            raise VectorError("trying to do dot product of vector with non-vector")
        
        return sum((x * y for (x, y) in itertools.izip(self.__list, other.__list)))

    def __rand__(self,other):
        return (self & other)

    def __or__(self,other):
        """
        cross product, defined only for 3D vectors. goes like this: a|b
        don't try this on non-3d vectors. must use () around it because of fucked up operator precedence.
        """
        a = self
        b = other
        
        assert a.dim() == b.dim() == 3
        return Vector([a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]])

    def __ror__(self,other):
        return -(self|other)

    def __abs__(self): 
        return math.sqrt(sum((x * x for x in self.__list)))
    

    def __iadd__(self, other):
        self = self + other
        return self

    def __isub__(self, other):
        self = self - other
        return self

    def __imul__(self, other):
        self = self * other
        return self

    def __idiv__(self, other):
        self = self / other
        return self

    def __iand__(self, other):
        raise VectorError("please don't do &= with my vectors, it confuses me")

    def __ior__(self, other):
        self = (self|other)
        return self

    
    def __iter__(self):
        return self.__list.__iter__()

    def normalized(self):
        """
        gives the vector, normalized
        """
        return (self / abs(self))
    
    def dim(self):
        return len(self.__list)

    def copy(self):
        return Vector(self)

    def __getitem__(self, *args, **kwargs):
        return self.__list.__getitem__(*args, **kwargs)
    
    def __repr__(self):
        
        return 'Vector(' + repr(self.__list) + ')'
    
################################################################################################

def zeros(n):
    """
    Returns a zero vector of length n.
    """
    return Vector(map(lambda x: 0., range(n)))

def ones(n):
    """
    Returns a vector of length n with all ones.
    """
    return Vector(map(lambda x: 1., range(n)))
