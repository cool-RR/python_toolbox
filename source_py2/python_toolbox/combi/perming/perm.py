# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import abc
import collections
import numbers

from python_toolbox.third_party import functools

from python_toolbox import misc_tools
from python_toolbox import nifty_collections
from python_toolbox import caching
from python_toolbox import sequence_tools
from python_toolbox import cute_iter_tools

from .. import misc


infinity = float('inf')


class _BasePermView(object):
    '''
    Abstract base class for viewers on Perm.
    '''
    __metaclass__ = abc.ABCMeta
    def __init__(self, perm):
        self.perm = perm
    __repr__ = lambda self: '<%s: %s>' % (type(self).__name__, self.perm)
    
    @abc.abstractmethod
    def __getitem__(self, i): pass


class PermItems(sequence_tools.CuteSequenceMixin, _BasePermView,
                collections.Sequence):
    '''
    A viewer of a perm's items, similar to `dict.items()`.
    
    This is useful for dapplied perms; it lets you view the perm (both index
    access and iteration) as a sequence where each item is a 2-tuple, where the
    first item is from the domain and the second item is its corresponding item
    from the sequence.
    '''
    
    def __getitem__(self, i):
        return (self.perm.domain[i], self.perm[self.perm.domain[i]])
    

class PermAsDictoid(sequence_tools.CuteSequenceMixin, _BasePermView,
                    collections.Mapping):
    '''A dict-like interface to a `Perm`.'''    
    def __getitem__(self, key):
        return self.perm[key]
    def __iter__(self):
        return iter(self.perm.domain)
        
    

class PermType(abc.ABCMeta):
    '''
    Metaclass for `Perm` and `Comb`.
    
    The functionality provided is: If someone tries to create a `Perm` with a
    `CombSpace`, we automatically use `Comb`.
    '''
    def __call__(cls, item, perm_space=None):
        if cls == Perm and isinstance(perm_space, CombSpace):
            cls = Comb
        return super(PermType, cls).__call__(item, perm_space)
        

