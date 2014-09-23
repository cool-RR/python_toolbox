import abc
import builtins
import types
import collections
import numbers

from python_toolbox import caching

from .misc import CuteSequence

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

        if start in infinities:
            raise TypeError(
                "Can't have `start=%s` because then what would the first item "
                "be, %s? And the second item, %s + 1? No can do." %
                (start, start)
            )
        if step in infinities:
            raise TypeError(
                "Can't have `step=%s` because then what would the second item "
                "be, %s? No can do." % (step, step)
            )
            
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


class CuteRangeType(abc.ABCMeta):
    '''Metaclass for `CuteRange`, see its docstring for details.'''
    def __call__(cls, *args, _avoid_built_in_range=False):
        # Our job here is to decide whether to instantiate using the built-in
        # `range` or our kickass `Range`.
        from python_toolbox import math_tools
        
        if (cls is CuteRange) and (not _avoid_built_in_range):
            start, stop, step = parse_range_args(*args)
            
            use_builtin_range = True # Until challenged.
            
            if not all(map(_is_integral_or_none, (start, stop, step))):
                # If any of `(start, stop, step)` are not integers or `None`, we
                # definitely need `Range`.
                use_builtin_range = False
                
            if (step > 0 and stop == infinity) or \
                                            (step < 0 and stop == (-infinity)):
                # If the range of numbers is infinite, we sure as shit need
                # `Range`.
                use_builtin_range = False
                    
            if use_builtin_range:
                return range(*args)
            else:
                return super().__call__(*args)
        
        else: # (cls is not Range) or _avoid_built_in_range
            return super().__call__(*args)
        

class CuteRange(CuteSequence, metaclass=CuteRangeType):
    '''
    Improved version of Python's `range` that has extra features.
    
    `CuteRange` is like Python's built-in `range`, except (1) it's cute and (2)
    it's completely different. LOL, just kidding.
    
    `CuteRange` takes start, stop and step arguments just like `range`, but it
    allows you to use floating-point numbers (or decimals), and it allows you
    to use infinite numbers to produce infinite ranges.
    
    
    
    '''
    def __init__(self, *args):
        self.start, self.stop, self.step = parse_range_args(*args)
        
    _reduced = property(lambda self: (type(self), (self.start, self.stop,
                                                   self.step)))
    
    __hash__ = lambda self: hash(self._reduced)
        
    __eq__ = lambda self, other: (isinstance(other, CuteRange) and
                                  (self._reduced == other._reduced))
    
    distance_to_cover = caching.CachedProperty(lambda self:
                                                        self.stop - self.start)
    
    @caching.CachedProperty
    def length(self):
        '''
        The length of the `CuteRange`.
        
        We're using a property `.length` rather than the built-in `__len__`
        because `__len__` can't handle infinite values or floats.
        '''
        from python_toolbox import math_tools
        
        if math_tools.get_sign(self.distance_to_cover) != \
                                                math_tools.get_sign(self.step):
            return 0
        else:
            raw_length, remainder = math_tools.cute_divmod(
                self.distance_to_cover, self.step
            )
            raw_length += (remainder != 0)
            return raw_length
    
    __repr__ = lambda self: self._repr
        
        
    @caching.CachedProperty
    def _repr(self):
        return '%s(%s%s%s)' % (
            type(self).__name__,
            '%s, ' % self.start,
            '%s' % self.stop, 
            (', %s' % self.step) if self.step != 1 else '',
        )
        
        
    
    def __getitem__(self, i, allow_out_of_range=False):
        from python_toolbox import sequence_tools
        if isinstance(i, numbers.Integral):
            if i < 0:
                if i < (-self.length) and not allow_out_of_range:
                    raise IndexError
                i += self.length
            if 0 <= i < self.length or allow_out_of_range:
                return self.start + (self.step * i)
            else:
                raise IndexError
        elif i == infinity:
            if self.length == infinity:
                return self.stop
            else:
                raise IndexError
        elif i == -infinity:
            raise IndexError
        elif isinstance(i, (slice, sequence_tools.CanonicalSlice)):
            canonical_slice = sequence_tools.CanonicalSlice(
                i, iterable_or_length=self
            )
            if not ((0 <= canonical_slice.start < self.length) and
                    ((0 <= canonical_slice.stop <= self.length) or
                     (canonical_slice.stop == self.length == infinity))):
                raise TypeError
            return CuteRange(
                self[canonical_slice.start],
                self.__getitem__(canonical_slice.stop,
                                 allow_out_of_range=True),
                self.step * canonical_slice.step
            )
        else:
            raise TypeError
        
    def __len__(self):
        # Sadly Python doesn't allow infinity or floats here.
        return self.length if isinstance(self.length, numbers.Integral) else 0
        
    def index(self, i):
        from python_toolbox import math_tools
        if not isinstance(i, numbers.Number):
            raise ValueError
        else:
            distance = i - self.start
            if distance == 0 and self:
                return True
            if math_tools.get_sign(distance) != math_tools.get_sign(self.step):
                raise ValueError
            index, remainder = math_tools.cute_divmod(distance, self.step)
            if remainder == 0 and (0 <= index < self.length or
                                             index == self.length == infinity):
                return index
            else:
                raise ValueError
            
    is_infinity = caching.CachedProperty(lambda self: self.length == infinity)
        
    
CuteRange.register(range)