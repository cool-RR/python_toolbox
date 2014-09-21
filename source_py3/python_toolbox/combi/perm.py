import functools
import abc
import collections
import itertools
import types
import sys
import math
import numbers

from python_toolbox import misc_tools
from python_toolbox import dict_tools
from python_toolbox import nifty_collections
from python_toolbox import decorator_tools
from python_toolbox import caching

from python_toolbox import math_tools
from python_toolbox import sequence_tools
from python_toolbox import cute_iter_tools
from python_toolbox import misc_tools

from . import misc


infinity = float('inf')


class _BasePermView:
    def __init__(self, perm):
        self.perm = perm
    __repr__ = lambda self: '<%s: %s>' % (type(self).__name__, self.perm)


class PermItems(sequence_tools.CuteSequenceMixin, _BasePermView,
                collections.Sequence):
    def __getitem__(self, i):
        return (self.perm.domain[i], self.perm._perm_sequence[i])
    

class PermAsDictoid(sequence_tools.CuteSequenceMixin, _BasePermView,
                    collections.Mapping):
    def __getitem__(self, key):
        return self.perm[key]
    def __iter__(self):
        return iter(self.perm.domain)
        
    

class PermType(abc.ABCMeta):
    def __call__(cls, item, perm_space=None):
        if cls == Perm and isinstance(perm_space, CombSpace):
            cls = Comb
        return super(PermType, cls).__call__(item, perm_space)
        

