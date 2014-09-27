# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

import collections
import abc
import functools
import types
import sys
import math
import numbers
import enum

from python_toolbox import misc_tools
from python_toolbox import nifty_collections
from python_toolbox import sequence_tools
from python_toolbox import caching
import python_toolbox.arguments_profiling
from python_toolbox import math_tools
from python_toolbox import sequence_tools
from python_toolbox import cute_iter_tools
from python_toolbox import nifty_collections
from python_toolbox import dict_tools
from python_toolbox.third_party import sortedcontainers
from python_toolbox import misc_tools

from . import misc
from . import variations
from .variations import UnallowedVariationSelectionException
from ._variation_removing_mixin import _VariationRemovingMixin
from ._variation_adding_mixin import _VariationAddingMixin
from ._fixed_map_managing_mixin import _FixedMapManagingMixin

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
                raise UnallowedVariationSelectionException(
                    {variations.Variation.FIXED: True,
                     variations.Variation.COMBINATION: True,}
                )
            return super(PermSpaceType, CombSpace).__call__(
                iterable_or_length=arguments_profile['iterable_or_length'], 
                n_elements=arguments_profile['n_elements'], 
                slice_=arguments_profile['slice_'],
                _domain_for_checking=arguments_profile['domain'],
                _degrees_for_checking=arguments_profile['degrees'],
            )
        else:
            return super().__call__(*args, **kwargs)
        
        
