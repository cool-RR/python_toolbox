# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import division

import collections
import abc
import functools
import types
import sys
import math
import numbers

from python_toolbox import misc_tools
from python_toolbox import dict_tools
from python_toolbox import nifty_collections
from python_toolbox import sequence_tools
from python_toolbox import caching
import python_toolbox.arguments_profiling

from python_toolbox import math_tools
from python_toolbox import sequence_tools
from python_toolbox import cute_iter_tools
from python_toolbox import nifty_collections
from python_toolbox import dict_tools

from . import misc
from python_toolbox import misc_tools

infinity = float('inf')



class PermSpaceType(abc.ABCMeta):
    '''
    Metaclass for `PermSpace` and `CombSpace`.
    
    The functionality provided is: If someone tries to instantiate `PermSpace`
    while specifying `is_combination=True`, we automatically use `CombSpace`
    for him.
    '''
    def __call__(cls, *args, **kwargs):
        if cls == PermSpace and kwargs.get('is_combination', False):
            from .comb_space import CombSpace
            arguments_profile = python_toolbox.arguments_profiling. \
                    ArgumentsProfile(PermSpace.__init__, None, *args, **kwargs)
            if arguments_profile.get('fixed_map', None):
                raise NotImplementedError
            return super(PermSpaceType, CombSpace).__call__(
                iterable_or_length=arguments_profile['iterable_or_length'], 
                n_elements=arguments_profile['n_elements'], 
                slice_=arguments_profile['slice_'],
                _domain_for_checking=arguments_profile['domain'],
                _degrees_for_checking=arguments_profile['degrees'],
            )
        else:
            return super(PermSpaceType, cls).__call__(*args, **kwargs)
        
        
