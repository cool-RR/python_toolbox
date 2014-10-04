# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `python_toolbox.nifty_collections.LazyTuple`.'''

import uuid
import re
import pickle
import itertools
import collections
import decimal as decimal_module

from python_toolbox import cute_iter_tools
from python_toolbox import sequence_tools
from python_toolbox import cute_testing


from python_toolbox.nifty_collections import (FrozenTally,
                                              FrozenOrderedTally,
                                              OrderedDict)

infinity = float('inf')
infinities = (infinity, -infinity)


def test_common():
    _check_common(FrozenTally)
    _check_common(FrozenOrderedTally)
    _check_comparison(FrozenTally)
    _check_comparison(FrozenOrderedTally)
    _check_ignores_zero(FrozenTally)
    _check_ignores_zero(FrozenOrderedTally)
    _check_immutable(FrozenTally)
    _check_immutable(FrozenOrderedTally)
    _check_only_positive_ints_or_zero(FrozenTally)
    _check_only_positive_ints_or_zero(FrozenOrderedTally)
    

def _check_common(frozen_tally_type):
    frozen_tally = frozen_tally_type('abracadabra')
    assert frozen_tally == collections.Counter('abracadabra') == \
           collections.Counter(frozen_tally) == \
           frozen_tally_type(collections.Counter('abracadabra'))
    
    assert len(frozen_tally) == 5
    assert set(frozen_tally) == set(frozen_tally.keys()) == set('abracadabra')
    assert set(frozen_tally.values()) == {1, 2, 5}
    assert set(frozen_tally.items()) == \
                             {('a', 5), ('r', 2), ('b', 2), ('c', 1), ('d', 1)}
    assert frozen_tally['a'] == 5
    assert frozen_tally['missing value'] == 0
    assert len(frozen_tally) == 5
    assert {frozen_tally, frozen_tally} == {frozen_tally}
    assert {frozen_tally: frozen_tally} == {frozen_tally: frozen_tally}
    assert isinstance(hash(frozen_tally), int)
    
    assert set(frozen_tally.most_common()) == \
                         set(collections.Counter(frozen_tally).most_common())
    
    assert frozen_tally + frozen_tally == \
                                         frozen_tally_type('abracadabra' * 2)
    assert frozen_tally - frozen_tally == frozen_tally_type()
    assert frozen_tally - frozen_tally_type('a') == \
                                              frozen_tally_type('abracadabr')
    assert frozen_tally - frozen_tally_type('a') == \
                                              frozen_tally_type('abracadabr')
    assert frozen_tally | frozen_tally_type('a') == frozen_tally
    assert frozen_tally | frozen_tally == \
           frozen_tally | frozen_tally | frozen_tally == frozen_tally
    assert frozen_tally & frozen_tally_type('a') == frozen_tally_type('a')
    assert frozen_tally & frozen_tally == \
           frozen_tally & frozen_tally & frozen_tally == frozen_tally
    
    assert frozen_tally_type(frozen_tally.elements()) == frozen_tally
    
    assert +frozen_tally == frozen_tally
    with cute_testing.RaiseAssertor(TypeError):
        - frozen_tally
    
    assert re.match('^Frozen(Ordered)?Tally\(.*$',
                    repr(frozen_tally))
    
    assert frozen_tally.copy({'meow': 9}) == \
           frozen_tally.copy(meow=9) == \
           frozen_tally_type(OrderedDict(
               [('a', 5), ('b', 2), ('r', 2), ('c', 1), ('d', 1), ('meow', 9)])
           )
    
    assert pickle.loads(pickle.dumps(frozen_tally)) == frozen_tally
    
    assert frozen_tally_type({'a': 0, 'b': 1,}) == \
                                         frozen_tally_type({'c': 0, 'b': 1,})
    
def _check_comparison(frozen_tally_type):
    tally_0 = frozen_tally_type('c')
    tally_1 = frozen_tally_type('abc')
    tally_2 = frozen_tally_type('aabc')
    tally_3 = frozen_tally_type('abbc')
    tally_4 = frozen_tally_type('aabbcc')
    
    hierarchy = (
        (tally_4, {tally_3, tally_2, tally_1, tally_0}),
        (tally_3, {tally_1, tally_0}),
        (tally_2, {tally_1, tally_0}),
        (tally_1, {tally_0}),
        (tally_0, set()),
    )
    
    for item, smaller_items in hierarchy:
        if not isinstance(item, frozen_tally_type):
            continue
        for smaller_item in smaller_items:
            assert not item <= smaller_item
            assert not item < smaller_item
            assert item >= smaller_item
            assert item > smaller_item
            assert item != smaller_item
        not_smaller_items = [item for item in next(zip(*hierarchy)) if
                                                  item not in smaller_item]
        for not_smaller_item in not_smaller_items:
            assert not item < smaller_item

