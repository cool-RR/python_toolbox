# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import pickle
import itertools
import collections
import ast

import nose

from python_toolbox import nifty_collections
from python_toolbox import context_management
from python_toolbox import cute_iter_tools
from python_toolbox import cute_testing
from python_toolbox import misc_tools
from python_toolbox import sequence_tools

from python_toolbox import combi
from python_toolbox.combi import *

infinity = float('inf')
infinities = (infinity, -infinity)


class _NO_ARGUMENT_TYPE(type):
    __repr__ = lambda cls: '<%s>' % cls.__name__
        

class NO_ARGUMENT(object):
    __metaclass__ = _NO_ARGUMENT_TYPE
        


class BrutePermSpace(object):
    '''
    A `PermSpace` substitute used for testing `PermSpace`.
    
    This class is used for comparing with `PermSpace` in tests and ensuring it
    produces the same results. The reason we have high confidence that
    `BrutePermSpace` itself produces true results is because it's
    implementation is much simpler than `PermSpace`'s, which is because it
    doesn't need to be efficient, because it's only used for tests.
    
    `BrutePermSpace` takes the some signature of arguments used for
    `PermSpace`, though it's not guaranteed to be able to deal with all the
    kinds of arguments that `PermSpace` would take.
    '''
    def __init__(self, iterable_or_length, domain=None, n_elements=None,
                 fixed_map={}, degrees=None, is_combination=False,
                 slice_=None, perm_type=None):
        self.sequence = tuple(iterable_or_length) if \
            isinstance(iterable_or_length, collections.Iterable) else \
                                   sequence_tools.CuteRange(iterable_or_length)
        self.sequence_length = len(self.sequence)
        self._sequence_frozen_bag = \
                                 nifty_collections.FrozenBag(self.sequence)
        self.is_recurrent = len(set(self.sequence)) < len(self.sequence)
        self.n_elements = n_elements if n_elements is not None else \
                                                             len(self.sequence)
        self.domain = (domain or
              sequence_tools.CuteRange(self.sequence_length))[:self.n_elements]
        self.fixed_map = dict((key, value) for key, value in fixed_map.items()
                              if key in self.domain)
        self.degrees = \
                      degrees or sequence_tools.CuteRange(self.sequence_length)
        self.is_combination = is_combination
        
        self.is_degreed = (self.degrees !=
                                sequence_tools.CuteRange(self.sequence_length))
        
        self.slice_ = slice_
 
        if perm_type is None:
            self.perm_type = tuple
            self.is_typed = False
        else:
            self.perm_type = FruityTuple
            self.is_typed = True
        
        
        
    def __iter__(self):
        if (self.is_recurrent and self.is_combination):
            def make_iterator():
                crap = set()
                for item in itertools.imap(self.perm_type, self._iter()):
                    fc = nifty_collections.FrozenBag(item)
                    if fc in crap:
                        continue
                    else:
                        yield item
                        crap.add(fc)
            iterator = make_iterator()
        else:
            iterator = iter(itertools.imap(self.perm_type, self._iter()))
        if self.slice_:
            return itertools.islice(iterator, self.slice_.start,
                                    self.slice_.stop)
        else:
            return iterator
        
    def _iter(self):
        yielded_candidates = set()
        for candidate in itertools.permutations(self.sequence, self.n_elements):
            if candidate in yielded_candidates:
                continue
            if any(candidate[self.domain.index(key)] != value for
                                         key, value in self.fixed_map.items()):
                continue
            if self.is_combination:
                i = -1
                rule_out_because_of_bad_comb_order = False # Until challeneged.
                for item in candidate:
                    try:
                        i = self.sequence.index(item, i+1)
                    except ValueError:
                        rule_out_because_of_bad_comb_order = True
                if rule_out_because_of_bad_comb_order:
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
                            candidate[current_item]
                        )
                        
                    if current_item == starting_item:
                        n_cycles += 1
                        
                degree = self.sequence_length - n_cycles
                
                if degree not in self.degrees:
                    continue
                
            yielded_candidates.add(candidate)
            yield candidate
                


class FruityMixin(object): pass
class FruityPerm(FruityMixin, Perm): pass
class FruityComb(FruityMixin, Comb): pass
class FruityTuple(FruityMixin, tuple): pass

