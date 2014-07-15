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


        
class SelectionSpace(shy_sequence_tools.CuteSequenceMixin,
                     collections.Sequence):
    def __init__(self, sequence, n):
        self.sequence = \
             shy_sequence_tools.ensure_iterable_is_immutable_sequence(sequence)
        self.length = 2 ** len(self.sequence)
        
        
    def __repr__(self):
        return '<%s: %s>' % (
            type(self).__name__,
            self.sequence
        )
        
    def __getitem__(self, i):
        if isinstance(i, slice):
            raise NotImplementedError
        
        if not (0 <= i < self.length):
            raise IndexError
        
        pattern = '{0:0%sb}' % self.length
        binary_i = pattern.format(i)
        
        assert len(binary_i) == len(self.sequence)
        
        return tuple(item for (is_included, item) in
                     zip(binary_i, self.sequence) if is_included)
        
        
    _reduced = property(lambda self: (type(self), self.sequence))
             
    __eq__ = lambda self, other: (isinstance(other, SelectionSpace) and
                                  self._reduced == other._reduced)
    
    # def __contains__(self, given_sequence):
        # try:
            # self.index(given_sequence)
        # except IndexError:
            # return False
        # else:
            # return True
        
    # def index(self, given_sequence):
        # if not isinstance(given_sequence, collections.Sequence) or \
                                # not len(given_sequence) == len(self.sequences):
            # raise IndexError
        
        # reverse_indices = []
        # current_radix = 1
        
        # wip_index = 0
            
        # for item, sequence in reversed(tuple(zip(given_sequence, self.sequences))):
            # wip_index += sequence.index(item) # Propagating `IndexError`
            # current_radix *= misc.get_length(sequence)
            
        # return wip_index
    
    
    # __bool__ = lambda self: bool(self.length)
        


