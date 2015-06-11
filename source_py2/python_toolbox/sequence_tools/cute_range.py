# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import abc
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



class CuteRange(CuteSequence):
    '''
    Improved version of Python's `range` that has extra features.
    
    `CuteRange` is like Python's built-in `range`, except (1) it's cute and (2)
    it's completely different. LOL, just kidding.
    
    `CuteRange` takes `start`, `stop` and `step` arguments just like `range`,
    but it allows you to use floating-point numbers (or decimals), and it
    allows you to use infinite numbers to produce infinite ranges.
    
    Obviously, `CuteRange` allows iteration, index access, searching for a
    number's index number, checking whether a number is in the range or not,
    and slicing.
    
    Examples:
    
        `CuteRange(float('inf'))` is an infinite range starting at zero and
        never ending.
        
        `CuteRange(7, float('inf'))` is an infinite range starting at 7 and
        never ending. (Like `itertools.count(7)` except it has all the
        amenities of a sequence, you can get items using list notation, you can
        slice it, you can get index numbers of items, etc.)
    
        `CuteRange(-1.6, 7.3)` is the finite range of numbers `(-1.6, -0.6,
        0.4, 1.4, 2.4, 3.4, 4.4, 5.4, 6.4)`.
        
        `CuteRange(10.4, -float('inf'), -7.1)` is the infinite range of numbers
        `(10.4, 3.3, -3.8, -10.9, -18.0, -25.1, ... )`.

    '''
    def __init__(self, *args):
        self.start, self.stop, self.step = parse_range_args(*args)
        
    _reduced = property(lambda self: (type(self), (self.start, self.stop,
                                                   self.step)))
    
    __hash__ = lambda self: hash(self._reduced)
        
    __eq__ = lambda self, other: (type(self) == type(other) and
                                  (self._reduced == other._reduced))
    __ne__ = lambda self, other: not self == other
    
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
        
        
    @caching.CachedProperty
    def short_repr(self):
        '''
        A shorter representation of the `CuteRange`.
        
        This is different than `repr(cute_range)` only in cases where `step=1`.
        In these cases, while `repr(cute_range)` would be something like
        `CuteRange(7, 20)`, `cute_range.short_repr` would be `7..20`.
        '''
        if self.step != 1:
            return self._repr
        else:
            return '%s..%s' % (self.start, self.stop - 1)
        
    
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
            if not ((0 <= canonical_slice.start <= self.length) and
                    ((0 <= canonical_slice.stop <= self.length) or
                     (canonical_slice.stop == self.length == infinity))):
                raise TypeError
            return CuteRange(
                self.__getitem__(canonical_slice.start,
                                 allow_out_of_range=True),
                self.__getitem__(canonical_slice.stop,
                                 allow_out_of_range=True),
                self.step * canonical_slice.step
            )
        else:
            raise TypeError
        
    def __len__(self):
        # Sadly Python doesn't allow infinity or floats here.
        return self.length if isinstance(self.length, numbers.Integral) else 0
        
    def index(self, i, start=-infinity, stop=infinity):
        '''Get the index number of `i` in this `CuteRange`.'''
        from python_toolbox import math_tools
        if not isinstance(i, numbers.Number):
            raise ValueError
        else:
            distance = i - self.start
            if distance == 0 and self:
                if start <= 0 < stop: return 0
                else: raise ValueError("Found but not within range.")
            if math_tools.get_sign(distance) != math_tools.get_sign(self.step):
                raise ValueError
            index, remainder = math_tools.cute_divmod(distance, self.step)
            if remainder == 0 and (0 <= index < self.length or
                                             index == self.length == infinity):
                if start <= index < stop: return index
                else: raise ValueError("Found but not within range.")

            else:
                raise ValueError
            
    is_infinite = caching.CachedProperty(lambda self: self.length == infinity)
        
    
CuteRange.register(xrange)