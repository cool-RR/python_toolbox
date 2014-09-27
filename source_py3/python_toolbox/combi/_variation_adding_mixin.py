from python_toolbox import caching
from python_toolbox import sequence_tools

# (`PermSpace` exported to here from `perm_space.py` to avoid import loop.)


class _VariationAddingMixin:

    def get_rapplied(self, sequence):
        '''Get a version of this `PermSpace` that has a range of `sequence`.'''
        assert not self.is_rapplied
        sequence = \
             sequence_tools.ensure_iterable_is_immutable_sequence(sequence)
        if len(sequence) != self.sequence_length:
            raise Exception
        return PermSpace(
            sequence, domain=self.domain,
            fixed_map={key: sequence[value] for key, value in
                                                       self.fixed_map.items()},
            degrees=self.degrees, slice_=self.canonical_slice,
            n_elements=self.n_elements, is_combination=self.is_combination
        )
    
    # There's no `.get_recurrented` because we can't know which sequence you'd
    # want. If you want a recurrent perm space you need to use `.get_rapplied`
    # with a recurrent sequence.
    
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
    def combinationed(self):
        if self.is_sliced:
            raise Exception(
                "Can't get partial of sliced `PermSpace` directly, because the "
                "number of items would be different. Use `.unsliced` first."
            )
        if self.is_degreed:
            raise Exception("Can't use degrees with combination spaces.")
        
        return PermSpace(
            self.sequence, domain=self.domain, n_elements=self.n_elements,
            fixed_map=self.fixed_map, is_combination=True
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
    
    def get_degreed(self, degrees):
        '''Get a degreed version of this `PermSpace`.'''
        if self.is_sliced:
            raise Exception("Can't be used on sliced perm spaces. Try "
                            "`perm_space.unsliced.get_degreed(...)`.")
        if self.is_combination:
            raise Exception("Can't use degrees with combination spaces.")
        degrees = sequence_tools.to_tuple(degrees, item_type=int)
        if not degrees:
            return self
        degrees_to_use = \
           degrees if not self.is_degreed else set(degrees) & set(self.degrees)
        return PermSpace(
            self.sequence, domain=self.domain, fixed_map=self.fixed_map,
            degrees=degrees_to_use, n_elements=self.n_elements,
            is_combination=self.is_combination
        )
    
    # There's no `get_sliced` because slicing is done using Python's normal
    # slice notation, e.g. perm_space[4:-7].
    