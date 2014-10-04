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
import inspect

from python_toolbox import misc_tools
from python_toolbox import nifty_collections
from python_toolbox import sequence_tools
from python_toolbox import caching
from python_toolbox import math_tools
from python_toolbox import sequence_tools
from python_toolbox import cute_iter_tools
from python_toolbox import nifty_collections
from python_toolbox import dict_tools
from python_toolbox.third_party import sortedcontainers
from python_toolbox import misc_tools

from .. import misc
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
            arguments = PermSpace.__init__.signature.bind(
                                               None, *args, **kwargs).arguments
            if arguments.get('fixed_map', None):
                raise UnallowedVariationSelectionException(
                    {variations.Variation.FIXED: True,
                     variations.Variation.COMBINATION: True,}
                )
            return super(PermSpaceType, CombSpace).__call__(
                iterable_or_length=arguments['iterable_or_length'], 
                n_elements=arguments.get('n_elements', None),
                slice_=arguments.get('slice_', None),
                _domain_for_checking=arguments.get('domain', None),
                _degrees_for_checking=arguments.get('degrees', None),
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
    
    def __init__(self, iterable_or_length, domain=None, *, n_elements=None, 
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
            self.is_recurrent = any(count >= 2 for count in
                                    self._frozen_ordered_counter.values())
        else:
            self.is_recurrent = False
        #                                                                     #
        ### Finished figuring out whether sequence is recurrent. ##############
        
        ### Figuring out number of elements: ##################################
        #                                                                     #
        
        self.n_elements = self.sequence_length if (n_elements is None) \
                                                                else n_elements
        if not 0 <= self.n_elements <= self.sequence_length:
            raise Exception(
                '`n_elements` must be between 0 and %s, you gave %s' %
                                        (self.sequence_length, self.n_elements)
            )
        self.is_partial = (self.n_elements < self.sequence_length)
        
        self.indices = sequence_tools.CuteRange(self.n_elements)
        
        #                                                                     #
        ### Finished figuring out number of elements. #########################

        ### Figuring out whether it's a combination: ##########################
        #                                                                     #
        self.is_combination = is_combination
        # Well that was quick.
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
            if not (self.is_dapplied or self.is_rapplied or degrees or slice_
                    or (n_elements is not None) or self.is_combination):
                self._just_fixed = self
            else:
                self._get_just_fixed = lambda: PermSpace(
                    len(self.sequence),
                    fixed_map=self._undapplied_unrapplied_fixed_map,
                )
        else:
                
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
        degrees = sequence_tools.to_tuple(degrees, item_type=int)
        
        if (not degrees) or cute_iter_tools.are_equal(degrees, all_degrees):
            self.is_degreed = False
            self.degrees = all_degrees
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
            
        #                                                                     #
        ### Finished figuring out degrees. ####################################
            
        ### Figuring out slice and length: ####################################
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
        ### Finished figuring out slice and length. ###########################
        
        
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

    __init__.signature = inspect.signature(__init__)
            
    @caching.CachedProperty
    def _unsliced_length(self):
        '''
        The number of perms in the space, ignoring any slicing.
        
        This is used as an interim step in calculating the actual length of the
        space with the slice taken into account.
        '''
        if self.is_degreed:
            assert not self.is_recurrent and not self.is_partial and \
                                                        not self.is_combination
            return sum(
                math_tools.abs_stirling(
                    self.sequence_length - len(self.fixed_map),
                    self.sequence_length - degree -
                                    self._n_cycles_in_fixed_items_of_just_fixed
                ) for degree in self.degrees
            )
        elif self.is_fixed:
            assert not self.is_degreed and not self.is_combination
            if self.is_recurrent:
                return math_tools.calculate_length_of_recurrent_perm_space(
                    self.n_elements - len(self.fixed_map),
                    nifty_collections.FrozenTallyTally(
                        collections.Counter(self.free_values).values()
                    )                    
                )
            else:
                return math_tools.factorial(
                    len(self.free_indices),
                    start=(len(self.free_indices) -
                                   (self.n_elements - len(self.fixed_map)) + 1)
                )
            
        else:
            assert not self.is_degreed and not self.is_fixed
            if self.is_recurrent:
                if self.is_combination:
                    return math_tools.calculate_length_of_recurrent_comb_space(
                        self.n_elements,
                        self._frozen_counter_counter
                    )
                else:
                    return math_tools.calculate_length_of_recurrent_perm_space(
                        self.n_elements,
                        self._frozen_counter_counter
                    )
                    
            else:
                return math_tools.factorial(
                    self.sequence_length,
                    start=(self.sequence_length - self.n_elements + 1)
                ) // (math_tools.factorial(self.n_elements) if
                          self.is_combination else 1)
                # This division is always without a remainder, because math.
            
            
        
            
    
    @caching.CachedProperty
    def variation_selection(self):
        '''
        The selection of variations that describe this space.
        
        For example, a rapplied, recurrent, fixed `PermSpace` will get
        `<VariationSelection #196: rapplied, recurrent, fixed>`.
        '''
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
    def _frozen_ordered_counter(self):
        return nifty_collections.FrozenOrderedTally(self.sequence)
            
    _frozen_counter_counter = caching.CachedProperty(
        lambda self: nifty_collections.FrozenTallyTally(
                                         self._frozen_ordered_counter.values())
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
            
        sequence_repr = self.sequence.short_repr if \
                  hasattr(self.sequence, 'short_repr') else repr(self.sequence)
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
        
        assert isinstance(i, numbers.Integral)
        if i <= -1:
            i += self.length
            
        if not (0 <= i < self.length):
            raise IndexError
        elif self.is_sliced:
            return self.unsliced[i + self.canonical_slice.start]
        elif self.is_dapplied:
            return self.perm_type(self.undapplied[i], perm_space=self)
        elif self.is_degreed:
            if self.is_rapplied:
                assert not self.is_recurrent
                return self.perm_type(map(self.sequence.__getitem__,
                                          self.unrapplied[i]),
                                      perm_space=self)
            
            assert not self.is_rapplied and not self.is_recurrent and \
                   not self.is_partial and not self.is_combination and \
                   not self.is_dapplied and not self.is_sliced
            # If that wasn't an example of asserting one's dominance, I don't
            # know what is.
            
            available_values = list(self.free_values)
            wip_perm_sequence_dict = dict(self.fixed_map)
            wip_n_cycles_in_fixed_items = \
                                    self._n_cycles_in_fixed_items_of_just_fixed
            wip_i = i
            for j in self.sequence:
                if j in wip_perm_sequence_dict:
                    continue
                for unused_value in available_values:
                    candidate_perm_sequence_dict = dict(wip_perm_sequence_dict)
                    candidate_perm_sequence_dict[j] = unused_value
                    
                    ### Checking whether we closed a cycle: ###################
                    #                                                         #
                    if j == unused_value:
                        closed_cycle = True
                    else:
                        current = j
                        while True:
                            current = candidate_perm_sequence_dict[current]
                            if current == j:
                                closed_cycle = True
                                break
                            elif current not in candidate_perm_sequence_dict:
                                closed_cycle = False
                                break
                    #                                                         #
                    ### Finished checking whether we closed a cycle. ##########
                    
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
                    
                    
                    if wip_i < candidate_fixed_perm_space_length:
                        available_values.remove(unused_value)
                        wip_perm_sequence_dict[j] = unused_value
                        wip_n_cycles_in_fixed_items = \
                                              candidate_n_cycles_in_fixed_items
                        
                        break
                    wip_i -= candidate_fixed_perm_space_length
                else:
                    raise RuntimeError
            assert wip_i == 0
            return self.perm_type((wip_perm_sequence_dict[k] for k in
                                   self.domain), self)
        elif self.is_recurrent:
            assert not self.is_dapplied and not self.is_degreed and \
                                                             not self.is_sliced
            available_values = list(self.sequence)
            reserved_values = list(self.fixed_map.values())
            wip_perm_sequence_dict = dict(self.fixed_map)
            wip_i = i
            shit_set = set()
            for j in range(self.n_elements):
                if j in self.fixed_map:
                    available_values.remove(self.fixed_map[j])
                    reserved_values.remove(self.fixed_map[j])
                    continue
                for unused_value in nifty_collections.OrderedSet((
                    value for value in available_values if not
                    ((value in reserved_values and available_values.count(value)
                                            == reserved_values.count(value)) or value in shit_set)
                    
                    )):
                    wip_perm_sequence_dict[j] = unused_value
                    
                    ###########################################################
                    #                                                         #
                    # Tricky thing here: Trying to put as much as we can in a
                    # sequence head that'll shorten the sequence we'll give to
                    # the candidate space instead of using a fixed map, if
                    # possible. This is crucial for `CombSpace` which can't use
                    # `fixed_map`.
                    head = []
                    fixed_map_to_use = dict(wip_perm_sequence_dict)
                    n_elements_to_use = self.n_elements
                    for k in sequence_tools.CuteRange(infinity):
                        try:
                            head.append(wip_perm_sequence_dict[k])
                        except KeyError:
                            break
                        else:
                            del fixed_map_to_use[k]
                            n_elements_to_use -= 1
                    sequence_to_use = list(self.sequence)
                    for item in head:
                        if self.is_combination:
                            sequence_to_use = sequence_to_use[
                                sequence_to_use.index(item) + 1:
                            ]
                        else:
                            sequence_to_use.remove(item)
                            
                    sequence_to_use = [x for x in sequence_to_use if x not in
                                       shit_set]
                        
                    fixed_map_to_use = {key - len(head): value for key, value
                                        in fixed_map_to_use.items()}
                    
                    if len(sequence_to_use) < n_elements_to_use:
                        class O: length = 0
                        candidate_sub_perm_space = O()
                    else:
                        candidate_sub_perm_space = PermSpace(
                            sequence_to_use,
                            n_elements=n_elements_to_use,
                            fixed_map=fixed_map_to_use, 
                            is_combination=self.is_combination
                        )
                    #                                                         #
                    ###########################################################
                    
                    if wip_i < candidate_sub_perm_space.length:
                        available_values.remove(unused_value)
                        break
                    else:
                        wip_i -= candidate_sub_perm_space.length
                        if self.is_combination:
                            shit_set.add(wip_perm_sequence_dict[j])
                        del wip_perm_sequence_dict[j]
                else:
                    raise RuntimeError
            assert wip_i == 0
            return self.perm_type(
                dict_tools.get_list(wip_perm_sequence_dict, self.domain),
                self
            )
        
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
        
        elif self.is_combination:
            wip_number = self.length - 1 - i
            wip_perm_sequence = []
            for i in range(self.n_elements, 0, -1):
                for j in range(self.sequence_length, i - 2, -1):
                    candidate = math_tools.binomial(j, i)
                    if candidate <= wip_number:
                        wip_perm_sequence.append(
                            self.sequence[-(j+1)]
                        )
                        wip_number -= candidate
                        break
                else:
                    raise RuntimeError
            result = tuple(wip_perm_sequence)
            assert len(result) == self.n_elements
            return self.perm_type(result, self)

        
        else:
            factoradic_number = math_tools.to_factoradic(
                i * math.factorial(
                     self.n_unused_elements),
                n_digits_pad=self.sequence_length
            )
            if self.is_partial:
                factoradic_number = factoradic_number[:-self.n_unused_elements]
            unused_numbers = list(self.sequence)
            result = tuple(unused_numbers.pop(factoradic_digit) for
                                             factoradic_digit in factoradic_number)
            assert sequence_tools.get_length(result) == self.n_elements
            
            return self.perm_type(result, self)
                
                
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
                      tuple(sorted(self.fixed_map.items())),
                      self.canonical_slice)
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
            perm = self.perm_type(perm, self)
            
        if self.sequence != perm.nominal_perm_space.sequence:
            # (This also covers `self.rapplied != perm.rapplied`)
            raise ValueError
        if self.domain != perm.domain:
            # (This also covers `self.dapplied != perm.dapplied`)
            raise ValueError
        if self.is_degreed and (perm.degree not in self.degrees):
            raise ValueError
        
        # At this point we know the permutation contains the correct items, and
        # has the correct degree.
        if perm.is_dapplied: return self.undapplied.index(perm.undapplied)
        if self.is_degreed:
            if perm.is_rapplied: return self.unrapplied.index(perm.unrapplied)
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
                    
                wip_perm_sequence_dict[self.domain[i]] = value
                
            perm_number = wip_perm_number
            
        elif self.is_recurrent:
            assert not self.is_degreed and not self.is_dapplied

            wip_perm_number = 0
            unused_values = list(self.sequence)
            reserved_values = list(self.fixed_map.values())
            perm_sequence_list = list(perm._perm_sequence)
            shit_set = set()
            for i, value in enumerate(perm):
                if i in self.fixed_map:
                    if self.fixed_map[i] == value:
                        unused_values.remove(value)
                        reserved_values.remove(value)
                        continue
                    else:
                        raise ValueError
                lower_values = [
                    thing for thing in
                    nifty_collections.OrderedSet(unused_values) if
                    (thing not in reserved_values or unused_values.count(thing)
                     > reserved_values.count(thing)) and 
                    unused_values.index(thing) < unused_values.index(value) and
                                                          thing not in shit_set
                ]
                unused_values.remove(value)
                for lower_value in lower_values:
                    temp_fixed_map = dict(
                            enumerate(perm_sequence_list[:i] + [lower_value])
                    )
                    temp_fixed_map.update(self.fixed_map)
                    
                    
                    head = []
                    n_elements_to_use = self.n_elements
                    for k in sequence_tools.CuteRange(infinity):
                        try:
                            head.append(temp_fixed_map[k])
                        except KeyError:
                            break
                        else:
                            del temp_fixed_map[k]
                            n_elements_to_use -= 1
                    sequence_to_use = list(self.sequence)
                    for item in head:
                        if self.is_combination:
                            sequence_to_use = sequence_to_use[
                                sequence_to_use.index(item) + 1:
                            ]
                        else:
                            sequence_to_use.remove(item)

                    sequence_to_use = [x for x in sequence_to_use if x not in shit_set]
                    
                    temp_fixed_map = {key - len(head): value for key, value in temp_fixed_map.items()}
                    
                    if len(sequence_to_use) >= n_elements_to_use:
                        wip_perm_number += PermSpace(
                            sequence_to_use,
                            fixed_map=temp_fixed_map,
                            n_elements=n_elements_to_use,
                            is_combination=self.is_combination
                        ).length
                    if self.is_combination:
                        shit_set.add(lower_value)
                    
                
            perm_number = wip_perm_number
            
        elif self.is_fixed:
            assert not self.is_degreed and not self.is_recurrent
            free_values_perm_sequence = []
            for i, perm_item in perm.items:
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
            
            
        elif self.is_combination:
            if perm.is_rapplied:
                return self.unrapplied.index(perm.unrapplied)
            
            processed_perm_sequence = tuple(
                self.sequence_length - 1 -
                                     item for item in perm._perm_sequence[::-1]
            )
            perm_number = self.unsliced.length - 1 - sum(
                (math_tools.binomial(item, i) for i, item in
                                      enumerate(processed_perm_sequence, start=1)),
                0
            )
        
            
              
        else:
            
            factoradic_number = []
            unused_values = list(self.sequence)
            for i, value in enumerate(perm):
                index_of_current_number = unused_values.index(value)
                factoradic_number.append(index_of_current_number)
                unused_values.remove(value)
            perm_number = math_tools.from_factoradic(
                factoradic_number +
                [0] * self.n_unused_elements
            ) // math.factorial(self.n_unused_elements)
            
            
        if perm_number not in self.canonical_slice:
            raise ValueError
            
        return perm_number - self.canonical_slice.start
    
    
    @caching.CachedProperty
    def short_length_string(self):
        '''Short string describing size of space, e.g. "12!"'''
        if not self.is_recurrent and not self.is_partial and \
           not self.is_combination and not self.is_fixed and \
                                                            not self.is_sliced:
            assert self.length == math_tools.factorial(self.sequence_length)
            return misc.get_short_factorial_string(self.sequence_length)
        else:
            return str(self.length)
    
    __bool__ = lambda self: bool(self.length)
    
    _domain_set = caching.CachedProperty(lambda self: set(self.domain))
    
    
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