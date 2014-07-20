import abc
import builtins
import types
import collections
import numbers

infinity = float('inf')
infinities = (infinity, -infinity)

NoneType = type(None)

def parse_range_args(*args):
    assert 0 <= len(args) <= 3
    if len(args) == 0:
        return (0, infinity, 1)
    elif len(args) == 1:
        return (0, args[0], 1)
    elif len(args) == 2:
        return (args[0], args[1], 1)
    else:
        assert len(args) == 3
        return (args[0], args[1], args[3])
    

def _is_integral_or_infinite_or_none(thing):
    return isinstance(thing, (math_tools.PossiblyInfiniteIntegral, NoneType))


class RangeType(abc.ABCMeta):
    def __call__(cls, *args):
        from python_toolbox import math_tools
        if cls is Range:
            start, stop, step = parse_range_args(*args)
            if not all(map(_is_integral_or_infinite_or_none,
                           (start, stop, step))):
                cls_to_use = Range
            if 
                
        else:
            cls_to_use = cls
        return super().__call__(cls_to_use, *args)
        

class Range(collections.Sequence, metaclass=RangeType):
    def __init__(self, *args):
        assert isinstance(start, numbers.Integral)
        self.start = start
        
    _reduced = property(lambda self: (type(self), self.start))
        
    __eq__ = lambda self, other: (isinstance(other, Range) and
                                  (self._reduced == other._reduced))
    
    def __iter__(self):
        i = self.start
        while True:
            yield i
            i += 1
        
    __repr__ = lambda self: '%s(%s)' % (type(self).__name__, self.start)
    
    def __getitem__(self, i):
        if isinstance(i, numbers.Integral):
            return self.start + i
        else:
            assert isinstance(i, slice)
            if i.step is not None:
                raise NotImplementedError # Easy to implement if I needed it.
            assert i.start is None or i.start >= 0
            start = 0 if i.start is None else i.start
            if i.stop == infinity:
                return Range(self.start + start)
            else:
                return range(self.start + start, self.start + i.stop)
                
            
        
    __len__ = lambda self: 0 # Sadly Python doesn't allow infinity here.
    __contains__ = lambda self, i: (isinstance(i, numbers.Integral) and
                                    i >= self.start)
    def index(self, i):
        if not isinstance(i, numbers.Integral) or not i >= self.start:
            raise IndexError
        else:
            return i - self.start
        
    
Range.register(range)