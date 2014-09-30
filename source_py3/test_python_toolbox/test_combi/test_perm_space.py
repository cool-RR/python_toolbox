# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

import pickle
import itertools

from python_toolbox import sequence_tools

from python_toolbox import combi
from python_toolbox.combi import *

infinity = float('inf')
infinities = (infinity, -infinity)


def test_perm_spaces():
    pure_0a = PermSpace(4)
    pure_0b = PermSpace(range(4))
    pure_0c = PermSpace(list(range(4)))
    pure_0d = PermSpace(iter(range(4)))
    assert pure_0a == pure_0b == pure_0c == pure_0d
    assert len(pure_0a) == len(pure_0b) == len(pure_0c) == len(pure_0d)
    assert repr(pure_0a) == repr(pure_0b) == repr(pure_0c) == \
                         repr(pure_0d) == '<PermSpace: CuteRange(0, 4)>'
    
    assert cute_iter_tools.are_equal(pure_0a, pure_0b, pure_0c, pure_0d)
    
    assert set(map(bool, (pure_0a, pure_0b, pure_0c, pure_0d))) == {True}
    
    pure_perm_space = pure_0a
    assert pure_0a.is_pure
    assert not pure_0a.is_rapplied
    assert not pure_0a.is_dapplied
    assert not pure_0a.is_fixed
    assert not pure_0a.is_sliced
    
    first_perm = pure_0a[0]
    some_perm = pure_0a[7]
    last_perm = pure_0a[-1]
    
    assert first_perm.index(2) == 2
    assert first_perm.index(0) == 0
    with cute_testing.RaiseAssertor(ValueError): first_perm.index(5)
    
    assert last_perm.apply('meow') == 'woem'
    assert last_perm.apply('meow', str) == 'woem'
    assert last_perm.apply('meow', tuple) == tuple('woem')
    
    with cute_testing.RaiseAssertor(IndexError): pure_0a[- pure_0a.length - 1]
    with cute_testing.RaiseAssertor(IndexError): pure_0a[- pure_0a.length - 2]
    with cute_testing.RaiseAssertor(IndexError): pure_0a[- pure_0a.length - 30]
    with cute_testing.RaiseAssertor(IndexError): pure_0a[pure_0a.length]
    with cute_testing.RaiseAssertor(IndexError): pure_0a[pure_0a.length + 1]
    with cute_testing.RaiseAssertor(IndexError): pure_0a[pure_0a.length + 2]
    with cute_testing.RaiseAssertor(IndexError): pure_0a[pure_0a.length + 300]
    
    with cute_testing.RaiseAssertor(): pure_0a[24]
    
    assert pure_0a.take_random() in pure_0c
    
    
    # Testing hashing: 
    pure_perm_space_dict = {pure_0a: 'a', pure_0b: 'b',
                            pure_0c: 'c', pure_0d: 'd',}
    assert len(pure_perm_space_dict) == 1 # They're all the same
    assert pure_perm_space_dict[pure_0a] == pure_perm_space_dict[pure_0b] == \
          pure_perm_space_dict[pure_0c] == pure_perm_space_dict[pure_0d] == 'd'
    
    assert None not in pure_0a # Because, damn.
    assert PermSpace('meow')[0] not in pure_0a
    
    assert type(first_perm) == type(some_perm) == type(last_perm) == Perm
    assert set(some_perm) == set(range(4))
    assert tuple(first_perm) == (0, 1, 2, 3)
    assert tuple(last_perm) == (3, 2, 1, 0)
    assert Perm.coerce(first_perm) == first_perm
    assert Perm.coerce(first_perm, pure_0b) == first_perm
    assert Perm.coerce(tuple(first_perm)) == first_perm
    assert Perm.coerce(list(first_perm)) == first_perm
    assert Perm.coerce(tuple(first_perm), pure_0a) == first_perm
    assert Perm.coerce(list(first_perm), pure_0b) == first_perm
    assert Perm.coerce(tuple(first_perm), PermSpace(5, n_elements=4)) != \
                                                                     first_perm
    
    
    assert isinstance(first_perm.items, combi.perm.PermItems)
    assert first_perm.items[2] == (2, 2)
    assert repr(first_perm.items) == '<PermItems: %s>' % repr(first_perm)
    assert isinstance(first_perm.as_dictoid, combi.perm.PermAsDictoid)
    assert first_perm.as_dictoid[2] == 2
    assert dict(first_perm.as_dictoid) == {0: 0, 1: 1, 2: 2, 3: 3}
    assert not (first_perm != first_perm)
    assert first_perm == first_perm
    assert first_perm
    assert {pure_0a[4]: 1, pure_0b[4]: 2, pure_0c[4]: 3,} == {pure_0d[4]: 3,}
    
    
    assert some_perm.inverse == ~ some_perm
    assert ~ ~ some_perm == some_perm
    
    
    assert first_perm in pure_perm_space
    assert set(first_perm) not in pure_perm_space # No order? Not contained.
    assert some_perm in pure_perm_space
    assert last_perm in pure_perm_space
    assert tuple(first_perm) in pure_perm_space
    assert list(some_perm) in pure_perm_space
    assert iter(last_perm) in pure_perm_space
    assert 'meow' not in pure_perm_space
    assert (0, 1, 2, 3, 3) not in pure_perm_space
    
    assert pure_perm_space.index(first_perm) == 0
    assert pure_perm_space.index(last_perm) == \
                                                len(pure_perm_space) - 1
    assert pure_perm_space.index(some_perm) == 7
    
    assert 'meow' * Perm((1, 3, 2, 0)) == 'ewom'
    assert Perm('meow', 'meow') * Perm((1, 3, 2, 0)) == Perm('ewom', 'meow')
    assert [0, 1, 2, 3] * Perm((0, 1, 2, 3)) == (0, 1, 2, 3)
    assert Perm((0, 1, 2, 3)) * Perm((0, 1, 2, 3)) == Perm((0, 1, 2, 3))
    assert Perm((2, 0, 1, 3)) * Perm((0, 1, 3, 2)) == Perm((2, 0, 3, 1))
    
    assert (Perm((0, 1, 2, 3)) ** (- 2)) == (Perm((0, 1, 2, 3)) ** (- 1)) == \
           (Perm((0, 1, 2, 3)) ** (0)) == (Perm((0, 1, 2, 3)) ** (1)) == \
           (Perm((0, 1, 2, 3)) ** 2) == (Perm((0, 1, 2, 3)) ** 3)
    
    assert set(map(bool, (pure_0a[4:4], pure_0a[3:2]))) == {False}
    assert pure_0a[2:6][1:-1] == pure_0a[3:5]
    assert tuple(pure_0a[2:6][1:-1]) == tuple(pure_0a[3:5])
    assert pure_0a[2:6][1:-1][1] == pure_0a[3:5][1]
    assert pure_0a[2:5][1:-1] != pure_0a[3:5]
    
    big_perm_space = PermSpace(range(150), fixed_map={1: 5, 70: 3,},
                               degrees=(3, 5))
    
    assert big_perm_space == PermSpace(range(150),
                                       fixed_map={1: 5, 70: 3,}.items(),
                                       degrees=(3, 5))
    
    for i in [10**10, 3*11**9-344, 4*12**8-5, 5*3**20+4]:
        perm = big_perm_space[i]
        assert big_perm_space.index(perm) == i
        
    repr_of_big_perm_space = repr(PermSpace(tuple(range(100, 0, -1))))
    assert '...' in repr_of_big_perm_space
    assert len(repr_of_big_perm_space) <= 100
    
    fixed_perm_space = pure_perm_space.get_fixed({0: 3,})
    assert fixed_perm_space.length == 6
    assert fixed_perm_space.is_fixed
    assert not fixed_perm_space.is_pure
    assert fixed_perm_space.unfixed.is_pure
    assert fixed_perm_space.unfixed == pure_perm_space
    
    assert pickle.loads(pickle.dumps(pure_perm_space)) == pure_perm_space
    assert pickle.loads(pickle.dumps(pure_0b[2])) == pure_0c[2]
    assert pickle.loads(pickle.dumps(pure_0b[3])) != pure_0b[4]
    
    