@functools.total_ordering
class Perm(sequence_tools.CuteSequenceMixin, collections.Sequence):
    '''
    A permutation of items from a `PermSpace`.
    
    In combinatorics, a permutation is a sequence of items taken from the
    original sequence.
    
    Example:
    
        >>> perm_space = PermSpace('abcd')
        >>> perm = Perm('dcba', perm_space)
        >>> perm
        <Perm: ('d', 'c', 'b', 'a')>
        >>> perm_space.index(perm)
        23
    
    '''
    __metaclass__ = PermType
    
    @classmethod
    def coerce(cls, item, perm_space=None):
        '''Coerce item into a perm, optionally of a specified `PermSpace`.'''
        if isinstance(item, Perm) and (perm_space is not None) and \
          (item.nominal_perm_space == perm_space._nominal_perm_space_of_perms):
            return item
        else:
            return cls(item, perm_space)
    
    
    def __init__(self, perm_sequence, perm_space=None):
        '''
        Create the `Perm`.
        
        If `perm_space` is not supplied, we assume that this is a pure
        permutation, i.e. a permutation on `range(len(perm_sequence))`.
        '''
        perm_space = None if perm_space is None \
                                              else PermSpace.coerce(perm_space)
        assert isinstance(perm_sequence, collections.Iterable)
        perm_sequence = sequence_tools. \
                           ensure_iterable_is_immutable_sequence(perm_sequence)
        
        ### Analyzing `perm_space`: ###########################################
        #                                                                     #
        if perm_space is None:
            if isinstance(perm_sequence, Perm):
                self.nominal_perm_space = perm_sequence.nominal_perm_space
            else:
                # We're assuming that `number_or_perm_sequence` is a pure
                # permutation sequence. Not asserting this because that would
                # be O(n).
                self.nominal_perm_space = PermSpace(len(perm_sequence))
        else: # perm_space is not None
            self.nominal_perm_space = perm_space.unsliced.undegreed.unfixed
            
        # `self.nominal_perm_space` is a perm space that preserves only the
        # rapplied, recurrent, partial, dapplied and combination properties of
        # the original `PermSpace`.
            
        #                                                                     #
        ### Finished analyzing `perm_space`. ##################################
        
        self.is_rapplied = self.nominal_perm_space.is_rapplied
        self.is_recurrent = self.nominal_perm_space.is_recurrent
        self.is_partial = self.nominal_perm_space.is_partial
        self.is_combination = self.nominal_perm_space.is_combination
        self.is_dapplied = self.nominal_perm_space.is_dapplied
        self.is_pure = not (self.is_rapplied or self.is_dapplied
                            or self.is_partial or self.is_combination)
        
        if not self.is_rapplied: self.unrapplied = self
        if not self.is_dapplied: self.undapplied = self
        if not self.is_combination: self.uncombinationed = self
        
        self._perm_sequence = sequence_tools. \
             ensure_iterable_is_immutable_sequence(perm_sequence)
            
        assert self.is_combination == isinstance(self, Comb)
            
            
    _reduced = property(lambda self: (
        type(self), self._perm_sequence, self.nominal_perm_space
    ))
            
    __iter__ = lambda self: iter(self._perm_sequence)
    
    def __eq__(self, other):
        return type(self) == type(other) and \
                      self.nominal_perm_space == other.nominal_perm_space and \
           cute_iter_tools.are_equal(self._perm_sequence, other._perm_sequence)

    __ne__ = lambda self, other: not (self == other)
    __hash__ = lambda self: hash(self._reduced)
    __bool__ = lambda self: bool(self._perm_sequence)
    __nonzero__ = __bool__
    
    def __contains__(self, item):
        try:
            return (item in self._perm_sequence)
        except TypeError:
            # Gotta have this `except` because Python complains if you try `1
            # in 'meow'`.
            return False
    
    def __repr__(self):
        return '<%s%s: %s(%s%s)>' % (
            type(self).__name__, 
            (', n_elements=%s' % len(self)) if self.is_partial else '',
            ('(%s) => ' % ', '.join(map(repr, self.domain)))
                                                   if self.is_dapplied else '',
            ', '.join(repr(item) for item in self),
            ',' if self.length == 1 else ''
        )
        
    def index(self, member):
        '''
        Get the index number of `member` in the permutation.
        
        Example:
        
            >>> perm = PermSpace(5)[10]
            >>> perm
            <Perm: (0, 2, 4, 1, 3)>
            >>> perm.index(3)
            4
        
        '''
        numerical_index = self._perm_sequence.index(member)
        return self.nominal_perm_space. \
               domain[numerical_index] if self.is_dapplied else numerical_index
        

    @caching.CachedProperty
    def inverse(self):
        '''
        The inverse of this permutation.
        
        i.e. the permutation that we need to multiply this permutation by to
        get the identity permutation.
        
        This is also accessible as `~perm`.
        
        Example:
        
            >>> perm = PermSpace(5)[10]
            >>> perm
            <Perm: (0, 2, 4, 1, 3)>
            >>> ~perm
            <Perm: (0, 3, 1, 4, 2)>
            >>> perm * ~perm
            <Perm: (0, 1, 2, 3, 4)>
           
        '''
        if self.is_partial:
            raise TypeError("Partial perms don't have an inverse.")
        if self.is_rapplied:
            raise TypeError("Rapplied perms don't have an inverse.")
        if self.is_dapplied:
            raise TypeError("Dapplied perms don't have an inverse.")
        if self.is_rapplied:
            return self.nominal_perm_space[0] * self.unrapplied.inverse
        else:
            _perm = [None] * \
                     self.nominal_perm_space.sequence_length
            for i, item in enumerate(self):
                _perm[item] = i
            return type(self)(_perm, self.nominal_perm_space)
        
        
    __invert__ = lambda self: self.inverse
    
    domain = caching.CachedProperty(
        lambda self: self.nominal_perm_space.domain,
        '''The permutation's domain.'''
    )
    
        
    @caching.CachedProperty
    def unrapplied(self):
        '''An unrapplied version of this permutation.'''
        ### Calculating the new perm sequence: ################################
        #                                                                     #
        # This is more complex than a one-line generator because of recurrent
        # perms; every time there's a recurrent item, we need to take not
        # necessary the index of its first occurrence in the rapplied sequence
        # but the first index we haven't taken already.
        rapplied_sequence = list(self.nominal_perm_space.sequence)
        new_perm_sequence = []
        for i in self._perm_sequence:
            i_index = rapplied_sequence.index(i)
            rapplied_sequence[i_index] = misc.MISSING_ELEMENT
            new_perm_sequence.append(i_index)
        #                                                                     #
        ### Finished calculating the new perm sequence. #######################
        
        unrapplied = type(self)(new_perm_sequence,
                                self.nominal_perm_space.unrapplied)
        assert not unrapplied.is_rapplied
        return unrapplied
    
    undapplied = caching.CachedProperty(
        lambda self: type(self)(
            self._perm_sequence,
            self.nominal_perm_space.undapplied
        ),
        '''An undapplied version of this permutation.'''
        
    )
    uncombinationed = caching.CachedProperty(
        lambda self: Perm(
            self._perm_sequence,
            self.nominal_perm_space.uncombinationed
        ),
        '''A non-combination version of this permutation.'''
        
    )

    def __getitem__(self, i):
        if self.is_dapplied:
            try:
                i_to_use = self.domain.index(i)
            except TypeError:
                # Some types, like `str`, annoyingly raise `TypeError` instead
                # of `IndexError`.
                raise IndexError
        else:
            i_to_use = i
        return self._perm_sequence[i_to_use]
        
    length = property(
        lambda self: self.nominal_perm_space.n_elements
    )
    
    def apply(self, sequence, result_type=None):
        '''
        Apply the perm to a sequence, choosing items from it.
        
        This can also be used as `sequence * perm`. Example:
        
        >>> perm = PermSpace(5)[10]
        >>> perm
        <Perm: (0, 2, 4, 1, 3)>
        >>> perm.apply('growl')
        'golrw'
        >>> 'growl' * perm
        'golrw'
        
        Specify `result_type` to determine the type of the result returned. If
        `result_type=None`, will use `tuple`, except when `other` is a `str` or
        `Perm`, in which case that same type would be used.
        '''
        sequence = \
             sequence_tools.ensure_iterable_is_immutable_sequence(sequence)
        if sequence_tools.get_length(sequence) < \
                                               sequence_tools.get_length(self):
            raise Exception("Can't apply permutation on sequence of "
                            "shorter length.")
        
        permed_generator = (sequence[i] for i in self)
        if result_type is not None:
            if result_type is str:
                return ''.join(permed_generator)
            else:
                return result_type(permed_generator)
        elif isinstance(sequence, Perm):
            return type(self)(permed_generator,
                              sequence.nominal_perm_space)
        elif isinstance(sequence, str):
            return ''.join(permed_generator)
        else:
            return tuple(permed_generator)
            
            
    __rmul__ = apply
    
    __mul__ = lambda self, other: other.__rmul__(self)
    # (Must define this explicitly because of Python special-casing
    # multiplication of objects of the same type.)
            
    def __pow__(self, exponent):
        '''Raise the perm by the power of `exponent`.'''
        assert isinstance(exponent, numbers.Integral)
        if exponent <= -1:
            return self.inverse ** (- exponent)
        elif exponent == 0:
            return self.nominal_perm_space[0]
        else:
            assert exponent >= 1
            return misc_tools.general_product((self,) * exponent)
        
            
    @caching.CachedProperty
    def degree(self):
        '''
        The permutation's degree.
        
        You can think of a permutation's degree like this: Imagine that you're
        starting with the identity permutation, and you want to make this
        permutation, by switching two items with each other over and over again
        until you get this permutation. The degree is the number of such
        switches you'll have to make.
        '''
        if self.is_partial:
            return NotImplemented
        else:
            return len(self) - self.n_cycles
        
    
    @caching.CachedProperty
    def n_cycles(self):
        '''
        The number of cycles in this permutation.
        
        If item 1 points at item 7, and item 7 points at item 3, and item 3
        points at item 1 again, then that's one cycle. `n_cycles` is the total
        number of cycles in this permutation.
        '''
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
      
      
    @misc_tools.limit_positional_arguments(1)
    def get_neighbors(self, degrees=(1,), perm_space=None):
        '''
        Get the neighbor permutations of this permutation.
        
        This means, get the permutations that are close to this permutation. By
        default, this means permutations that are one transformation (switching
        a pair of items) away from this permutation. You can specify a custom
        sequence of integers to the `degrees` argument to get different degrees
        of relation. (e.g. specify `degrees=(1, 2)` to get both the closest
        neighbors and the second-closest neighbors.)
        '''
        from ..map_space import MapSpace
        if self.is_combination or self.is_recurrent or self.is_partial:
            raise NotImplementedError
        if perm_space is None:
            perm_space = self.nominal_perm_space
        return MapSpace(
            perm_space.coerce_perm,
            nifty_collections.LazyTuple(
                tuple(perm) for perm in PermSpace(
                    self._perm_sequence,
                    degrees=degrees
                ) if tuple(perm) in perm_space
            )
        )
        
        
    def __lt__(self, other):
        if isinstance(other, Perm) and \
                           self.nominal_perm_space == other.nominal_perm_space:
            return self._perm_sequence < other._perm_sequence
        else:
            return NotImplemented
        
    __reversed__ = lambda self: type(self)(reversed(self._perm_sequence),
                                           self.nominal_perm_space)
    
    items = caching.CachedProperty(PermItems)
    as_dictoid = caching.CachedProperty(PermAsDictoid)
    

class UnrecurrentedMixin(object):
    '''Mixin for a permutation in a space that's been unrecurrented.'''
    def __getitem__(self, i):
        return super(UnrecurrentedMixin, self).__getitem__(i)[1]
    def __iter__(self):
        return iter(tuple(zip(*super(UnrecurrentedMixin, self).__iter__()))[1])
    index = lambda self, item: self.nominal_perm_space.domain[
        next(j for j, pair in enumerate(self._perm_sequence)
                                                            if pair[1] == item)
    ]
    '''Get the index number of `member` in the permutation.'''
    
class UnrecurrentedPerm(UnrecurrentedMixin, Perm):
    '''A permutation in a space that's been unrecurrented.'''
        
        

from .perm_space import PermSpace
from .comb_space import CombSpace
from .comb import Comb