@functools.total_ordering
class Perm(sequence_tools.CuteSequenceMixin, collections.Sequence,
           metaclass=PermType):
    
    @classmethod
    def coerce(cls, item, perm_space=None):
        if isinstance(item, Perm) and (perm_space is not None) and \
           (item.just_dapplied_rapplied_perm_space
                                        == perm_space._just_dapplied_rapplied):
            return item
        else:
            return cls(item, perm_space)
    
    
    def __init__(self, number_or_perm_sequence, perm_space=None):
        '''
        
        Not supplying `perm_space` is allowed only if given either a number (in
        which case a pure infinite perm space will be assumed) or a sequence of
        natural numbers.
        '''
        perm_space = None if perm_space is None \
                                              else PermSpace.coerce(perm_space)
        if isinstance(number_or_perm_sequence, collections.Iterable):
            number_or_perm_sequence = sequence_tools. \
                 ensure_iterable_is_immutable_sequence(number_or_perm_sequence)
        assert isinstance(number_or_perm_sequence, (numbers.Integral,
                                                    collections.Sequence))
        
        ### Analyzing `perm_space`: ###########################################
        #                                                                     #
        if perm_space is None:
            self.is_rapplied = self.is_dapplied = self.is_partial = \
                                                    self.is_combination = False
            if not isinstance(number_or_perm_sequence,
                              collections.Sequence):
                raise Exception(
                    "You tried creating a `Perm` using a number instead of a "
                    "sequence and without specifying `PermSpace`, so we have "
                    "no way of knowing which `PermSpace` to use."
                )
            # We're assuming that `number_or_perm_sequence` is a pure
            # permutation sequence. Not asserting this because that would
            # be O(n).
            self.just_dapplied_rapplied_perm_space = \
                                        PermSpace(len(number_or_perm_sequence))
        else: # perm_space is not None
            self.is_rapplied = perm_space.is_rapplied
            self.is_dapplied = perm_space.is_dapplied
            self.is_partial = perm_space.is_partial
            self.is_combination = perm_space.is_combination
            self.just_dapplied_rapplied_perm_space = \
                                          perm_space.unsliced.undegreed.unfixed
        #                                                                     #
        ### Finished analyzing `perm_space`. ##################################
        
        self.is_pure = not (self.is_rapplied or self.is_dapplied
                            or self.is_partial or self.is_combination)
        
        if not self.is_rapplied: self.unrapplied = self
        if not self.is_dapplied: self.undapplied = self
        if not self.is_combination: self.uncombinationed = self
        
        if isinstance(number_or_perm_sequence, numbers.Integral):
            if not (0 <= number_or_perm_sequence <
                                self.just_dapplied_rapplied_perm_space.length):
                raise Exception(
                    "You're creating a `Perm` with number %s, but the chosen "
                    "`PermSpace` only goes from 0 up to %s." % (
                        number_or_perm_sequence,
                        self.just_dapplied_rapplied_perm_space.length - 1
                    )
                )
                
            self.number = number_or_perm_sequence
        else:
            assert isinstance(number_or_perm_sequence, collections.Iterable)
            self._perm_sequence = sequence_tools. \
                 ensure_iterable_is_immutable_sequence(number_or_perm_sequence)
            
        assert self.is_combination == isinstance(self, Comb)
            
            
    _reduced = property(lambda self: (
        type(self), self.number,
        self.just_dapplied_rapplied_perm_space.length)
    )
            
    __int__ = lambda self: self.number
    __mod__ = lambda self, other: self.number % other
    __iter__ = lambda self: iter(self._perm_sequence)
    
    __eq__ = lambda self, other: (isinstance(other, Perm) and
                                  self._reduced == other._reduced)
    __ne__ = lambda self, other: not (self == other)
    __hash__ = lambda self: hash(self._reduced)
    __bool__ = lambda self: bool(self._perm_sequence)
    
    def __contains__(self, item):
        try:
            return (item in self._perm_sequence)
        except TypeError:
            # Gotta have this `except` because Python complains if you try `1
            # in 'meow'`.
            return False
    
    def __repr__(self):
        return '<%s%s%s: (%s / %s) %s(%s%s)>' % (
            type(self).__name__, 
            (', n_elements=%s' % len(self)) if self.is_partial else '',
            ', is_combination=True' if self.is_combination else '',
            self.number,
            self._perm_space_short_length_string,
            ('(%s) => ' % ', '.join(map(repr, self.domain)))
                                                   if self.is_dapplied else '',
            ', '.join(repr(item) for item in self),
            ',' if self.length == 1 else ''
        )
        
    def index(self, member):
        numerical_index = self._perm_sequence.index(member)
        return self.just_dapplied_rapplied_perm_space. \
               domain[numerical_index] if self.is_dapplied else numerical_index
        
        
    
    @caching.CachedProperty
    def _perm_space_short_length_string(self):
        if self.is_partial or self.is_combination:
            return str(self.just_dapplied_rapplied_perm_space.length)
        else:
            return misc.get_short_factorial_string(
                self.just_dapplied_rapplied_perm_space.sequence_length,
            )
            
    
    
    @caching.CachedProperty
    def number(self):
        '''
        
        The number here is not necessarily the number with which the perm was
        fetched from the perm space; it's the number of the perm in a perm
        space that is neither degreed, fixed or sliced.
        '''
        if self.is_rapplied or self.is_dapplied:
            return self.unrapplied.undapplied.number
        
        factoradic_number = []
        unused_numbers = list(self.just_dapplied_rapplied_perm_space.
                                                                  sequence)
        for i, number in enumerate(self):
            index_of_current_number = unused_numbers.index(number)
            factoradic_number.append(index_of_current_number)
            del unused_numbers[index_of_current_number]
        return math_tools.from_factoradic(
            factoradic_number +
            [0] * self.just_dapplied_rapplied_perm_space.n_unused_elements
        ) // math.factorial(
                  self.just_dapplied_rapplied_perm_space.n_unused_elements)
            
    
    @caching.CachedProperty
    def _perm_sequence(self):
        assert (0 <= self.number < 
                                 self.just_dapplied_rapplied_perm_space.length)
        factoradic_number = math_tools.to_factoradic(
            self.number * math.factorial(
                 self.just_dapplied_rapplied_perm_space.n_unused_elements),
            n_digits_pad=self.just_dapplied_rapplied_perm_space.sequence_length
        )
        if self.is_partial:
            factoradic_number = factoradic_number[
                :-self.just_dapplied_rapplied_perm_space.n_unused_elements
            ]
        unused_numbers = list(self.just_dapplied_rapplied_perm_space.sequence)
        result = tuple(unused_numbers.pop(factoradic_digit) for
                                         factoradic_digit in factoradic_number)
        assert sequence_tools.get_length(result) == self.length
        return nifty_collections.LazyTuple(result)
    


    @caching.CachedProperty
    def inverse(self):
        if self.is_rapplied:
            return self.unrapplied.inverse * \
                                  self.just_dapplied_rapplied_perm_space[0]
        else:
            _perm = [None] * \
                     self.just_dapplied_rapplied_perm_space.sequence_length
            for i, item in enumerate(self):
                _perm[item] = i
            return type(self)(_perm,
                              self.just_dapplied_rapplied_perm_space)
        
        
    __invert__ = lambda self: self.inverse
    
    domain = caching.CachedProperty(
        lambda self: self.just_dapplied_rapplied_perm_space.domain
    )
    
        
    @caching.CachedProperty
    def unrapplied(self):
        unrapplied = Perm(
            (self.just_dapplied_rapplied_perm_space.sequence.index(i)
             for i in self),
            self.just_dapplied_rapplied_perm_space.unrapplied
        )
        assert not unrapplied.is_rapplied
        return unrapplied
    
    undapplied = caching.CachedProperty(
        lambda self: Perm(
            self._perm_sequence,
            self.just_dapplied_rapplied_perm_space.undapplied
        )
        
    )
    uncombinationed = caching.CachedProperty(
        lambda self: Perm(
            self._perm_sequence,
            self.just_dapplied_rapplied_perm_space.uncombinationed
        )
        
    )

    def __getitem__(self, i):
        i_to_use = self.domain.index(i) if self.is_dapplied else i
        return self._perm_sequence[i_to_use]
        
    length = property(
        lambda self: self.just_dapplied_rapplied_perm_space.n_elements
    )
    
    def rapply(self, sequence, result_type=None):
        '''
        
        Specify `result_type` to determine the type of the result returned. If
        `result_type=None`, will use `tuple`, except when `other` is a `str` or
        `Perm`, in which case that same type would be used.
        '''
        if self.is_rapplied:
            raise TypeError("Can't rapply an rapplied permutation, try "
                            "`perm.unrapplied`.")
        sequence = \
             sequence_tools.ensure_iterable_is_immutable_sequence(sequence)
        if sequence_tools.get_length(sequence) < \
                                               sequence_tools.get_length(self):
            raise Exception("Can't rapply permutation on sequence of "
                            "shorter length.")
        
        permed_generator = (sequence[i] for i in self)
        if result_type is not None:
            if result_type is str:
                return ''.join(permed_generator)
            else:
                return result_type(permed_generator)
        elif isinstance(sequence, Perm):
            return Perm(permed_generator,
                        sequence.just_dapplied_rapplied_perm_space)
        elif isinstance(sequence, str):
            return ''.join(permed_generator)
        else:
            return tuple(permed_generator)
            
            
    __mul__ = rapply
            
    def __pow__(self, exponent):
        assert isinstance(exponent, numbers.Integral)
        if exponent <= -1:
            return self.inverse ** (- exponent)
        elif exponent == 0:
            return self.just_dapplied_rapplied_perm_space[0]
        else:
            assert exponent >= 1
            return misc_tools.general_product((self,) * exponent)
        
            
    @caching.CachedProperty
    def degree(self):
        if self.is_partial:
            return NotImplemented
        else:
            return len(self) - self.n_cycles
        
    
    @caching.CachedProperty
    def n_cycles(self):
        if self.is_partial:
            return NotImplemented
        if self.is_rapplied:
            return self.unrapplied.n_cycles
        if self.is_dapplied:
            return self.undapplied.n_cycles
        
        unvisited_items = set(self)
        n_cycles = 0
        while unvisited_items:
            starting_item = current_item = next(iter(unvisited_items))
            
            while current_item in unvisited_items:
                unvisited_items.remove(current_item)
                current_item = self[current_item]
                
            if current_item == starting_item:
                n_cycles += 1
                
        return n_cycles
      
      
    def get_neighbors(self, degrees=(1,), perm_space=None):
        from .map_space import MapSpace
        if perm_space is None:
            perm_space = self.just_dapplied_rapplied_perm_space
        return MapSpace(perm_space._coerce_perm,
                        PermSpace(self._perm_sequence,
                                  fixed_map=perm_space._undapplied_fixed_map,
                                  degrees=degrees, slice_=None))
        
        
    def __lt__(self, other):
        if isinstance(other, Perm):
            return (self.number, self.just_dapplied_rapplied_perm_space) < \
                  (other.number, other.just_dapplied_rapplied_perm_space)
        else:
            return NotImplemented
        
    __reversed__ = lambda self: Perm(reversed(self._perm_sequence),
                                     self.just_dapplied_rapplied_perm_space)
    
    items = caching.CachedProperty(PermItems)
    as_dictoid = caching.CachedProperty(PermAsDictoid)
    
        


from .perm_space import PermSpace
from .comb_space import CombSpace
from .comb import Comb