def test_fixed_perm_space():
    pure_perm_space = PermSpace(5)
    small_fixed_perm_space = PermSpace(5, fixed_map={0: 0, 2: 2, 4: 4,})
    big_fixed_perm_space = PermSpace(5, fixed_map={0: 0, 2: 2,})
    
    assert pure_perm_space != big_fixed_perm_space != small_fixed_perm_space
    assert small_fixed_perm_space.length == \
                                        len(tuple(small_fixed_perm_space)) == 2
    assert big_fixed_perm_space.length == \
                                          len(tuple(big_fixed_perm_space)) == 6
    
    for perm in small_fixed_perm_space:
        assert perm in big_fixed_perm_space
        assert perm in pure_perm_space
        
    for perm in big_fixed_perm_space:
        assert perm in pure_perm_space
        
    assert len([perm for perm in big_fixed_perm_space if perm
                not in small_fixed_perm_space]) == 4
    
    assert small_fixed_perm_space[:] == small_fixed_perm_space
    assert small_fixed_perm_space[1:][0] == small_fixed_perm_space[1]
    
    assert small_fixed_perm_space.index(small_fixed_perm_space[0]) == 0
    assert small_fixed_perm_space.index(small_fixed_perm_space[1]) == 1
    
    assert big_fixed_perm_space.index(big_fixed_perm_space[0]) == 0
    assert big_fixed_perm_space.index(big_fixed_perm_space[1]) == 1
    assert big_fixed_perm_space.index(big_fixed_perm_space[2]) == 2
    assert big_fixed_perm_space.index(big_fixed_perm_space[3]) == 3
    assert big_fixed_perm_space.index(big_fixed_perm_space[4]) == 4
    assert big_fixed_perm_space.index(big_fixed_perm_space[5]) == 5
    
    for perm in small_fixed_perm_space:
        assert (perm[0], perm[2], perm[4]) == (0, 2, 4)
    
    for perm in big_fixed_perm_space:
        assert (perm[0], perm[2]) == (0, 2)
    
    assert big_fixed_perm_space.index(small_fixed_perm_space[1]) != 1
    
    
