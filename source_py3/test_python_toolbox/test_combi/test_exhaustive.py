# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

import pickle
import itertools
import collections

import nose

from python_toolbox import context_management
from python_toolbox import sequence_tools

from python_toolbox import combi
from python_toolbox.combi import *

infinity = float('inf')
infinities = (infinity, -infinity)


class BrutePermSpace:
    def __init__(self, iterable_or_length, domain=None, n_elements=None,
                 fixed_map=None, degrees=None, is_combination=False,
                 slice_=None):
        self.sequence = tuple(iterable_or_length) if \
            isinstance(iterable_or_length, collections.Iterable) else \
                                   sequence_tools.CuteRange(iterable_or_length)
        self.sequence_length = len(self.sequence)
        self._sequence_counter = collections.Counter(self.sequence)
        self.domain = domain or sequence_tools.CuteRange(self.sequence_length)
        self.n_elements = n_elements if n_elements is not None else \
                                                             len(self.sequence)
        self.fixed_map = fixed_map or {}
        self.degrees = \
                      degrees or sequence_tools.CuteRange(self.sequence_length)
        self.is_combination = is_combination
        self.slice_ = slice_
        
        self.is_degreed = (self.degrees !=
                                sequence_tools.CuteRange(self.sequence_length))
        
    def __iter__(self):
        if self.slice_:
            return itertools.islice(self._iter())
        else:
            return self._iter()
        
    def _iter(self):
        
        for candidate in itertools.product(*(self.sequence for i in
                                                 range(self.sequence_length))):
            candidate = candidate[:self.n_elements]
            if collections.Counter(candidate) != self._sequence_counter:
                continue
            if any(candidate[self.domain.index(key)] != value for
                                         key, value in self.fixed_map.items()):
                continue
            if self.is_degreed:
                unvisited_items = \
                            set(sequence_tools.CuteRange(self.sequence_length))
                n_cycles = 0
                while unvisited_items:
                    starting_item = current_item = next(iter(unvisited_items))
                    
                    while current_item in unvisited_items:
                        unvisited_items.remove(current_item)
                        current_item = self.sequence.index(
                            candidate[self.sequence.index(current_item)]
                        )
                        
                    if current_item == starting_item:
                        n_cycles += 1
                        
                degree = self.sequence_length - n_cycles
                
                if degree not in self.degrees:
                    continue
            yield candidate
                