@functools.total_ordering
class PermSpace(_VariationRemovingMixin, _VariationAddingMixin,
                _FixedMapManagingMixin, sequence_tools.CuteSequenceMixin,
                collections.Sequence, metaclass=PermSpaceType):
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
    
    There are several variations that a perm space could have:
     - Rapplied (Range-applied): having an arbitrary sequence as a range.
       To make one, pass your sequence as the first argument.
     - Dapplied (Domain-applied): having an arbitrary sequence as a domain.
       To make one, pass a sequence into the `domain` argument.
     - Fixed: Having a specified number of indices always pointing at certain
       values, making the space smaller. To make one, pass a dict from each
       key to the value it should be fixed to as the argument `fixed_map`.
     - Sliced: A perm space can be sliced like any Python sequence (except you
       can't change the step.) To make one, use slice notation on an existing
       perm space, e.g. perm_space[56:100]
     - Degreed: A perm space can be limited to perms of a certain degree. (A
       perm's degree is the number of transformations it takes to make it.)
       To make one, pass into the `degrees` argument either a single degree
       (like `5`) or a tuple of different degrees (like `(1, 3, 7)`)
     - Partial: A perm space can be partial, in which case not all elements
       are used in perms. E.g. you can have a perm space of a sequence of
       length 5 but with `n_elements=3`, so every perm will have only 3 items.
       (These are usually called "k-permutations" in math-land.) To make one,
       pass a number as the argument `n_elements`.
     - Combination: If you pass in `is_combination=True` or use the subclass
       `CombSpace`, then you'll have a space of combinations (combs) instead of
       perms. Combs are like perms except there's no order to the elements.

    Note: Some of the options are not allowed to be used with each other.
    
    For each of these variations, there's a function to make a perm space have
    that variation and get rid of it. For example, if you want to make a normal
    perm space be degreed, call `.get_degreed()` on it with the desired
    degrees. If you want to make a degreed perm space non-degreed, access its
    `.undegreed` property. The same is true for all other variations.
    
    A perm space that has none of these variations is called pure.
    '''
    
    @classmethod
    def coerce(cls, argument):
        '''Make `argument` into something of class `cls` if it isn't.'''
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
            self.sequence = sequence_tools.CuteRange(iterable_or_length)
            self.sequence_length = iterable_or_length
        else:
            assert isinstance(iterable_or_length, collections.Iterable)
            self.sequence = sequence_tools. \
                      ensure_iterable_is_immutable_sequence(iterable_or_length)
            range_candidate = sequence_tools.CuteRange(len(self.sequence))
            
            self.is_rapplied = not (
                cute_iter_tools.are_equal(self.sequence,
                                              range_candidate)
            )
            self.sequence_length = len(self.sequence)
            if not self.is_rapplied:
                self.sequence = sequence_tools.CuteRange(self.sequence_length)
        
        #                                                                     #
        ### Finished figuring out sequence and whether space is rapplied. #####
        
        ### Figuring out whether sequence is recurrent: #######################
        #                                                                     #
        if self.is_rapplied:
            self._sequence_counteroid
            # Sets `.is_recurrent` as a side-effect.
        else:
            self.is_recurrent = False
        #                                                                     #
        ### Finished figuring out whether sequence is recurrent. ##############
        
        ### Figuring out number of elements: ##################################
        #                                                                     #
        
        self.n_elements = self.sequence_length if (n_elements is None) \
                                                                else n_elements
        if not 0 <= self.n_elements <= self.sequence_length:
            raise Exception('`n_elements` must be between 0 and %s' %
                                                          self.sequence_length)
        self.is_partial = (self.n_elements < self.sequence_length)
        
        self.indices = sequence_tools.CuteRange(self.n_elements)
        
        #                                                                     #
        ### Finished figuring out number of elements. #########################

        ### Figuring out whether it's a combination: ##########################
        #                                                                     #
        self.is_combination = is_combination
        
        if self.is_combination:
            if fixed_map:
                raise UnallowedVariationSelectionException(
                    {variations.Variation.FIXED: True,
                     variations.Variation.COMBINATION: True,}
                )
        
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
                raise UnallowedVariationSelectionException(
                    {variations.Variation.DAPPLIED: True,
                     variations.Variation.COMBINATION: True,}
                )

            self.domain = domain
            if len(set(self.domain)) < len(self.domain):
                raise Exception('The domain must not have repeating elements.')
        else:
            self.domain = self.indices
            self.undapplied = self
        #                                                                     #
        ### Finished figuring out whether space is dapplied. ##################
        
        ### Doing interim calculation of the length: ##########################
        #                                                                     #
        # The length calculated here will be true only for perm spaces that
        # don't have any additional complications.
        if self.is_recurrent:
            function_to_use = math_tools.catshit if self.is_combination else \
                                                            math_tools.shitfuck
            self._just_recurrented_partialled_combinationed_length = \
                   function_to_use(self.n_elements, self._frozen_crate_counter)
        else:
            self._just_recurrented_partialled_combinationed_length = \
                math_tools.factorial(
                    self.sequence_length,
                    start=(self.sequence_length - self.n_elements + 1)
                ) // (math_tools.factorial(self.n_elements) if
                                                    self.is_combination else 1)
            # This division is always without a remainder, because math.
        #                                                                     #
        ### Finished doing interim calculation of the length. #################
        
        
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
            if self.is_combination:
                raise UnallowedVariationSelectionException(
                    {variations.Variation.FIXED: True,
                     variations.Variation.COMBINATION: True,}
                )
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
                         self._just_recurrented_partialled_combinationed_length
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
            if self.is_combination:
                raise UnallowedVariationSelectionException(
                    {variations.Variation.DEGREED: True,
                     variations.Variation.COMBINATION: True,}
                )
            if self.is_partial:
                raise UnallowedVariationSelectionException(
                    {variations.Variation.DEGREED: True,
                     variations.Variation.PARTIAL: True,}
                )
            if self.is_recurrent:
                raise UnallowedVariationSelectionException(
                    {variations.Variation.DEGREED: True,
                     variations.Variation.RECURRENT: True,}
                )
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
        if not self.is_recurrent:
            self.unrecurrented = self
        if not self.is_partial:
            self.unpartialled = self
        if not self.is_combination:
            self.uncombinationed = self
        # No need do this for `undapplied`, it's already done above.
        if not self.is_fixed:
            self.unfixed = self
        if not self.is_degreed:
            self.undegreed = self
        if not self.is_sliced:
            self.unsliced = self
            
            
    is_recurrent = None
    
    @caching.CachedProperty
    def variation_selection(self):
        variation_selection = variations.VariationSelection(
            filter(
                None,
                (variations.Variation.RAPPLIED if self.is_rapplied else None,
                 variations.Variation.RECURRENT if self.is_recurrent else None,
                 variations.Variation.PARTIAL if self.is_partial else None,
                 variations.Variation.COMBINATION if self.is_combination
                                                                     else None,
                 variations.Variation.DAPPLIED if self.is_dapplied else None,
                 variations.Variation.FIXED if self.is_fixed else None,
                 variations.Variation.DEGREED if self.is_degreed else None,
                 variations.Variation.SLICED if self.is_sliced else None,)
            )
        )
        assert variation_selection.is_allowed
        return variation_selection
    
    @caching.CachedProperty
    def _sequence_counteroid(self):
        '''
        
        Sets `is_recurrent` as a side-effect, or if it was set ensures it was
        set correctly.
        '''
        _sequence_counteroid = collections.OrderedDict()
        is_recurrent = False # Until challenged
        for item in self.sequence:
            if item not in _sequence_counteroid:
                _sequence_counteroid[item] = 0
            else:
                is_recurrent = True
            _sequence_counteroid[item] += 1
        if self.is_recurrent is None:
            self.is_recurrent = is_recurrent
        else:
            assert self.is_recurrent == is_recurrent
        return _sequence_counteroid

            
    @caching.CachedProperty
    def _frozen_crate_counter(self):
        return nifty_collections.FrozenCrateCounter(
            self._sequence_counteroid.values()
        )
        
            
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
            return PermSpace(
                self.sequence, domain=self.domain, n_elements=self.n_elements,
                fixed_map=self.fixed_map, degrees=self.degrees,
                is_combination=self.is_combination, slice_=canonical_slice
            )
        
        else:
            assert isinstance(i, numbers.Integral)
            if i <= -1:
                i += self.length
            if not (0 <= i < self.length):
                raise IndexError
            if self.is_rapplied:
                return self.perm_type(self.unrapplied[i].apply(self.sequence),
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
                return self.perm_type((wip_perm_sequence_dict[k] for k in
                                       self.domain), self)
            elif self.is_fixed:
                free_values_perm = self._free_values_unsliced_perm_space[i]
                free_values_perm_iterator = iter(free_values_perm)
                return self.perm_type(
                    tuple(
                        (self._undapplied_fixed_map[m] if
                         (m in self.fixed_indices) else
                         next(free_values_perm_iterator))
                                           for m in range(self.sequence_length)
                    ),
                    self
                )
            
            else:
                return self.perm_type(i, self)
                
                
    enumerated_sequence = caching.CachedProperty(
        lambda self: tuple(enumerate(self.sequence))
    )
                
    n_unused_elements = caching.CachedProperty(
        lambda self: self.sequence_length - self.n_elements,
        '''In partial perm spaces, number of elements that aren't used.'''
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
        doc='''Short string describing size of space, e.g. "12!"'''
    )
    
    __bool__ = lambda self: bool(self.length)
    
    
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
        return super().__reduce__(*args, **kwargs)
        
        
    def _coerce_perm(self, perm):
        '''Coerce `perm` to be a permutation of this space.'''
        return Perm(perm, self)
        
        

from .perm import Perm
from . import _variation_removing_mixin
from . import _variation_adding_mixin
from . import _fixed_map_managing_mixin

# Must set these after-the-fact because of import loop:
PermSpace.perm_type = Perm
_variation_removing_mixin.PermSpace = PermSpace
_variation_adding_mixin.PermSpace = PermSpace
_fixed_map_managing_mixin.PermSpace = PermSpace