@functools.total_ordering
class PermSpace(sequence_tools.CuteSequenceMixin, collections.Sequence):
    '''
    A space of permutations on a sequence.
    
    Each item in a `PermSpace` is a `Perm`, i.e. a permutation. This is similar
    to `itertools.permutations`, except it offers far, far more functionality.
    The permutations may be accessed by index number, the permutation space can
    have its range and domain specified, some items can be fixed, and more.
    
    Here is a simple `PermSpace`:
    
        >>> perm_space = PermSpace(3)
        >>> tuple(perm_space)
        (<Perm: (0 / 6) (0, 1, 2)>, <Perm: (1 / 6) (0, 2, 1)>,
         <Perm: (2 / 6) (1, 0, 2)>, <Perm: (3 / 6) (1, 2, 0)>,
         <Perm: (4 / 6) (2, 0, 1)>, <Perm: (5 / 6) (2, 1, 0)>)

    The permutations are generated on-demand, not in advance. This means you
    can easily create something like `PermSpace(1000)`, which has about
    10**2500 permutations in it (a number that far exceeds the number of
    particles in the universe), in a fraction of a second. You can then fetch
    by index number any permutation of the 10**2500 permutations in a fraction
    of a second as well.
    
    Instead of a number, you can also pass a sequence as the first argument,
    and the `PermSpace` will use that rather than `range`.
    
    You may pass a sequence as the `domain` argument, and it'll be used as the
    indices for the permutations. (i.e., if the permutations are seen as a
    function, `domain` is the domain of the function.)
    
    You may pass a number as `n_elements` in order to make a partial
    permutation space. That number must be smaller than the size of the
    sequence, and every permutation will have only that number of items. This
    means that permutations will not use all the items in `sequence` but just
    some of them.
    
    You may pass in a `dict` for the argument `fixed_map` that'll map between
    indices and values that should remain fixed in the permutation space. Only
    the non-fixed items will be allowed to change between permutations.
    
    You may pass in a list of integers as `degrees`, and then only permutations
    with those degrees will be included in the space. (A degree of a
    permutation stands for that number of transformations (single switches
    between items) that are needed to create that permutation. )
    
    A permutation space can be sliced by using regular Python slice notation.
    
    Note: Some of the options are not allowed to be used with each other.
    
    Some clarification  on terminology <blocktododoc> rapplied, dapplied "just" etc.
    '''
    __metaclass__ = PermSpaceType
    
    @classmethod
    def coerce(cls, argument):
        '''
        Make `argument` into something of class `cls`, if it isn't already.
        '''
        if isinstance(argument, PermSpace):
            return argument
        else:
            return cls(argument)
    
    def __init__(self, iterable_or_length, domain=None, n_elements=None, 
                 fixed_map=None, degrees=None, is_combination=False,
                 slice_=None):
        
        ### Making basic argument checks: #####################################
        #                                                                     #
        assert isinstance(
            iterable_or_length,
            (collections.Iterable, numbers.Integral)
        )
        if isinstance(iterable_or_length, numbers.Integral):
            assert iterable_or_length >= 0
        if slice_ is not None:
            assert isinstance(slice_,
                              (slice, sequence_tools.CanonicalSlice))
            if slice_.step not in (1, None):
                raise NotImplementedError
        assert isinstance(n_elements, numbers.Integral) or n_elements is None
        assert isinstance(is_combination, bool)
        #                                                                     #
        ### Finished making basic argument checks. ############################

        ### Figuring out sequence and whether space is rapplied: ##############
        #                                                                     #
        if isinstance(iterable_or_length, numbers.Integral):
            self.is_rapplied = False
            self.sequence = sequence_tools.CuteRange(
                iterable_or_length,
                _avoid_built_in_range=True
            )
            # (Avoiding built-in `xrange` in Python 2 because it lacks
            # `.index`.)
            self.sequence_length = iterable_or_length
        else:
            assert isinstance(iterable_or_length, collections.Iterable)
            self.sequence = sequence_tools. \
                      ensure_iterable_is_immutable_sequence(iterable_or_length)
            range_candidate = sequence_tools.CuteRange(
                len(self.sequence),
                _avoid_built_in_range=True
            )
            # (Avoiding built-in `xrange` in Python 2 because it lacks
            # `.index`.)
            
            self.is_rapplied = not (
                cute_iter_tools.are_equal(self.sequence,
                                              range_candidate)
            )
            self.sequence_length = len(self.sequence)
            if not self.is_rapplied:
                self.sequence = sequence_tools.CuteRange(
                    self.sequence_length,
                    _avoid_built_in_range=True
                )
                # (Avoiding built-in `xrange` in Python 2 because it lacks
                # `.index`.)
                
        
        if self.is_rapplied and (len(set(self.sequence)) < len(self.sequence)):
            # Can implement this later by calculating the actual length.
            raise NotImplementedError
        
        #                                                                     #
        ### Finished figuring out sequence and whether space is rapplied. #####
        
        ### Figuring out number of elements: ##################################
        #                                                                     #
        
        self.n_elements = self.sequence_length if (n_elements is None) \
                                                                else n_elements
        if not 0 <= self.n_elements <= self.sequence_length:
            raise Exception('`n_elements` must be between 0 and %s' %
                                                          self.sequence_length)
        self.is_partial = (self.n_elements < self.sequence_length)
        
        self.indices = sequence_tools.CuteRange(self.n_elements,
                                                _avoid_built_in_range=True)
        # Avoiding built-in xrange because on Python 2 it don't have `index`.
        
        #                                                                     #
        ### Finished figuring out number of elements. #########################
        
        ### Figuring out whether it's a combination: ##########################
        #                                                                     #
        self.is_combination = is_combination
        
        if self.is_combination:
            if fixed_map:
                raise NotImplementedError
        
        self._just_partialled_combinationed_length = \
            math_tools.factorial(
                self.sequence_length,
                start=(self.sequence_length - self.n_elements + 1)
            ) // (math_tools.factorial(self.n_elements) if
                                                    self.is_combination else 1)
        # This division is always without a remainder, because math.
        #                                                                     #
        ### Finished figuring out whether it's a combination. #################
        
        
        ### Figuring out whether space is dapplied: ###########################
        #                                                                     #
        if domain is None:
            domain = self.indices
        domain = \
               sequence_tools.ensure_iterable_is_immutable_sequence(domain)
        if self.is_partial:
            domain = domain[:self.n_elements]
        self.is_dapplied = not cute_iter_tools.are_equal(
            domain, self.indices
        )
        if self.is_dapplied:
            if self.is_combination:
                raise Exception("Can't use a domain with combination spaces.")
            self.domain = domain
            if len(set(self.domain)) < len(self.domain):
                raise Exception('The domain must not have repeating elements.')
        else:
            self.domain = self.indices
            self.undapplied = self
        #                                                                     #
        ### Finished figuring out whether space is dapplied. ##################
        
        
        ### Figuring out fixed map: ###########################################
        #                                                                     #
        if fixed_map is None:
            fixed_map = {}
        if not isinstance(fixed_map, dict):
            if isinstance(fixed_map, collections.Callable):
                fixed_map = {item: fixed_map(item) for item in self.sequence}
            else:
                fixed_map = dict(fixed_map) 
        if fixed_map:
            self.fixed_map = {key: value for (key, value) in
                              fixed_map.items() if (key in self.domain) and
                              (value in self.sequence)}
                
        else:
            (self.fixed_map, self.free_indices, self.free_keys,
             self.free_values) = (
                {},
                self.indices,
                self.domain, 
                self.sequence
            )
                
        self.is_fixed = bool(self.fixed_map)
        if self.is_fixed:
            self._unsliced_undegreed_length = math_tools.factorial(
                len(self.free_indices),
                start=(len(self.free_indices) -
                                   (self.n_elements - len(self.fixed_map)) + 1)
            )
            if not (self.is_dapplied or self.is_rapplied or degrees or slice_
                    or (n_elements is not None) or self.is_combination):
                self._just_fixed = self
            else:
                self._get_just_fixed = lambda: PermSpace(
                    len(self.sequence),
                    fixed_map=self._undapplied_unrapplied_fixed_map,
                )
        else:
            self._unsliced_undegreed_length = \
                                     self._just_partialled_combinationed_length
            if not (self.is_dapplied or self.is_rapplied or degrees or slice_
                    or (n_elements is not None) or self.is_combination):
                self._just_fixed = self
            else:
                self._get_just_fixed = lambda: PermSpace(len(self.sequence))
        
        #                                                                     #
        ### Finished figuring out fixed map. ##################################
        
        ### Figuring out degrees: #############################################
        #                                                                     #
        all_degrees = sequence_tools.CuteRange(self.sequence_length)
        if degrees is None:
            degrees = ()
        if not isinstance(degrees, collections.Iterable):
            assert isinstance(degrees, numbers.Integral)
            degrees = (degrees,)
        degrees = \
              sequence_tools.ensure_iterable_is_immutable_sequence(degrees)
        
        if not degrees or cute_iter_tools.are_equal(degrees,
                                                        all_degrees):
            self.is_degreed = False
            self.degrees = all_degrees
            self._unsliced_length = self._unsliced_undegreed_length
        else:
            self.is_degreed = True
            if self.is_combination or self.is_partial:
                raise NotImplementedError
            self.degrees = tuple(
                degree for degree in degrees if degree in all_degrees
            )
            self._unsliced_length = sum(
                math_tools.abs_stirling(
                    self.sequence_length - len(self.fixed_map),
                    self.sequence_length - degree -
                                    self._n_cycles_in_fixed_items_of_just_fixed
                ) for degree in self.degrees
            )
            
        #                                                                     #
        ### Finished figuring out degrees. ####################################
            
        ### Figuring out slice: ###############################################
        #                                                                     #
        self.slice_ = slice_
        self.canonical_slice = sequence_tools.CanonicalSlice(
            slice_ or slice(float('inf')),
            self._unsliced_length
        )
        self.length = max(
            self.canonical_slice.stop - self.canonical_slice.start,
            0
        )
        self.is_sliced = (self.length != self._unsliced_length)
        #                                                                     #
        ### Finished figuring out slice. ######################################
        
        
        self.is_pure = not (self.is_rapplied or self.is_fixed or self.is_sliced
                            or self.is_degreed or self.is_partial or
                            self.is_combination)
        
        if self.is_pure:
            self.purified = self
        if not self.is_rapplied:
            self.unrapplied = self
        if not self.is_fixed:
            self.unfixed = self
        if not self.is_sliced:
            self.unsliced = self
        if not self.is_degreed:
            self.undegreed = self
        if not self.is_partial:
            self.unpartialled = self
        if not self.is_combination:
            self.uncombinationed = self
            
    @caching.CachedProperty
    def _undapplied_fixed_map(self):
        if self.is_dapplied:
            return {self.domain.index(key): value for key, value
                    in self.fixed_map.items()}
        else:
            return self.fixed_map
            
    @caching.CachedProperty
    def _undapplied_unrapplied_fixed_map(self):
        if self.is_dapplied or self.is_rapplied:
            return {self.domain.index(key): self.sequence.index(value)
                    for key, value in self.fixed_map.items()}
        else:
            return self.fixed_map
        
    _just_fixed = caching.CachedProperty(lambda self: self._get_just_fixed())
    
    def _get_just_fixed(self):
        # This gets overridden in `__init__`.
        raise RuntimeError
        
        
    def __repr__(self):
        
        if self.is_dapplied:
            domain_repr = repr(self.domain)
            if len(domain_repr) > 40:
                domain_repr = \
                          ''.join((domain_repr[:35], ' ... ', domain_repr[-1]))
            domain_snippet = '%s => ' % domain_repr
        else:
            domain_snippet = ''
            
        sequence_repr = repr(self.sequence)
        if len(sequence_repr) > 40:
            sequence_repr = \
                      ''.join((sequence_repr[:35], ' ... ', sequence_repr[-1]))
            
        return '<%s: %s%s%s%s%s%s>%s' % (
            type(self).__name__,
            domain_snippet,
            sequence_repr,
            (', n_elements=%s' % (self.n_elements,)) if self.is_partial
                                                                       else '',
            ', is_combination=True' if self.is_combination else '',
            (', fixed_map=%s' % (self.fixed_map,)) if self.is_fixed else '',
            (', degrees=%s' % (self.degrees,)) if self.is_degreed else '',
            ('[%s:%s]' % (self.slice_.start, self.slice_.stop)) if
                                                         self.is_sliced else ''
        )
        
    def __getitem__(self, i):
        if isinstance(i, (slice, sequence_tools.CanonicalSlice)):
            canonical_slice = sequence_tools.CanonicalSlice(
                i, self.length, offset=self.canonical_slice.start
            )
            return PermSpace(self.sequence, domain=self.domain,
                             fixed_map=self.fixed_map, degrees=self.degrees,
                             slice_=canonical_slice)
        
        else:
            assert isinstance(i, numbers.Integral)
            if i <= -1:
                i += self.length
            if not (0 <= i < self.length):
                raise IndexError
            if self.is_rapplied:
                return self.perm_type(self.unrapplied[i].rapply(self.sequence),
                                      self)
            elif self.is_sliced:
                return self.unsliced[i + self.canonical_slice.start]
            if self.is_degreed:
                available_elements = list(self.free_values)
                wip_perm_sequence_dict = dict(self.fixed_map)
                wip_n_cycles_in_fixed_items = \
                                    self._n_cycles_in_fixed_items_of_just_fixed
                wip_i_with_slice_boost = i
                for j in range(self.sequence_length):
                    domain_j = self.domain[j]
                    if domain_j in wip_perm_sequence_dict:
                        continue
                    for unused_number in available_elements:
                        candidate_perm_sequence_dict = \
                                                   dict(wip_perm_sequence_dict)
                        candidate_perm_sequence_dict[domain_j] = unused_number
                        
                        ### Checking whether we closed a cycle: ###############
                        #                                                     #
                        if j == unused_number:
                            closed_cycle = True
                        else:
                            current = domain_j
                            while True:
                                current = self.domain[
                                    candidate_perm_sequence_dict[current]
                                ]
                                if current == domain_j:
                                    closed_cycle = True
                                    break
                                elif current not in candidate_perm_sequence_dict:
                                    closed_cycle = False
                                    break
                        #                                                     #
                        ### Finished checking whether we closed a cycle. ######
                        
                        candidate_n_cycles_in_fixed_items = \
                                     wip_n_cycles_in_fixed_items + closed_cycle
                        
                        candidate_fixed_perm_space_length = sum(
                            math_tools.abs_stirling(
                                self.sequence_length -
                                             len(candidate_perm_sequence_dict),
                                self.sequence_length - degree -
                                              candidate_n_cycles_in_fixed_items
                            ) for degree in self.degrees
                        )
                        
                        
                        if wip_i_with_slice_boost < \
                                             candidate_fixed_perm_space_length:
                            available_elements.remove(unused_number)
                            wip_perm_sequence_dict[domain_j] = unused_number
                            wip_n_cycles_in_fixed_items = \
                                              candidate_n_cycles_in_fixed_items
                            
                            break
                        wip_i_with_slice_boost -= \
                                              candidate_fixed_perm_space_length
                    else:
                        raise RuntimeError
                return self.perm_type((wip_perm_sequence_dict[i] for i in
                                       self.domain), self)
            elif self.is_fixed:
                free_values_perm = self._free_values_unsliced_perm_space[i]
                free_values_perm_iterator = iter(free_values_perm)
                return self.perm_type(
                    tuple(
                        (self._undapplied_fixed_map[i] if
                         (i in self.fixed_indices) else
                         next(free_values_perm_iterator))
                                           for i in range(self.sequence_length)
                    ),
                    self
                )
            
            else:
                return self.perm_type(i, self)
                
                
    n_unused_elements = caching.CachedProperty(
        lambda self: self.sequence_length - self.n_elements
    )
    
    __iter__ = lambda self: (self[i] for i in
                                         sequence_tools.CuteRange(self.length))
    _reduced = property(
        lambda self: (type(self), self.sequence, self.domain, 
                      tuple(self.fixed_map.items()), self.canonical_slice)
    )
             
    __eq__ = lambda self, other: (isinstance(other, PermSpace) and
                                  self._reduced == other._reduced)
    __ne__ = lambda self, other: not (self == other)
    __hash__ = lambda self: hash(self._reduced)
    
    
    def index(self, perm):
        '''Get the index number of permutation `perm` in this space.'''
        if not isinstance(perm, collections.Iterable):
            raise ValueError
        
        try:
            perm = sequence_tools.ensure_iterable_is_immutable_sequence(
                perm,
                allow_unordered=self.is_combination
            )
        except sequence_tools.UnorderedIterableException:
            raise ValueError('An unordered iterable is never contained in a '
                             'non-combination `PermSpace`.')
        
        perm_set = set(perm)
        if not (perm_set <= set(self.sequence)):
            raise ValueError
        
        if sequence_tools.get_length(perm) != self.n_elements:
            raise ValueError
        
        if not isinstance(perm, self.perm_type):
            if perm_set != set(range(len(perm))):
                perm = self.perm_type(perm, self)
            else:
                perm = self.perm_type(perm)
            
        elif self.is_rapplied:
            if not perm.is_rapplied:
                raise ValueError
        elif perm.is_rapplied and not self.is_rapplied:
            raise ValueError
        if self.is_degreed and (perm.degree not in self.degrees):
            raise ValueError
        
        # At this point we know the permutation contains the correct items, and
        # has the correct degree.
        
        if self.is_rapplied or self.is_dapplied:
            return self.unrapplied.undapplied.index(perm.unrapplied.undapplied)
        
        if self.is_degreed:
            wip_perm_number = 0
            wip_perm_sequence_dict = dict(self.fixed_map)
            unused_values = list(self.free_values)
            for i, value in enumerate(perm):
                if i in self.fixed_indices:
                    continue
                unused_values.remove(value)
                lower_values = [j for j in unused_values if j < value]
                for lower_value in lower_values:
                    temp_fixed_map = dict(wip_perm_sequence_dict)
                    temp_fixed_map[i] = lower_value
                    wip_perm_number += PermSpace(
                        self.sequence_length, degrees=self.degrees,
                        fixed_map=temp_fixed_map
                    ).length
                    
                wip_perm_sequence_dict[i] = value
                
            perm_number = wip_perm_number
            
        elif self.is_fixed:
            free_values_perm_sequence = []
            for i, perm_item in enumerate(perm):
                if i in self.fixed_map:
                    if self.fixed_map[i] != perm_item:
                        raise ValueError
                else:
                    free_values_perm_sequence.append(perm_item)
            
            # At this point we know all the items that should be fixed are
            # fixed.
            
            perm_number = self._free_values_unsliced_perm_space.index(
                free_values_perm_sequence
            )
            
        else:
            perm_number = perm.number
            
        if not perm_number in self.canonical_slice:
            raise ValueError
            
        return perm_number - self.canonical_slice.start
    
    
    short_length_string = caching.CachedProperty(
        lambda self: misc.get_short_factorial_string(self.sequence_length),
        doc='Short string describing size of space, e.g. "12!"'
    )
    
    undapplied = caching.CachedProperty(
        lambda self: PermSpace(
            self.sequence, fixed_map=self._undapplied_fixed_map,
            degrees=self.degrees, slice_=self.canonical_slice,
            n_elements=self.n_elements, is_combination=self.is_combination
        ),
        doc='A version of this `PermSpace` without a custom domain.'
    )
    unrapplied = caching.CachedProperty(
        lambda self: PermSpace(
            self.sequence_length, domain=self.domain, 
            fixed_map={key: self.sequence.index(value) for
                       key, value in self.fixed_map.items()},
            degrees=self.degrees, slice_=self.canonical_slice,
            n_elements=self.n_elements, is_combination=self.is_combination
        ),
        doc='A version of this `PermSpace` without a custom range.'
    )
    @caching.CachedProperty
    def unpartialled(self):
        '''A non-partial version of this `PermSpace`.'''
        assert self.is_partial # Otherwise this property would be overridden.
        if self.is_sliced:
            raise Exception(
                "Can't convert sliced `PermSpace` directly to unpartialled, "
                "because the number of items would be different. Use "
                "`.unsliced` first."
            )
        if self.is_dapplied:
            raise Exception(
                "Can't convert a partial, dapplied `PermSpace` to "
                "non-partialled, because we'll need to extend the domain with "
                "more items and we don't know which to use."
            )
            
        return PermSpace(
            self.sequence, n_elements=self.sequence_length,
            fixed_map=self.fixed_map, degrees=self.degrees,
            slice_=self.canonical_slice, is_combination=self.is_combination
        )
    
    unsliced = caching.CachedProperty(
        lambda self: PermSpace(
            self.sequence, domain=self.domain, fixed_map=self.fixed_map,
            n_elements=self.n_elements, is_combination=self.is_combination, 
            degrees=self.degrees, slice_=None
        ),
        doc='An unsliced version of this `PermSpace`.'
    )
    purified = caching.CachedProperty(
        lambda self: PermSpace(len(self.sequence)),
        doc='An purified version of this `PermSpace`.'
    )
    _just_dapplied_rapplied = caching.CachedProperty(
        lambda self: self.purified.get_dapplied(self.domain). \
                                                   get_rapplied(self.sequence),
        doc='Purified, but dapplied and rapplied, version of this `PermSpace`.'
    )
    
    @caching.CachedProperty
    def uncombinationed(self):
        '''A version of this `PermSpace` where permutations have order.'''
        if self.is_sliced:
            raise Exception("Can't convert sliced `CombSpace` directly to "
                            "uncombinationed, because the number of items "
                            "would be different. Use `.unsliced` first.")
        return PermSpace(
            self.sequence, domain=self.domain, fixed_map=self.fixed_map,
            degrees=self.degrees, slice_=None,
            n_elements=self.n_elements, is_combination=False
        )
      
    
    @caching.CachedProperty
    def _free_values_purified_perm_space(self):
        '''
        A purified `PermSpace` of the free values in the `PermSpace`.
        
        Non-fixed permutation spaces have this set to `self` in the
        constructor.
        '''
        if self.is_fixed:
            return PermSpace(
                len(self.free_indices),
                n_elements=self.n_elements-len(self.fixed_map)
            )
        else:
            return self.purified
    
    
    _free_values_unsliced_perm_space = caching.CachedProperty(
        lambda self: self._free_values_purified_perm_space.get_degreed(
            (degree - self._n_cycles_in_fixed_items_of_just_fixed
                                                    for degree in self.degrees)
            if self.is_degreed else None).get_rapplied(self.free_values).
            get_dapplied(self.free_keys).
                          get_partialled(self.n_elements - len(self.fixed_map)),
    )
    
    __bool__ = lambda self: bool(self.length)
    
    def get_partialled(self, n_elements):
        '''Get a partialled version of this `PermSpace`.'''
        if self.is_sliced:
            raise Exception(
                "Can't get partial of sliced `PermSpace` directly, because the "
                "number of items would be different. Use `.unsliced` first."
            )
        return PermSpace(
            self.sequence, domain=self.domain, fixed_map=self.fixed_map,
            degrees=self.degrees, slice_=None,
            is_combination=self.is_combination, n_elements=n_elements
        )
        
        
    

    @caching.CachedProperty
    def undegreed(self):
        '''Get an undegreed version of this `PermSpace`.'''
        if self.is_sliced:
            raise Exception("Can't be used on sliced perm spaces. Try "
                            "`perm_space.unsliced.undegreed`.")
        return PermSpace(
            self.sequence, domain=self.domain, fixed_map=self.fixed_map,
            degrees=None, n_elements=self.n_elements,
            is_combination=self.is_combination
        )
    

    def get_rapplied(self, sequence):
        '''Get a version of this `PermSpace` that has a range of `sequence`.'''
        assert not self.is_rapplied
        sequence = \
             sequence_tools.ensure_iterable_is_immutable_sequence(sequence)
        if len(sequence) != self.sequence_length:
            raise Exception
        return PermSpace(
            sequence, domain=self.domain,
            fixed_map={key: sequence[value] for key, value in self.fixed_map}, 
            degrees=self.degrees, slice_=self.canonical_slice,
            n_elements=self.n_elements, is_combination=self.is_combination
        )
    
    def get_dapplied(self, domain):
        '''Get a version of this `PermSpace` that has a domain of `domain`.'''
        assert not self.is_dapplied
        if self.is_combination:
            raise Exception("Can't use a domain with combination spaces.")
        domain = \
               sequence_tools.ensure_iterable_is_immutable_sequence(domain)
        if len(domain) != self.n_elements:
            raise Exception
        return PermSpace(
            self.sequence, domain,
            fixed_map={domain[key]: value for key, value in self.fixed_map}, 
            degrees=self.degrees, slice_=self.canonical_slice,
            n_elements=self.n_elements, is_combination=self.is_combination
        )
    
    def get_degreed(self, degrees):
        '''Get a degreed version of this `PermSpace`.'''
        if self.is_sliced:
            raise Exception("Can't be used on sliced perm spaces. Try "
                            "`perm_space.unsliced.get_degreed(...)`.")
        if self.is_combination:
            raise Exception("Can't use degrees with combination spaces.")
        if not degrees:
            return self
        degrees_to_use = \
           degrees if not self.is_degreed else set(degrees) & set(self.degrees)
        return PermSpace(
            self.sequence, domain=self.domain, fixed_map=self.fixed_map,
            degrees=degrees_to_use, n_elements=self.n_elements,
            is_combination=self.is_combination
        )
    
    def get_fixed(self, fixed_map):
        '''Get a fixed version of this `PermSpace`.'''
        if self.is_sliced:
            raise Exception("Can't be used on sliced perm spaces. Try "
                            "`perm_space.unsliced.get_fixed(...)`.")
        combined_fixed_map = dict(self.fixed_map)
        for key, value in fixed_map.items():
            if key in self.fixed_map:
                assert self.fixed_map[key] == value
            combined_fixed_map[key] = value
            
        return PermSpace(
            self.sequence, domain=self.domain, fixed_map=combined_fixed_map,
            degrees=self.degrees, slice_=None,
            n_elements=self.n_elements, is_combination=self.is_combination
        )
    
    @caching.CachedProperty
    def unfixed(self):
        '''An unfixed version of this `PermSpace`.'''
        if self.is_sliced:
            raise Exception("Can't be used on sliced perm spaces. Try "
                            "`perm_space.unsliced.unfixed`.")
        return PermSpace(
            self.sequence, domain=self.domain, fixed_map=None,
            degrees=self.degrees, n_elements=self.n_elements,
            is_combination=self.is_combination
        )
    
    
    @caching.CachedProperty
    def _n_cycles_in_fixed_items_of_just_fixed(self):
        '''
        The number of cycles in the fixed items of this `PermSpace`.
        
        This is used for degree calculations.
        '''
        unvisited_items = set(self._undapplied_unrapplied_fixed_map)
        n_cycles = 0
        while unvisited_items:
            starting_item = current_item = next(iter(unvisited_items))
            
            while current_item in unvisited_items:
                unvisited_items.remove(current_item)
                current_item = \
                            self._undapplied_unrapplied_fixed_map[current_item]
                
            if current_item == starting_item:
                n_cycles += 1
                
        return n_cycles
    
    
    @caching.CachedProperty
    def fixed_indices(self):
        '''The indices of any fixed items in this `PermSpace`.'''
        if not self.fixed_map:
            return ()
        return tuple(map(self.domain.index, self.fixed_map))
    
    free_indices = caching.CachedProperty(
        lambda self: tuple(item for item in range(self.sequence_length)
                           if item not in self._undapplied_fixed_map.keys()),
        doc='Integer indices of items that can change between permutations.'
    )
    free_keys = caching.CachedProperty(
        lambda self: tuple(item for item in self.domain
                           if item not in self.fixed_map.keys()),
        doc='Indices (possibly from domain) of items that can change between '
             'permutations.'
        
    )
    free_values = caching.CachedProperty(
        lambda self: tuple(item for item in self.sequence
                           if item not in self.fixed_map.values()), 
        doc='Items that can change between permutations.'
    )
    
    
    def __lt__(self, other):
        if isinstance(other, PermSpace):
            return self._reduced < other._reduced
        else:
            return NotImplemented
        
        
    def __reduce__(self, *args, **kwargs):
        #######################################################################
        #                                                                     #
        self._just_fixed
        # (Getting this generated because we can't save a lambda.)
        try:
            del self._get_just_fixed
        except AttributeError:
            pass
        #                                                                     #
        #######################################################################
        return super(PermSpace, self).__reduce__(*args, **kwargs)
        
        
    def _coerce_perm(self, perm):
        '''Coerce `perm` to be a permutation of this space.'''
        return Perm(perm, self)
        
        

from .perm import Perm

# Must set this after-the-fact because of import loop:
PermSpace.perm_type = Perm
