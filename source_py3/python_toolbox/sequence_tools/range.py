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
        (stop,) = args
        if stop == -infinity: raise TypeError
        elif stop is None: stop = infinity
        return (0, stop, 1)
    
    elif len(args) == 2:
        (start, stop) = args
        
        if start in infinities: raise TypeError
        elif start is None: start = 0

        if stop == -infinity: raise TypeError
        elif stop is None: stop = infinity
        
        return (start, stop, 1)
    
    else:
        assert len(args) == 3
        (start, stop, step) = args
        
        if step == 0: raise TypeError

        if start in infinities: raise TypeError
        elif start is None: start = 0
        
        elif step > 0:
                
            if stop == -infinity: raise TypeError
            elif stop is None: stop = infinity
            
        else:
            assert step < 0
        
            if stop == infinity: raise TypeError
            elif stop is None: stop = (-infinity)
            
            
        return (start, stop, step)
    

def _is_integral_or_none(thing):
    return isinstance(thing, (numbers.Integral, NoneType))


class RangeType(abc.ABCMeta):
    def __call__(cls, *args):
        from python_toolbox import math_tools
        if cls is Range:
            start, stop, step = parse_range_args(*args)
            cls_to_use = range # Until challenged.
            if not all(map(_is_integral_or_none, (start, stop, step))):
                cls_to_use = Range
                
            if (step > 0 and stop == infinity) or \
                                            (step < 0 and stop == (-infinity)):
                cls_to_use = Range
                    
            return super().__call__(cls_to_use, *args)
        
        else:
            return super().__call__(cls, *args)
        

class Range(collections.Sequence, metaclass=RangeType):
    def __init__(self, *args):
        self.start, self.stop, self.step = parse_range_args(*args)
        
    _reduced = property(lambda self: (type(self), (self.start, self.stop,
                                                   self.end)))
        
    __eq__ = lambda self, other: (isinstance(other, Range) and
                                  (self._reduced == other._reduced))
    
    @caching.CachedProperty
    def length(self):
        from python_toolbox import math_tools
        distance_to_cover = self.stop - self.start
        if math_tools.get_sign(distance_to_cover) != \
                                                math_tools.get_sign(self.step):
            return 0
        else:
            raw_length, remainder = divmod(distance_to_cover, self.step)
            raw_length += (remainder != 0)
            return raw_length
    
    __repr__ = lambda self: '%s(%s)' % (type(self).__name__, self.start)
    
    def __getitem__(self, i):
        from python_toolbox import sequence_tools
        if isinstance(i, numbers.Integral):
            if 0 <= i < self.length:
                return self.start + (self.step * i)
            else:
                raise IndexError
        elif isinstance(i, (slice, sequence_tools.CanonicalSlice)):
            canonical_slice = sequence_tools.CanonicalSlice(
                i, iterable_or_length=self
            )
            if not (0 <= canonical_slice.start < self.length and
                    0 <= canonical_slice.stop < self.length):
                raise TypeError
            return Range(
                self[canonical_slice.start],
                self[canonical_slice.stop],
                self.step * canonical_slice.step
            )
        else:
            raise TypeError
        
    def __len__(self):
        # Sadly Python doesn't allow infinity here.
        return self.length if (self.length not in infinities) else 0
        
    def __contains__(self, i):
        
        if not isinstance(i, numbers.Number):
            return False
        
        
    __contains__ = lambda self, i: (isinstance(i, numbers.Integral) and
                                    i >= self.start)
    def index(self, i):
        if not isinstance(i, numbers.Integral) or not i >= self.start:
            raise ValueError
        else:
            return i - self.start
        
    
Range.register(range)