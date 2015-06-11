# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import collections

from python_toolbox import nifty_collections
from python_toolbox import caching
from python_toolbox import sequence_tools

infinity = float('inf')


        
class MapSpace(sequence_tools.CuteSequenceMixin, collections.Sequence):
    '''
    A space of a function applied to a sequence.
    
    This is similar to Python's builtin `map`, except that it behaves like a
    sequence rather than an iterable. (Though it's also iterable.) You can
    access any item by its index number.
    
    Example:
    
        >>> map_space = MapSpace(lambda x: x ** 2, range(7))
        >>> map_space
        MapSpace(<function <lambda> at 0x00000000030C1510>, range(0, 7))
        >>> len(map_space)
        7
        >>> map_space[3]
        9
        >>> tuple(map_space)
        (0, 1, 4, 9, 16, 25, 36)
    
    '''    
    def __init__(self, function, sequence):
        
        self.function = function
        self.sequence = sequence_tools.ensure_iterable_is_immutable_sequence(
            sequence,
            default_type=nifty_collections.LazyTuple
        )
    
    
    length = caching.CachedProperty(
        lambda self: sequence_tools.get_length(self.sequence)
    )
        
    def __repr__(self):
        return '%s(%s, %s)' % (
            type(self).__name__,
            self.function,
            self.sequence
        )
        
    def __getitem__(self, i):
        if isinstance(i, slice):
            return type(self)(self.function, self.sequence[i])
        assert isinstance(i, int)
        return self.function(self.sequence[i]) # Propagating `IndexError`.
        
    
    def __iter__(self):
        for item in self.sequence:
            yield self.function(item)
        
    _reduced = property(
        lambda self: (type(self), self.function, self.sequence)
    )
             
    __eq__ = lambda self, other: (isinstance(other, MapSpace) and
                                  self._reduced == other._reduced)
    __hash__ = lambda self: hash(self._reduced)
    
    __bool__ = lambda self: bool(self.sequence)
        


