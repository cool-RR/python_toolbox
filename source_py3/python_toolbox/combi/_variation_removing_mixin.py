from python_toolbox import caching

# (`PermSpace` exported to here from `perm_space.py` to avoid import loop.)


class _VariationRemovingMixin:
    purified = caching.CachedProperty(
        lambda self: PermSpace(len(self.sequence)),
        doc='''An purified version of this `PermSpace`.'''
    )
    unrapplied = caching.CachedProperty(
        lambda self: PermSpace(
            self.sequence_length, domain=self.domain, 
            fixed_map={key: self.sequence.index(value) for
                       key, value in self.fixed_map.items()},
            degrees=self.degrees, slice_=self.canonical_slice,
            n_elements=self.n_elements, is_combination=self.is_combination
        ),
        doc='''A version of this `PermSpace` without a custom range.'''
    )
    unreccurented = caching.CachedProperty(
        lambda self: 1 / 0, # blocktodo
        doc='''A non-recurrent version of this `PermSpace`.'''
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

    undapplied = caching.CachedProperty(
        lambda self: PermSpace(
            self.sequence, fixed_map=self._undapplied_fixed_map,
            degrees=self.degrees, slice_=self.canonical_slice,
            n_elements=self.n_elements, is_combination=self.is_combination
        ),
        doc='''A version of this `PermSpace` without a custom domain.'''
    )

    @caching.CachedProperty
    def uncombinationed(self):
        '''A version of this `PermSpace` where permutations have order.'''
        if self.is_sliced:
            raise Exception(
                "Can't convert sliced `CombSpace` directly to "
                "uncombinationed, because the number of items would be "
                "different. Use `.unsliced` first."
            )
        return PermSpace(
            self.sequence, domain=self.domain, fixed_map=self.fixed_map,
            degrees=self.degrees, slice_=None,
            n_elements=self.n_elements, is_combination=False
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
    def undegreed(self):
        '''An undegreed version of this `PermSpace`.'''
        if self.is_sliced:
            raise Exception("Can't be used on sliced perm spaces. Try "
                            "`perm_space.unsliced.undegreed`.")
        return PermSpace(
            self.sequence, domain=self.domain, fixed_map=self.fixed_map,
            degrees=None, n_elements=self.n_elements,
            is_combination=self.is_combination
        )
    
    unsliced = caching.CachedProperty(
        lambda self: PermSpace(
            self.sequence, domain=self.domain, fixed_map=self.fixed_map,
            n_elements=self.n_elements, is_combination=self.is_combination, 
            degrees=self.degrees, slice_=None
        ),
        doc='''An unsliced version of this `PermSpace`.'''
    )
        