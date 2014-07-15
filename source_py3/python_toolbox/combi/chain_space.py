import collections
import types
import sys
import math
import numbers

from python_toolbox import misc_tools
from python_toolbox import binary_search
from python_toolbox import dict_tools
from python_toolbox import nifty_collections
from python_toolbox import caching

from layout_rabbit import shy_math_tools
from layout_rabbit import shy_sequence_tools
from layout_rabbit import shy_cute_iter_tools
from layout_rabbit import shy_nifty_collections

from . import misc
from layout_rabbit import shy_misc_tools

infinity = float('inf')


        
class ChainSpace(shy_sequence_tools.CuteSequenceMixin, collections.Sequence):
    '''
    A space of sequences chained together.
    
    This is similar to `itertools.chain`, except that items can be fetched by
    index number rather than just iteration.
    '''
    def __init__(self, sequences):
        
        self.sequences = nifty_collections.LazyTuple(
            (shy_sequence_tools.ensure_iterable_is_immutable_sequence(
                sequence, default_type=nifty_collections.LazyTuple)
                                                     for sequence in sequences)
        )
    
    
    @caching.CachedProperty
    @nifty_collections.LazyTuple.factory()
    def accumulated_lengths(self):
        '''
        A sequence of the accumulated length as every sequence is added.
        
        For example, if this chain space has sequences with lengths of 10, 100
        and 1000, this would be `[0, 10, 110, 1110]`.
        '''
        total = 0
        yield 0
        for sequence in self.sequences:
            total += shy_sequence_tools.get_length(sequence)
            yield total
        
        
    length = caching.CachedProperty(lambda self: self.accumulated_lengths[-1])
        
        
    def __repr__(self):
        return '<%s: %s>' % (
            type(self).__name__,
            '+'.join(str(len(sequence)) for sequence in sequences),
        )
        
    def __getitem__(self, i):
        if isinstance(i, slice):
            raise NotImplementedError
        assert isinstance(i, int)
        sequence_index = binary_search.binary_search_by_index(
            self.accumulated_lengths, lambda x: x,
            i, rounding=binary_search.LOW_IF_BOTH
        )
        if sequence_index is None:
            raise IndexError
        sequence_start = self.accumulated_lengths[sequence_index]
        return self.sequences[sequence_index][i - sequence_start]
        
    
    def __iter__(self):
        for sequence in self.sequences:
            # yield from sequence Commenting for fucking Pypy
            for i in sequence: yield i
        
    _reduced = property(lambda self: (type(self), self.sequences))
             
    __eq__ = lambda self, other: (isinstance(other, ChainSpace) and
                                  self._reduced == other._reduced)
    
    def __contains__(self, item):
        return any(item in sequence for sequence in self.sequences
                   if (not isinstance(sequence, str) or isinstance(item, str)))
        
    def index(self, item):
        for sequence, accumulated_length in zip(self.sequences,
                                                self.accumulated_lengths):
            try:
                return sequence.index(item) + accumulated_length
            except IndexError:
                pass
        else:
            raise IndexError
    
    def __bool__(self):
        try:
            next(iter(self))
        except StopIteration:
            return False
        else:
            return True
        