def test_rapplied_perm_space():
    rapplied_perm_space = PermSpace('meow')
    assert rapplied_perm_space.is_rapplied
    assert not rapplied_perm_space.is_fixed
    assert not rapplied_perm_space.is_sliced
    
    assert 'mowe' in rapplied_perm_space
    assert 'woof' not in rapplied_perm_space
    assert rapplied_perm_space.unrapplied[0] not in rapplied_perm_space
    assert rapplied_perm_space[rapplied_perm_space.index('wome')] == \
                                              Perm('wome', rapplied_perm_space)
    
    rapplied_perm = rapplied_perm_space[3]
    assert isinstance(reversed(rapplied_perm), Perm)
    assert tuple(reversed(rapplied_perm)) == \
                                          tuple(reversed(tuple(rapplied_perm)))
    assert reversed(reversed(rapplied_perm)) == rapplied_perm
    
def test_dapplied_perm_space():
    dapplied_perm_space = PermSpace(5, domain='growl')
    assert dapplied_perm_space.is_dapplied
    assert not dapplied_perm_space.is_rapplied
    assert not dapplied_perm_space.is_fixed
    assert not dapplied_perm_space.is_sliced
    
    assert (0, 4, 2, 3, 1) in dapplied_perm_space
    assert (0, 4, 'ooga booga', 2, 3, 1) not in dapplied_perm_space
    assert dapplied_perm_space.get_partialled(3)[2] not in dapplied_perm_space
    
    assert dapplied_perm_space.undapplied[7] not in dapplied_perm_space
    
    dapplied_perm = dapplied_perm_space[-1]
    assert dapplied_perm in dapplied_perm_space
    assert isinstance(reversed(dapplied_perm), Perm)
    assert reversed(dapplied_perm) in dapplied_perm_space
    assert tuple(reversed(dapplied_perm)) == \
                                          tuple(reversed(tuple(dapplied_perm)))
    assert reversed(reversed(dapplied_perm)) == dapplied_perm
    
    assert dapplied_perm['l'] == 0
    assert dapplied_perm['w'] == 1
    assert dapplied_perm['o'] == 2
    assert dapplied_perm['r'] == 3
    assert dapplied_perm['g'] == 4
    assert repr(dapplied_perm) == \
         '''<Perm: (119 / 120) ('g', 'r', 'o', 'w', 'l') => (4, 3, 2, 1, 0)>'''
    
    assert dapplied_perm.index(4) == 'g'
    
    assert dapplied_perm.as_dictoid['g'] == 4
    assert dapplied_perm.items[0] == ('g', 4)
    
    
    # `__contains__` works on the values, not the keys:
    for char in 'growl':
        assert char not in dapplied_perm
    for number in range(5):
        assert number in dapplied_perm
        
    assert not dapplied_perm_space._just_fixed.is_fixed
    assert not dapplied_perm_space._just_fixed.is_dapplied
    assert not dapplied_perm_space._just_fixed.is_rapplied
    assert not dapplied_perm_space._just_fixed.is_partial
    assert not dapplied_perm_space._just_fixed.is_combination
    assert not dapplied_perm_space._just_fixed.is_degreed
    
    assert repr(dapplied_perm_space) == \
                                      "<PermSpace: 'growl' => CuteRange(0, 5)>"
    
    # Testing `repr` shortening: 
    assert repr(PermSpace(20, domain=tuple(range(20, 0, -1)))) == (
        '<PermSpace: (20, 19, 18, 17, 16, 15, 14, 13, 12 ... ) => '
        'CuteRange(0, 20)>'
    )
    
