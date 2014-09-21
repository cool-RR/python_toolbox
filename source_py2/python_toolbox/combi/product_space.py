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

from python_toolbox import math_tools
from python_toolbox import sequence_tools
from python_toolbox import cute_iter_tools
from python_toolbox import nifty_collections

from . import misc
from python_toolbox import misc_tools

infinity = float('inf')


        
class ProductSpace(sequence_tools.CuteSequenceMixin, collections.Sequence):
    def __init__(self, sequences):
        self.sequences = sequence_tools. \
                               ensure_iterable_is_immutable_sequence(sequences)
        self.sequence_lengths = tuple(map(sequence_tools.get_length,
                                          self.sequences))
        self.length = math_tools.product(self.sequence_lengths)
        
    def __repr__(self):
        return '<%s: %s>' % (
            type(self).__name__,
            ' * '.join(str(sequence_tools.get_length(sequence))
                       for sequence in self.sequences),
        )
        
    def __getitem__(self, i):
        if isinstance(i, slice):
            raise NotImplementedError
        
        if i < 0:
            i += self.length
            
        if not (0 <= i < self.length):
            raise IndexError
        
        wip_i = i
        reverse_indices = []
        for sequence_length in reversed(self.sequence_lengths):
            wip_i, current_index = divmod(wip_i, sequence_length)
            reverse_indices.append(current_index)
        assert wip_i == 0
        return tuple(sequence[index] for sequence, index in
                     zip(self.sequences, reversed(reverse_indices)))
    
        
    _reduced = property(lambda self: (type(self), self.sequences))
    __hash__ = lambda self: hash(self._reduced)
    __eq__ = lambda self, other: (isinstance(other, ProductSpace) and
                                  self._reduced == other._reduced)
    
    def index(self, given_sequence):
        if not isinstance(given_sequence, collections.Sequence) or \
                                not len(given_sequence) == len(self.sequences):
            raise ValueError
        
        reverse_indices = []
        current_radix = 1
        
        wip_index = 0
            
        for item, sequence in reversed(tuple(zip(given_sequence,
                                                 self.sequences))):
            wip_index += current_radix * sequence.index(item)
            # (Propagating `ValueError`.)
            current_radix *= sequence_tools.get_length(sequence)
            
        return wip_index
    
    
    __bool__ = lambda self: bool(self.length)
        