def _check_variation_selection(variation_selection, perm_space_type,
                               iterable_or_length_and_sequence, domain_to_cut,
                               n_elements, is_combination, purified_fixed_map,
                               degrees, slice_, perm_type):
    assert isinstance(variation_selection,
                      combi.perming.variations.VariationSelection)
    kwargs = {}
    
    iterable_or_length, sequence = iterable_or_length_and_sequence
    
    kwargs['iterable_or_length'] = iterable_or_length
    sequence_set = set(sequence)
    
    if domain_to_cut != NO_ARGUMENT:
        kwargs['domain'] = actual_domain = domain_to_cut[:len(sequence)]
    else:
        actual_domain = sequence_tools.CuteRange(len(sequence))
        
    if n_elements != NO_ARGUMENT:
        kwargs['n_elements'] = n_elements
    actual_n_elements = n_elements if (n_elements != NO_ARGUMENT) else 0
        
    if is_combination != NO_ARGUMENT:
        kwargs['is_combination'] = is_combination
        
    if purified_fixed_map != NO_ARGUMENT:
        kwargs['fixed_map'] = actual_fixed_map = dict(
            (actual_domain[key], sequence[value]) for key, value
                           in purified_fixed_map.items() if key < len(sequence)
        )
    else:
        actual_fixed_map = {}
        
    if variation_selection.is_degreed:
        kwargs['degrees'] = degrees = (0, 2, 4, 5)
        
    if perm_type != NO_ARGUMENT:
        kwargs['perm_type'] = perm_type

    try:
        perm_space = perm_space_type(**kwargs)
    except (combi.UnallowedVariationSelectionException, TypeError):
        if not variation_selection.is_allowed:
            return
        else:
            raise
        
    if slice_ != NO_ARGUMENT:
        perm_space = perm_space[slice_]
        
    else:
        if not variation_selection.is_allowed:
            raise TypeError(
                "Shouldn't have allowed this `VariationSelection.`"
            )
    
    brute_perm_space = BrutePermSpace(
        slice_=(perm_space.canonical_slice if variation_selection.is_sliced else
                None), 
        **kwargs
    )
    assert perm_space.variation_selection == variation_selection
    assert perm_space.sequence_length == len(sequence)
    
    assert (perm_space.domain == perm_space.sequence) == (
        not variation_selection.is_dapplied and
        not variation_selection.is_rapplied and
        not variation_selection.is_partial
    )
    
    if perm_space.length:
        assert perm_space.index(perm_space[-1]) == perm_space.length - 1
        assert perm_space.index(perm_space[0]) == 0
        
    if variation_selection.is_partial:
        assert 0 < perm_space.n_unused_elements == \
                                              len(sequence) - actual_n_elements
    else:
        assert perm_space.n_unused_elements == 0
        
    assert perm_space == PermSpace(**kwargs)[perm_space.canonical_slice]
    assert (not perm_space != PermSpace(**kwargs)[perm_space.canonical_slice])
    assert hash(perm_space) == \
                          hash(PermSpace(**kwargs)[perm_space.canonical_slice])
    
    typed_perm_space = perm_space.get_typed(FruityComb if
                            variation_selection.is_combination else FruityPerm)
    assert typed_perm_space.is_typed
    assert variation_selection.is_typed is perm_space.is_typed is \
         (perm_space != perm_space.untyped) is (perm_space == typed_perm_space)
    

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
    
    for i, (perm, brute_perm_tuple) in enumerate(
           itertools.islice(itertools.izip(perm_space, brute_perm_space), 10)):
        
        assert tuple(perm) == brute_perm_tuple
        assert perm in perm_space
        assert tuple(perm) in perm_space
        assert iter(list(perm)) in perm_space
        assert set(perm) not in perm_space
        
        assert isinstance(perm, combi.Perm)
        assert perm.is_rapplied == variation_selection.is_rapplied
        assert perm.is_dapplied == variation_selection.is_dapplied
        assert perm.is_partial == variation_selection.is_partial
        assert perm.is_combination == variation_selection.is_combination
        assert perm.is_pure == (not (variation_selection.is_rapplied or
                                     variation_selection.is_dapplied or
                                     variation_selection.is_partial or
                                     variation_selection.is_combination))
        
        assert isinstance(perm, FruityMixin) is variation_selection.is_typed
        
        if variation_selection.is_rapplied:
            assert perm != perm.unrapplied
            if not variation_selection.is_recurrent:
                perm.unrapplied == perm_space.unrapplied[i]
        else:
            assert perm == perm.unrapplied == perm_space.unrapplied[i]
            if not variation_selection.is_dapplied:
                sample_domain = \
                               'qwertyasdfgzxcvbyuiophjkl;nm,.'[:len(sequence)]
                assert perm.apply(sample_domain) == sample_domain * perm
                assert tuple(sample_domain * perm) == tuple(
                    perm_space.get_rapplied(sample_domain)[i]._perm_sequence
                )
            
        
        if variation_selection.is_dapplied:
            assert perm != perm.undapplied == perm_space.undapplied[i]
        else:
            assert perm == perm.undapplied == perm_space.undapplied[i]
            
        if variation_selection.is_combination:
            if variation_selection.is_typed:
                with cute_testing.RaiseAssertor(TypeError):
                    perm.uncombinationed
            else:
                assert perm != perm.uncombinationed
        else:
            assert perm == perm.uncombinationed
        
        if variation_selection.is_combination:
            if variation_selection.is_typed:
                assert type(perm) == FruityComb
            else:
                assert type(perm) == Comb
        else:
            if variation_selection.is_typed:
                assert type(perm) == FruityPerm
            else:
                assert type(perm) == Perm
        
        if variation_selection.variations <= set((
            perming.variations.Variation.DAPPLIED,
            perming.variations.Variation.RAPPLIED,
            perming.variations.Variation.COMBINATION)):
            assert perm.nominal_perm_space == perm_space
        assert perm.nominal_perm_space == \
                                   perm_space._nominal_perm_space_of_perms == \
                                          perm_space.unsliced.undegreed.unfixed
        # Give me your unsliced, your undegreed, your unfixed.
        
        if not variation_selection.is_fixed and \
                                            not variation_selection.is_degreed:
            assert perm_space.index(perm) == i
            
        assert type(perm)(iter(perm), perm_space=perm_space) == perm
        assert type(perm)(perm._perm_sequence, perm_space=perm_space) == perm
        
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
            assert len(perm) == actual_n_elements
            if variation_selection.is_recurrent:
                assert perm_set <= sequence_set
            else:
                assert perm_set < sequence_set
                assert len(perm_set) == actual_n_elements
        else:
            assert perm_set == sequence_set
            assert len(perm) == len(sequence)
            
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
            assert perm.degree == degrees or perm.degree in degrees
        elif variation_selection.is_partial:
            assert perm.degree == NotImplemented
        else:
            assert 0 <= perm.degree <= len(sequence)
            
        
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
                if perm_space.length >= 5:
                    # (Guarding against cases of really small spaces where
                    # there aren't any neighbors.)
                    assert neighbors
                for neigbhor in itertools.islice(neighbors, 0, 10):
                    assert neigbhor in perm_space 
                    assert len(cute_iter_tools.zip_non_equal((perm, neigbhor),
                                                         lazy_tuple=True)) == 2
        
        #                                                                     #
        ### Finished testing neighbors. #######################################
        
        perm_repr = repr(perm)
        
        