def test_degreed_perm_space():
    assert PermSpace(3, degrees=0).length == 1
    assert PermSpace(3, degrees=1).length == 3
    assert PermSpace(3, degrees=2).length == 2
    
    for perm in PermSpace(3, degrees=1):
        assert perm.degree == 1
        
        
    perm_space = PermSpace(5, degrees=(1, 3))
    for perm in perm_space:
        assert perm.degree in (1, 3)
        
    assert cute_iter_tools.is_sorted(
        [perm_space.index(perm) for perm in perm_space]
    )
    
    assert PermSpace(
        7, 'travels',
        fixed_map={'l': 5, 'a': 2, 't': 0, 'v': 3, 'r': 1, 'e': 6},
        degrees=(1, 3, 5)
    ).length == 1
    
    assert PermSpace(4, degrees=1, fixed_map={0: 0, 1: 1, 2: 2,}).length == 0
    assert PermSpace(4, degrees=1, fixed_map={0: 0, 1: 1}).length == 1
    assert PermSpace(4, degrees=1, fixed_map={0: 0, }).length == 3
    assert PermSpace(4, degrees=1, fixed_map={0: 1, 1: 0,}).length == 1
    assert PermSpace(4, degrees=1, fixed_map={0: 1, 1: 2,}).length == 0
    assert PermSpace(4, degrees=2, fixed_map={0: 1, 1: 2,}).length == 1
    assert PermSpace(4, degrees=3, fixed_map={0: 1, 1: 2,}).length == 1
    
    assert PermSpace(4, degrees=3, fixed_map={2: 3,}).length == 2
    assert PermSpace(4, degrees=1, fixed_map={2: 3,}).length == 1
    
    funky_perm_space = PermSpace('isogram', domain='travels',
                                 degrees=(1, 3, 5, 9),
                                 fixed_map={'t': 'i', 'v': 'g',})[2:-2]
    assert funky_perm_space.purified == PermSpace(7)
    
    assert funky_perm_space.is_rapplied
    assert funky_perm_space.is_dapplied
    assert funky_perm_space.is_degreed
    assert funky_perm_space.is_fixed
    assert funky_perm_space.is_sliced
    assert not funky_perm_space.is_pure
    
    assert funky_perm_space.degrees == (1, 3, 5)
    assert funky_perm_space.sequence == 'isogram'
    assert funky_perm_space.domain == 'travels'
    assert funky_perm_space.canonical_slice.start == 2
    
    assert funky_perm_space.unsliced.undegreed.get_degreed(2)[0] \
                                                        not in funky_perm_space
    assert funky_perm_space.unsliced.get_fixed({'t': 'i', 'v': 'g',}) \
                                  [funky_perm_space.slice_] == funky_perm_space
    
    for i, perm in enumerate(funky_perm_space):
        assert perm.is_dapplied
        assert perm.is_rapplied
        assert perm['t'] == 'i'
        assert perm['v'] == 'g'
        assert perm['s'] in 'isogram'
        assert 1 not in perm
        assert perm.degree in (1, 3, 5, 9)
        assert funky_perm_space.index(perm) == i
        assert perm.undapplied[0] == 'i'
        assert perm.unrapplied['t'] == 0
        assert perm.unrapplied.undapplied[0] == 0
        assert perm.undapplied.is_rapplied
        assert perm.unrapplied.is_dapplied
        
    assert cute_iter_tools.is_sorted(
        [funky_perm_space.index(perm) for perm in funky_perm_space]
    )
    
    assert cute_iter_tools.is_sorted(funky_perm_space)
    
    
    other_perms_chain_space = ChainSpace((funky_perm_space.unsliced[:2],
                                          funky_perm_space.unsliced[-2:]))
    for perm in other_perms_chain_space:
        assert perm.is_dapplied
        assert perm.is_rapplied
        assert perm['t'] == 'i'
        assert perm['v'] == 'g'
        assert perm['s'] in 'isogram'
        assert 1 not in perm
        assert perm.degree in (1, 3, 5, 9)
        assert perm not in funky_perm_space
        assert perm.unrapplied['t'] == 0
        assert perm.unrapplied.undapplied[0] == 0        
        assert perm.undapplied.is_rapplied
        assert perm.unrapplied.is_dapplied
        
    assert other_perms_chain_space.length + funky_perm_space.length == \
                                               funky_perm_space.unsliced.length
    
    assert funky_perm_space.unsliced.length + \
           funky_perm_space.unsliced.undegreed.get_degreed(
               i for i in range(funky_perm_space.sequence_length)
               if i not in funky_perm_space.degrees
            ).length == funky_perm_space.unsliced.undegreed.length
    
    assert funky_perm_space._just_fixed.is_fixed
    assert not funky_perm_space._just_fixed.is_rapplied
    assert not funky_perm_space._just_fixed.is_dapplied
    assert not funky_perm_space._just_fixed.is_sliced
    assert not funky_perm_space._just_fixed.is_degreed
    
    assert pickle.loads(pickle.dumps(funky_perm_space)) == funky_perm_space
    assert funky_perm_space != \
             pickle.loads(pickle.dumps(funky_perm_space.unsliced.unfixed)) == \
                                              funky_perm_space.unsliced.unfixed
    
    
    
