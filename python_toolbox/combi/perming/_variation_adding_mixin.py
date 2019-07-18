# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import caching
from python_toolbox import sequence_tools

# (`PermSpace` exported to here from `perm_space.py` to avoid import loop.)


class _VariationAddingMixin:
    '''Mixin for `PermSpace` to add variations to a perm space.'''
    def get_rapplied(self, sequence):
        '''Get a version of this `PermSpace` that has a range of `sequence`.'''
        if self.is_rapplied:
            raise TypeError('This space is already rapplied, to rapply it to a '
                            'different sequence please use `.unrapplied` '
                            'first.')
        sequence = \
                 sequence_tools.ensure_iterable_is_immutable_sequence(sequence)
        if len(sequence) != self.sequence_length:
            raise Exception
        return PermSpace(
            sequence, n_elements=self.n_elements, domain=self.domain,
            fixed_map={key: sequence[value] for key, value in
                                                       self.fixed_map.items()},
            degrees=self.degrees, slice_=self.canonical_slice,
            is_combination=self.is_combination,
            perm_type=self.perm_type
        )

    # There's no `.get_recurrented` because we can't know which sequence you'd
    # want. If you want a recurrent perm space you need to use `.get_rapplied`
    # with a recurrent sequence.

    def get_partialled(self, n_elements):
        '''Get a partialled version of this `PermSpace`.'''
        if self.is_sliced:
            raise TypeError(
                "Can't get partial of sliced `PermSpace` directly, because "
                "the number of items would be different. Use `.unsliced` "
                "first."
            )
        return PermSpace(
            self.sequence, n_elements=n_elements, domain=self.domain,
            fixed_map=self.fixed_map, degrees=self.degrees, slice_=None,
            is_combination=self.is_combination,
            perm_type=self.perm_type
        )

    @caching.CachedProperty
    def combinationed(self):
        '''Get a combination version of this perm space.'''
        from .comb import Comb
        if self.is_sliced:
            raise TypeError(
                "Can't get a combinationed version of a sliced `PermSpace`"
                "directly, because the number of items would be different. "
                "Use `.unsliced` first."
            )
        if self.is_typed:
            raise TypeError(
                "Can't convert typed `PermSpace` directly to "
                "combinationed, because the perm class would not be a "
                "subclass of `Comb`."
            )
        if self.is_degreed:
            raise TypeError("Can't use degrees with combination spaces.")

        return PermSpace(
            self.sequence, n_elements=self.n_elements, domain=self.domain,
            fixed_map=self.fixed_map, is_combination=True,
            perm_type=Comb
        )


    def get_dapplied(self, domain):
        '''Get a version of this `PermSpace` that has a domain of `domain`.'''
        from . import variations

        if self.is_combination:
            raise variations.UnallowedVariationSelectionException(
                {variations.Variation.DAPPLIED: True,
                 variations.Variation.COMBINATION: True,}
            )
        domain = sequence_tools.ensure_iterable_is_immutable_sequence(domain)
        if len(domain) != self.n_elements:
            raise Exception
        return PermSpace(
            self.sequence, n_elements=self.n_elements, domain=domain,
            fixed_map={domain[key]: value for key, value in
                                                   self._undapplied_fixed_map},
            degrees=self.degrees, slice_=self.canonical_slice,
            is_combination=self.is_combination,
            perm_type=self.perm_type
        )

    def get_fixed(self, fixed_map):
        '''Get a fixed version of this `PermSpace`.'''
        if self.is_sliced:
            raise TypeError(
                "Can't be used on sliced perm spaces. Try "
                "`perm_space.unsliced.get_fixed(...)`. You may then re-slice "
                "the resulting space."
            )
        combined_fixed_map = dict(self.fixed_map)
        for key, value in fixed_map.items():
            if key in self.fixed_map:
                assert self.fixed_map[key] == value
            combined_fixed_map[key] = value

        return PermSpace(
            self.sequence, n_elements=self.n_elements, domain=self.domain,
            fixed_map=combined_fixed_map, degrees=self.degrees, slice_=None,
            is_combination=self.is_combination, perm_type=self.perm_type
        )

    def get_degreed(self, degrees):
        '''Get a version of this `PermSpace` restricted to certain degrees.'''
        from . import variations

        if self.is_sliced:
            raise TypeError(
                "Can't be used on sliced perm spaces. Try "
                "`perm_space.unsliced.get_degreed(...)`. You may then "
                "re-slice the resulting space."
            )
        if self.is_combination:
            raise variations.UnallowedVariationSelectionException(
                {variations.Variation.DEGREED: True,
                 variations.Variation.COMBINATION: True,}
            )
        degrees = sequence_tools.to_tuple(degrees, item_type=int)
        if not degrees:
            return self
        degrees_to_use = \
           degrees if not self.is_degreed else set(degrees) & set(self.degrees)
        return PermSpace(
            self.sequence, n_elements=self.n_elements, domain=self.domain,
            fixed_map=self.fixed_map, degrees=degrees_to_use,
            is_combination=self.is_combination, perm_type=self.perm_type
        )

    # There's no `get_sliced` because slicing is done using Python's normal
    # slice notation, e.g. perm_space[4:-7].

    def get_typed(self, perm_type):
        '''
        Get a version of this `PermSpace` where perms are of a custom type.
        '''
        return PermSpace(
            self.sequence, n_elements=self.n_elements, domain=self.domain,
            fixed_map=self.fixed_map, degrees=self.degrees,
            slice_=self.canonical_slice, is_combination=self.is_combination,
            perm_type=perm_type
        )
