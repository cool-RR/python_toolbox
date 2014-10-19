# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import collections

from python_toolbox import caching

# (`PermSpace` exported to here from `perm_space.py` to avoid import loop.)


class _FixedMapManagingMixin:
    '''
    Mixin for `PermSpace` to manage the `fixed_map`. (For fixed perm spaces.)
    '''
    
    @caching.CachedProperty
    def fixed_indices(self):
        '''
        The indices of any fixed items in this `PermSpace`.
        
        This'll be different from `self.fixed_map.keys()` for dapplied perm
        spaces.
        '''
        if not self.fixed_map:
            return ()
        return tuple(map(self.domain.index, self.fixed_map))
    
    free_indices = caching.CachedProperty(
        lambda self: tuple(item for item in range(self.sequence_length)
                           if item not in self._undapplied_fixed_map.keys()),
        doc='''Integer indices of free items.'''
    )
    free_keys = caching.CachedProperty(
        lambda self: tuple(item for item in self.domain
                           if item not in self.fixed_map.keys()),
        doc='''Indices (possibly from domain) of free items.'''
        
    )
    
    @caching.CachedProperty
    def free_values(self):
        '''Items that can change between permutations.'''
        # This algorithm is required instead of just a one-liner because in the
        # case of recurrent sequences, we don't want to remove all the sequence
        # items that are in `self.fixed_map.values()` but only as many as there
        # are in `self.fixed_map.values()`.
        free_values = []
        fixed_counter = collections.Counter(self.fixed_map.values())
        for item in self.sequence:
            if fixed_counter[item]:
                fixed_counter[item] -= 1
            else:
                free_values.append(item)
        return tuple(free_values)
    
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
    