def test_partial_perm_space():
    with cute_testing.RaiseAssertor():
        PermSpace(5, n_elements=6)
        
    perm_space_0 = PermSpace(5, n_elements=5)
    perm_space_1 = PermSpace(5, n_elements=3)
    perm_space_2 = PermSpace(5, n_elements=2)
    perm_space_3 = PermSpace(5, n_elements=1)
    perm_space_4 = PermSpace(5, n_elements=0)
        
    perm_space_5 = PermSpace(5, n_elements=5, is_combination=True)
    perm_space_6 = PermSpace(5, n_elements=3, is_combination=True)
    perm_space_7 = PermSpace(5, n_elements=2, is_combination=True)
    perm_space_8 = PermSpace(5, n_elements=1, is_combination=True)
    perm_space_9 = PermSpace(5, n_elements=0, is_combination=True)
    
    assert not perm_space_0.is_partial and not perm_space_0.is_combination
    assert perm_space_1.is_partial and not perm_space_1.is_combination
    assert perm_space_2.is_partial and not perm_space_2.is_combination
    assert perm_space_3.is_partial and not perm_space_3.is_combination
    assert perm_space_4.is_partial and not perm_space_4.is_combination
    assert set(map(type, (perm_space_0, perm_space_1, perm_space_2,
                          perm_space_3, perm_space_4))) == {PermSpace}
    
    assert not perm_space_5.is_partial and perm_space_5.is_combination
    assert perm_space_6.is_partial and perm_space_6.is_combination
    assert perm_space_7.is_partial and perm_space_7.is_combination
    assert perm_space_8.is_partial and perm_space_8.is_combination
    assert perm_space_9.is_partial and perm_space_9.is_combination
    assert set(map(type, (perm_space_5, perm_space_6, perm_space_7,
                          perm_space_8, perm_space_9))) == {CombSpace}
    
    assert CombSpace(5, n_elements=2) == perm_space_7
    
    assert perm_space_0.length == math.factorial(5)
    assert perm_space_1.length == 5 * 4 * 3
    assert perm_space_2.length == 5 * 4
    assert perm_space_3.length == 5
    assert perm_space_4.length == 1
    
    assert perm_space_5.length == 1
    assert perm_space_6.length == perm_space_7.length == 5 * 4 / 2
    assert perm_space_8.length == 5
    assert perm_space_9.length == 1
    
    assert set(map(tuple, perm_space_1)) > set(map(tuple, perm_space_6))
    
    for i, perm in enumerate(perm_space_2):
        assert len(perm) == 2
        assert not perm.is_dapplied
        assert not perm.is_rapplied
        assert not isinstance(perm, Comb)
        assert perm_space_2.index(perm) == i
        reconstructed_perm = Perm(tuple(perm), perm_space=perm_space_2)
        assert perm == reconstructed_perm
        
    
    for i, perm in enumerate(perm_space_7):
        assert len(perm) == 2
        assert not perm.is_dapplied
        assert not perm.is_rapplied
        assert isinstance(perm, Comb)
        assert perm_space_7.index(perm) == i
        assert perm[0] < perm[1]
        reconstructed_perm = Perm(tuple(perm), perm_space=perm_space_7)
        assert perm == reconstructed_perm
        
    assert cute_iter_tools.is_sorted(
        [perm_space_2.index(perm) for perm in perm_space_2]
    )
    assert cute_iter_tools.is_sorted(
        [tuple(perm) for perm in perm_space_2]
    )
    assert cute_iter_tools.is_sorted(
        [perm_space_7.index(perm) for perm in perm_space_7]
    )
    assert cute_iter_tools.is_sorted(
        [tuple(perm) for perm in perm_space_7]
    )
    
    