def _check_variation_selection(variation_selection):
    assert isinstance(variation_selection, combi.variations.VariationSelection)
    
    kwargs = {}
    
    if variation_selection.is_recurrent and \
                                           not variation_selection.is_rapplied:
        assert not variation_selection.is_allowed
        # Can't even test this illogical clash.
        return 
        
    
    iterable_or_length = (
        'abracab' if variation_selection.is_recurrent else
        tuple(range(60, -10, -10)) if variation_selection.is_rapplied else 7
    )
    kwargs['iterable_or_length'] = iterable_or_length
    sequence = (iterable_or_length if
                isinstance(iterable_or_length, collections.Iterable) else
                sequence_tools.CuteRange(iterable_or_length))
    sequence_set = set(sequence)
    
    if variation_selection.is_dapplied:
        domain = 'isogram'
        kwargs['domain'] = domain
    else:
        domain = sequence_tools.CuteRange(11)
    domain_set = set(domain)
        
    if variation_selection.is_partial:
        kwargs['n_elements'] = 5
        
    if variation_selection.is_combination:
        kwargs['is_combination'] = True
        
    if variation_selection.is_fixed:
        fixed_map = {domain[1]: sequence[1], domain[4]: sequence[3],}
        kwargs['fixed_map'] = fixed_map
    else:
        fixed_map = {}
        
    if variation_selection.is_degreed:
        kwargs['degrees'] = degrees = (0, 2, 4, 5)
        

    context_manager = (
        context_management.BlankContextManager() if
        variation_selection.is_allowed else
        cute_testing.RaiseAssertor(combi.UnallowedVariationSelectionException)
    )
    
    with context_manager:
        perm_space = PermSpace(**kwargs)
        
    if not variation_selection.is_allowed:
        return
    
    brute_perm_space = BrutePermSpace(**kwargs)

    if variation_selection.is_sliced:
        if perm_space.length >= 2:
            perm_space = perm_space[2:-2]
        else:
            assert variation_selection.is_combination and \
                                         not variation_selection.is_partial
            perm_space = perm_space[:0]
    
    
    assert perm_space.variation_selection == variation_selection
    assert perm_space.sequence_length == 7
    
    assert (perm_space.domain == perm_space.sequence) == (
        not variation_selection.is_dapplied and
        not variation_selection.is_rapplied and
        not variation_selection.is_partial
    )
    
    if perm_space.length >= 2:
        assert perm_space[-1] >= perm_space[0]
        assert perm_space[-1] > perm_space[0]
        assert perm_space[0] <= perm_space[-1]
        assert perm_space[0] < perm_space[-1]
        assert perm_space[0] != perm_space[-1]
        
        
    if variation_selection.is_partial:
        assert perm_space.n_unused_elements == 2
    else:
        assert perm_space.n_unused_elements == 0
        
    assert perm_space == PermSpace(**kwargs)[perm_space.canonical_slice]
    assert (not perm_space != PermSpace(**kwargs)[perm_space.canonical_slice])
    assert hash(perm_space) == \
                          hash(PermSpace(**kwargs)[perm_space.canonical_slice])

    if perm_space.is_sliced and perm_space.length >= 2:
        assert perm_space[0] == perm_space.unsliced[2]
        assert perm_space[1] == perm_space.unsliced[3]
        assert perm_space[-1] == perm_space.unsliced[-3]
        assert perm_space[-2] == perm_space.unsliced[-4]
        assert perm_space.unsliced[0] not in perm_space
        assert perm_space.unsliced[1] not in perm_space
        assert perm_space.unsliced[2] in perm_space
        assert perm_space.unsliced[-1] not in perm_space
        assert perm_space.unsliced[-2] not in perm_space
        assert perm_space.unsliced[-3] in perm_space
        
    if perm_space:
        # Making sure that `brute_perm_space` isn't empty:
        next(iter(brute_perm_space))
        # This is crucial otherwise the zip-based loop below won't run and
        # we'll get the illusion that the tests are running while they're
        # really not.
    
    # blocktodo: change to 100 after finished debugging 
    for i, (perm, brute_perm_tuple) in enumerate(
                      itertools.islice(zip(perm_space, brute_perm_space), 10)):
        
        assert tuple(perm) == brute_perm_tuple
        assert perm in perm_space
        
        assert isinstance(perm, combi.Perm)
        assert perm.is_rapplied == variation_selection.is_rapplied
        assert perm.is_dapplied == variation_selection.is_dapplied
        assert perm.is_partial == variation_selection.is_partial
        assert perm.is_combination == variation_selection.is_combination
        assert perm.is_pure == (not (variation_selection.is_rapplied or
                                     variation_selection.is_dapplied or
                                     variation_selection.is_partial or
                                     variation_selection.is_combination))
        
        
        if variation_selection.is_rapplied:
            assert perm != perm.unrapplied
            if not variation_selection.is_recurrent:
                perm.unrapplied == perm_space.unrapplied[i]
        else:
            assert perm == perm.unrapplied == perm_space.unrapplied[i]
            if not variation_selection.is_dapplied:
                assert perm.apply('isogram') == 'isogram' * perm
                assert tuple('isogram' * perm) == tuple(
                    perm_space.get_rapplied('isogram')[i]._perm_sequence
                )
            
        
        if variation_selection.is_dapplied:
            assert perm != perm.undapplied == perm_space.undapplied[i]
        else:
            assert perm == perm.undapplied == perm_space.undapplied[i]
            
        if variation_selection.is_combination:
            assert perm != perm.uncombinationed
        else:
            assert perm == perm.uncombinationed
            
        assert type(perm) == combi.Comb if variation_selection.is_combination \
                                                                else combi.Perm
        
        if variation_selection.variations <= {
            variations.Variation.DAPPLIED, variations.Variation.RAPPLIED,
                                            variations.Variation.COMBINATION,}:
            assert perm.nominal_perm_space == perm_space
        assert perm.nominal_perm_space == \
                                   perm_space._nominal_perm_space_of_perms == \
                                          perm_space.unsliced.undegreed.unfixed
        # Give me your unsliced, your undegreed, your unfixed.
        
        if not variation_selection.is_fixed and \
                                            not variation_selection.is_degreed:
            assert perm_space.index(perm) == i
            if not variation_selection.is_sliced:
                assert perm.number == i
            
        assert Perm(perm.number, perm_space=perm_space) == perm
        assert Perm(perm._perm_sequence, perm_space=perm_space) == perm
        
        assert perm.length == perm_space.n_elements
        if variation_selection.is_partial or variation_selection.is_rapplied \
                                            or variation_selection.is_dapplied:
            with cute_testing.RaiseAssertor(TypeError):
                ~perm
            with cute_testing.RaiseAssertor(TypeError):
                perm.inverse
            with cute_testing.RaiseAssertor(TypeError):
                perm ** -1
        else:
            assert ~perm == perm.inverse == perm ** -1
            assert ~~perm == perm.inverse.inverse == perm == perm ** 1
            assert (perm * ~perm) == (~perm * perm) == \
                                                     perm.nominal_perm_space[0]
            assert isinstance(perm ** 4, Perm)
            assert isinstance(perm ** -7, Perm)
            
        perm_set = set(perm)
        if variation_selection.is_partial:
            assert perm_set < sequence_set
            assert len(perm_set) == 5
            assert len(perm) == 5
        else:
            assert perm_set == sequence_set
            assert len(perm) == 7
            
        for j, (value, key, (key__, value__)) in enumerate(
                                       zip(perm, perm.as_dictoid, perm.items)):
            assert key == key__
            assert value == perm.as_dictoid[key] == value__
            assert perm.items[j] == (key, value)
            if not variation_selection.is_recurrent:
                assert perm.index(value) == key
            assert perm[key] == value
            assert key in perm.domain
            assert value in perm
            
        if variation_selection.is_degreed:
            assert perm.degree in degrees
        elif variation_selection.is_partial:
            assert perm.degree == NotImplemented
        else:
            assert 0 <= perm.degree <= 7
            
        
        ### Testing neighbors: ################################################
        #                                                                     #
        if variation_selection.is_combination or \
            variation_selection.is_recurrent or variation_selection.is_partial:
            with cute_testing.RaiseAssertor(NotImplementedError):
                neighbors = perm.get_neighbors(perm_space=perm_space)
        else:
            neighbors = perm.get_neighbors(perm_space=perm_space)
            if variation_selection.is_degreed and perm.degree in (0, 2):
                assert not neighbors
                # No neighbors in this case because they'll have a degree of 1
                # or 3 which are excluded.
            else:
                assert neighbors
                for neigbhor in neighbors:
                    assert neigbhor in perm_space 
                    assert len(cute_iter_tools.zip_non_equal((perm, neigbhor),
                                                         lazy_tuple=True)) == 2
        
        #                                                                     #
        ### Finished testing neighbors. #######################################
        
        
    # blocktodo add brute force generation of first 100 perms and ensure
    # identical.
    
def test():
    yield from ((_check_variation_selection, variation_selection) for
                variation_selection in combi.variations.variation_selection_space)
    