# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import misc_tools
from python_toolbox import caching

from .. import misc

# (`PermSpace` exported to here from `perm_space.py` to avoid import loop.)


class _VariationRemovingMixin:
    '''Mixin for `PermSpace` to add variations to a perm space.'''
    purified = caching.CachedProperty(
        lambda self: PermSpace(len(self.sequence)),
        doc='''A purified version of this `PermSpace`.'''
    )

    ###########################################################################

    @caching.CachedProperty
    def unrapplied(self):
        '''A version of this `PermSpace` without a custom range.'''
        if self.is_recurrent and self.is_sliced:
            raise TypeError(
                "You can't get an unrapplied version of a recurrent, sliced "
                "`PermSpace` because after unrapplying it, it'll no longer be "
                "recurrent, and thus have a different number of elements, and "
                "thus the slice wouldn't be usable. Please use `.unsliced` "
                "first."
            )
        return PermSpace(
            self.sequence_length, n_elements=self.n_elements,
            domain=self.domain,
            fixed_map={key: self.sequence.index(value) for
                       key, value in self.fixed_map.items()},
            degrees=self.degrees, slice_=self.canonical_slice,
            is_combination=self.is_combination, perm_type=self.perm_type
        )

    @caching.CachedProperty
    def unrecurrented(self):
        '''A version of this `PermSpace` with no recurrences.'''
        from .perm import UnrecurrentedPerm
        from .comb import UnrecurrentedComb
        assert self.is_recurrent # Otherwise was overridden in `__init__`
        if self.is_sliced:
            raise TypeError(
                "You can't get an unrecurrented version of a sliced "
                "`PermSpace` because after unrecurrenting it, it'll have a "
                "different number of elements, and thus the slice wouldn't be "
                "usable. Please use `.unsliced` first."
            )
        if self.is_typed:
            raise TypeError(
                "You can't get an unrecurrented version of a typed "
                "`PermSpace`, because we need to use the "
                "`UnrecurrentedPerm` type to unrecurrent it."
            )

        sequence_copy = list(self.sequence)
        processed_fixed_map = {}
        for key, value in self.fixed_map:
            index = sequence_copy.index(value)
            sequence_copy[value] = misc.MISSING_ELEMENT
            processed_fixed_map[key] = (index, value)


        return PermSpace(
            enumerate(self.sequence), n_elements=self.n_elements,
            domain=self.domain, fixed_map=processed_fixed_map,
            degrees=self.degrees, is_combination=self.is_combination,
            perm_type=UnrecurrentedComb if self.is_combination
                                                         else UnrecurrentedPerm
        )


    @caching.CachedProperty
    def unpartialled(self):
        '''A non-partial version of this `PermSpace`.'''
        assert self.is_partial # Otherwise this property would be overridden.
        if self.is_sliced:
            raise TypeError(
                "Can't convert sliced `PermSpace` directly to unpartialled, "
                "because the number of items would be different. Use "
                "`.unsliced` first."
            )
        if self.is_dapplied:
            raise TypeError(
                "Can't convert a partial, dapplied `PermSpace` to "
                "non-partialled, because we'll need to extend the domain with "
                "more items and we don't know which to use."
            )

        return PermSpace(
            self.sequence, n_elements=self.sequence_length,
            fixed_map=self.fixed_map, degrees=self.degrees,
            slice_=self.canonical_slice, is_combination=self.is_combination,
            perm_type=self.perm_type
        )

    @caching.CachedProperty
    def uncombinationed(self):
        '''A version of this `PermSpace` where permutations have order.'''
        from .perm import Perm
        if self.is_sliced:
            raise TypeError(
                "Can't convert sliced `CombSpace` directly to "
                "uncombinationed, because the number of items would be "
                "different. Use `.unsliced` first."
            )
        if self.is_typed:
            raise TypeError(
                "Can't convert typed `CombSpace` directly to "
                "uncombinationed, because the perm class would still be a "
                "subclass of `Comb`."
            )
        return PermSpace(
            self.sequence, n_elements=self.n_elements, domain=self.domain,
            fixed_map=self.fixed_map, degrees=self.degrees, slice_=None,
            is_combination=False, perm_type=Perm
        )

    undapplied = caching.CachedProperty(
        lambda self: PermSpace(
            self.sequence, n_elements=self.n_elements,
            fixed_map=self._undapplied_fixed_map, degrees=self.degrees,
            slice_=self.canonical_slice, is_combination=self.is_combination,
            perm_type=self.perm_type
        ),
        doc='''A version of this `PermSpace` without a custom domain.'''
    )

    @caching.CachedProperty
    def unfixed(self):
        '''An unfixed version of this `PermSpace`.'''
        if self.is_sliced:
            raise TypeError("Can't be used on sliced perm spaces. Try "
                            "`perm_space.unsliced.unfixed`.")
        return PermSpace(
            self.sequence, n_elements=self.n_elements,
            domain=self.domain, fixed_map=None, degrees=self.degrees,
            is_combination=self.is_combination, perm_type=self.perm_type
        )

    @caching.CachedProperty
    def undegreed(self):
        '''An undegreed version of this `PermSpace`.'''
        if self.is_sliced:
            raise TypeError("Can't be used on sliced perm spaces. Try "
                            "`perm_space.unsliced.undegreed`.")
        return PermSpace(
            self.sequence, n_elements=self.n_elements, domain=self.domain,
            fixed_map=self.fixed_map, degrees=None,
            is_combination=self.is_combination, perm_type=self.perm_type
        )

    unsliced = caching.CachedProperty(
        lambda self: PermSpace(
            self.sequence, n_elements=self.n_elements, domain=self.domain,
            fixed_map=self.fixed_map, is_combination=self.is_combination,
            degrees=self.degrees, slice_=None, perm_type=self.perm_type
        ),
        doc='''An unsliced version of this `PermSpace`.'''
    )

    untyped = caching.CachedProperty(
        lambda self: PermSpace(
            self.sequence, n_elements=self.n_elements, domain=self.domain,
            fixed_map=self.fixed_map, is_combination=self.is_combination,
            degrees=self.degrees, slice_=self.slice_,
            perm_type=self.default_perm_type
        ),
        doc='''An untyped version of this `PermSpace`.'''
    )

    ###########################################################################
    ###########################################################################

    # More exotic variation removals below:

    _just_fixed = caching.CachedProperty(
        lambda self: self._get_just_fixed(),
        """A version of this perm space without any variations except fixed."""
    )

    def _get_just_fixed(self):
        # This gets overridden in `__init__`.
        raise RuntimeError


    _nominal_perm_space_of_perms = caching.CachedProperty(
        lambda self: self.unsliced.undegreed.unfixed,
    )

