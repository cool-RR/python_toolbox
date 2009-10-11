
def sign(x):
    if x > 0: return 1
    if x < 0: return -1
    return 0

def is_floatable(x):
    try:
        float(x)
        return True
    except:
        return False

def is_nonfractional(x):
    try:
        int(x)
        return int(x) == x
    except:
        return False
    
class InfinityRaceError(Exception):
    pass

class InfinityError(Exception):
    pass

class InfinityClass(object):
    def __init__(self, direction=1):
        self.direction = direction
    def __abs__(self):
        return Infinity
    def __add__(self, other):
        if isinstance(other, InfinityClass):
            if self.direction == other.direction:
                return self
            else:
                raise InfinityRaceError
        elif is_floatable(other):
            return self
    def __sub__(self, other):
        return self.__add__(-other)
    def __cmp__(self, other):
        if isinstance(other, InfinityClass):
            d_cmp = cmp(self.direction, other.direction)
            if d_cmp == 0:
                return d_cmp
            else:
                raise InfinityRaceError
        elif is_floatable(other):
            return self.direction
        else:
            raise NotImplementedError
    def __div__(self, other):
        if isinstance(other, InfinityClass):
            raise InfinityRaceError
        elif is_floatable(other):
            s = sign(other)
            if s==0:
                raise InfinityRaceError
            else:
                return InfinityClass(direction=self.direction * s)
    def __float__(self):
        raise ValueError("Can't convert infinite number to float")
    def __mul__(self, other):
        if isinstance(other, InfinityClass):
            return InfinityClass(self.direction * other.direction)
        elif is_floatable(other):
            s = sign(other)
            if s==0:
                raise InfinityRaceError
            else:
                return InfinityClass(direction=self.direction * s)
    def __neg__(self):
        return InfinityClass(-self.direction)
    def __nonzero__(self):
        return True
    def __pos__(self):
        return self
    def __pow__(self, other):
        if isinstance(other, InfinityClass):
            raise object # todo
        elif is_floatable(other):
            s = sign(other)
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
                                return InfinityClass()
                            else:                    
                                return InfinityClass(-1)                            
                    else: # is_nonfractional(other) is False
                        raise ValueError(""""negative number cannot be raised
to a fractional power""")            
          
            
                
    def __rpow__(self, other):
        if isinstance(other, InfinityClass):
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
        return isinstance(other, InfinityClass) and \
               other.direction == self.direction
    def __neq__(self, other):
        return not self.__eq__(other)
    
    def __repr__(self):
        if self.direction==1:
            suffix=''
        else: # self.direction == -1
            suffix='-'
        return suffix + 'Infinity'
        

Infinity = InfinityClass()