def _iterate_tests():
    for variation_selection in \
                            combi.perming.variations.variation_selection_space:
        
        kwargs = {}
        
        if variation_selection.is_recurrent and \
                                           not variation_selection.is_rapplied:
            assert not variation_selection.is_allowed
            # Can't even test this illogical clash.
            continue
            
        
        if variation_selection.is_recurrent:
            iterable_or_length_and_sequence_options = (
                ('abracab', 'abracab'),
                ((1, 2, 3, 4, 5, 5, 4, 3),
                 (1, 2, 3, 4, 5, 5, 4, 3))
            )
        elif variation_selection.is_rapplied:
            iterable_or_length_and_sequence_options = (
                ([1, 4, 2, 5, 3, 7],
                 (1, 4, 2, 5, 3, 7)), 
            )
        else:
            iterable_or_length_and_sequence_options = (
                (7, sequence_tools.CuteRange(7)),
                (sequence_tools.CuteRange(9), sequence_tools.CuteRange(9))
            )
        
        if variation_selection.is_dapplied:
            domain_to_cut_options = (
                'QPONMLKJIHGFEDCBAZYXWVUTSR',
                [7 + i ** 2 for i in range(20)]
            )
        else:
            domain_to_cut_options = (NO_ARGUMENT,)
            
        if variation_selection.is_partial:
            n_elements_options = (1, 2, 5)
        else:
            n_elements_options = (NO_ARGUMENT,)
            
        perm_space_type_options = (PermSpace,)
        if variation_selection.is_combination:
            is_combination_options = (True,)
        else:
            is_combination_options = (NO_ARGUMENT,)
            
            
        if variation_selection.is_fixed:
            # All fixed maps have key `0` so even if `n_elements=1` the space
            # will still be fixed.
            purified_fixed_map_options = (
                {0: 1, 4: 3,},
                {0: 0, 1: -2, -2: -3,},
            )
        else:
            purified_fixed_map_options = (NO_ARGUMENT,)
            
        if variation_selection.is_degreed:
            degrees_options = (
                (0, 2, 4, 5),
                1,
            )
        else:
            degrees_options = (NO_ARGUMENT,)
            
        if variation_selection.is_sliced:
            slice_options = (
                slice(2, -2),
                slice(3, 4)
            )
        else:
            slice_options = (NO_ARGUMENT,)
            
            
        if variation_selection.is_typed:
            if variation_selection.is_combination:
                perm_type_options = (FruityComb,)
            else:
                perm_type_options = (FruityPerm,)
        else:
            perm_type_options = (NO_ARGUMENT,)
            
        product_space_ = combi.ProductSpace(
            ((variation_selection,), perm_space_type_options,
             iterable_or_length_and_sequence_options, domain_to_cut_options,
             n_elements_options, is_combination_options,
             purified_fixed_map_options, degrees_options, slice_options,
             perm_type_options)
        )
        
        for i in range(len(product_space_)):
            fucking_globals = dict(globals())
            fucking_globals.update(locals())
            yield eval(
                'lambda: _check_variation_selection(*product_space_[%s])' % i,
                fucking_globals, locals()
            )
            

# We use this shit because Nose can't parallelize generator tests:
lambdas = []
for i, f in enumerate(_iterate_tests()):
    f.name = 'f_%s' % i
    locals()[f.name] = f
    lambdas.append(f)
for i, partition in enumerate(sequence_tools.partitions(lambdas, 500)):
    exec('def test_%s(): return (%s)' %
         (i, ', '.join('%s()'% f.name for f in partition)))
    
    