def _check_ignores_zero(frozen_tally_type):
    frozen_tally_0 = frozen_tally_type({'a': 0,})
    frozen_tally_1 = frozen_tally_type()
    assert frozen_tally_0 == frozen_tally_1
    
    assert hash(frozen_tally_0) == hash(frozen_tally_1)
    assert {frozen_tally_0, frozen_tally_1} == {frozen_tally_0} == \
                                                             {frozen_tally_1}
    
    frozen_tally_2 = frozen_tally_type(
                       {'a': 0.0, 'b': 2, 'c': decimal_module.Decimal('0.0'),})
    frozen_tally_3 = frozen_tally_type('bb')
    
    assert hash(frozen_tally_2) == hash(frozen_tally_3)
    assert {frozen_tally_2, frozen_tally_3} == {frozen_tally_2} == \
                                                             {frozen_tally_3}


def _check_immutable(frozen_tally_type):
    frozen_tally = frozen_tally_type('abracadabra')
    with cute_testing.RaiseAssertor(TypeError):
        frozen_tally['a'] += 1
    with cute_testing.RaiseAssertor(TypeError):
        frozen_tally['a'] -= 1
    with cute_testing.RaiseAssertor(TypeError):
        frozen_tally['a'] = 7
    

def _check_immutable(frozen_tally_type):
    frozen_tally = frozen_tally_type('abracadabra')
    with cute_testing.RaiseAssertor(TypeError):
        frozen_tally['a'] += 1
    with cute_testing.RaiseAssertor(TypeError):
        frozen_tally['a'] -= 1
    with cute_testing.RaiseAssertor(TypeError):
        frozen_tally['a'] = 7
    
def _check_only_positive_ints_or_zero(frozen_tally_type):
    assert frozen_tally_type(
        OrderedDict([('a', 0), ('b', 0.0), ('c', 1), ('d', 2.0),
                     ('e', decimal_module.Decimal('3.0'))])) == \
                                                          frozen_tally_type('cddeee')
    with cute_testing.RaiseAssertor(TypeError):
        frozen_tally_type({'a': 1.1,})
    with cute_testing.RaiseAssertor(TypeError):
        frozen_tally_type({'a': -2,})
    with cute_testing.RaiseAssertor(TypeError):
        frozen_tally_type({'a': -3,})
    with cute_testing.RaiseAssertor(TypeError):
        frozen_tally_type({'a': decimal_module.Decimal('-3'),})
    with cute_testing.RaiseAssertor(TypeError):
        frozen_tally_type({'a': infinity,})
    with cute_testing.RaiseAssertor(TypeError):
        frozen_tally_type({'a': -infinity,})
    with cute_testing.RaiseAssertor(TypeError):
        frozen_tally_type({'a': 'whatever',})
    with cute_testing.RaiseAssertor(TypeError):
        frozen_tally_type({'a': b'whateva',})
    with cute_testing.RaiseAssertor(TypeError):
        frozen_tally_type({'a': ('still', 'nope'),})
    
    
    
def test_ordered():
    frozen_tally_0 = FrozenTally('ababb')
    frozen_tally_1 = FrozenTally('bbbaa')
    assert frozen_tally_0 == frozen_tally_1
    assert hash(frozen_tally_0) == hash(frozen_tally_1)
    
    frozen_ordered_tally_0 = FrozenOrderedTally('ababb')
    frozen_ordered_tally_1 = FrozenOrderedTally('bbbaa')
    assert frozen_ordered_tally_0 == frozen_ordered_tally_0
    assert hash(frozen_ordered_tally_0) == hash(frozen_ordered_tally_0)
    assert frozen_ordered_tally_1 == frozen_ordered_tally_1
    assert hash(frozen_ordered_tally_1) == hash(frozen_ordered_tally_1)
    assert frozen_ordered_tally_0 != frozen_ordered_tally_1
    assert frozen_ordered_tally_0 <= frozen_ordered_tally_1
    assert frozen_ordered_tally_0 >= frozen_ordered_tally_1
    
def test_repr():
    assert re.match(
        "^FrozenTally\\({(?:(?:'b': 3, 'a': 2)|(?:'a': 2, 'b': 3))}\\)$", 
        repr(FrozenTally('ababb'))
    )
    assert repr(FrozenOrderedTally('ababb')) == \
                                     "FrozenOrderedTally([('a', 2), ('b', 3)])"
    
    