def test_neighbors():
    perm = Perm('wome', 'meow')
    first_level_neighbors = perm.get_neighbors()
    assert Perm('woem', 'meow') in first_level_neighbors
    assert Perm('meow', 'meow') not in first_level_neighbors
    assert len(first_level_neighbors) == 6
    assert isinstance(first_level_neighbors[0], Perm)
    
    
    
    first_and_second_level_neighbors = perm.get_neighbors(degrees=(1, 2))
    assert Perm('woem', 'meow') in first_and_second_level_neighbors
    assert Perm('meow', 'meow') not in first_and_second_level_neighbors
    assert Perm('owem', 'meow') in first_and_second_level_neighbors
    assert isinstance(first_and_second_level_neighbors[-1], Perm)
    
    
    assert set(first_level_neighbors) < set(first_and_second_level_neighbors)
    
    assert perm in perm.get_neighbors(degrees=(0, 1))
    assert set(first_level_neighbors) < set(perm.get_neighbors(degrees=(0, 1)))
    assert len(first_level_neighbors) + 1 == \
                                        len(perm.get_neighbors(degrees=(0, 1)))
    
    
def test_recurrent():
    recurrent_perm_space = PermSpace('abbccddd', n_elements=3)
    assert recurrent_perm_space.is_recurrent
    assert recurrent_perm_space.is_partial
    assert recurrent_perm_space.length == 52
    assert recurrent_perm_space.combinationed.length == 14
    
    assert recurrent_perm_space.get_fixed({1: 'b',}).length == 14
    
    # blocktodo: Don't forget getitem and index tests of course... 