import abc
import collections

infinity = float('inf')
infinities = (infinity, -infinity)

def parse_range_args(*args, **kwargs):
    # We allow either `args` or `kwargs`, not both:
    assert not (args and kwargs)
    
    if kwargs:
        assert set(kwargs.keys()) in ('start', 'stop', 'set')
        
    assert 0 <= len(args) <= 3
    if len(args) == 0:
        return (0, infinity, 1)
    elif len(args) == 1:
        return (0, infinity, 1)
    
    
    


class RangeType(abc.ABCMeta):
    def __call__(cls, *args):
        if cls is Range:
        else:
            super().__call__(cls, *args)
        
        
        

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