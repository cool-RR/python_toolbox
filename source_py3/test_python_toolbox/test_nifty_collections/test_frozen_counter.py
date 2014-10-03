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


from python_toolbox.nifty_collections import (FrozenCounter,
                                              FrozenOrderedCounter,
                                              OrderedDict)

def test_common():
    _check_common(FrozenCounter)
    _check_common(FrozenOrderedCounter)
    _check_comparison(FrozenCounter)
    _check_comparison(FrozenOrderedCounter)
    _check_ignores_zero(FrozenCounter)
    _check_ignores_zero(FrozenOrderedCounter)
    _check_immutable(FrozenCounter)
    _check_immutable(FrozenOrderedCounter)
    

def _check_common(frozen_counter_type):
    frozen_counter = frozen_counter_type('abracadabra')
    assert frozen_counter == collections.Counter('abracadabra') == \
           collections.Counter(frozen_counter) == \
           frozen_counter_type(collections.Counter('abracadabra'))
    
    assert len(frozen_counter) == 5
    assert set(frozen_counter) == set(frozen_counter.keys()) == \
                                                             set('abracadabra')
    assert set(frozen_counter.values()) == {1, 2, 5}
    assert set(frozen_counter.items()) == \
                             {('a', 5), ('r', 2), ('b', 2), ('c', 1), ('d', 1)}
    assert frozen_counter['a'] == 5
    assert frozen_counter['missing value'] == 0
    assert len(frozen_counter) == 5
    assert {frozen_counter, frozen_counter} == {frozen_counter}
    assert {frozen_counter: frozen_counter} == {frozen_counter: frozen_counter}
    assert isinstance(hash(frozen_counter), int)
    
    assert set(frozen_counter.most_common()) == \
                         set(collections.Counter(frozen_counter).most_common())
    
    assert frozen_counter + frozen_counter == \
                                         frozen_counter_type('abracadabra' * 2)
    assert frozen_counter - frozen_counter == frozen_counter_type()
    assert frozen_counter - frozen_counter_type('a') == \
                                              frozen_counter_type('abracadabr')
    assert frozen_counter - frozen_counter_type('a') == \
                                              frozen_counter_type('abracadabr')
    assert frozen_counter | frozen_counter_type('a') == frozen_counter
    assert frozen_counter | frozen_counter == \
           frozen_counter | frozen_counter | frozen_counter == frozen_counter
    assert frozen_counter & frozen_counter_type('a') == frozen_counter_type('a')
    assert frozen_counter & frozen_counter == \
           frozen_counter & frozen_counter & frozen_counter == \
                                                                 frozen_counter
    
    assert frozen_counter_type(frozen_counter.elements()) == frozen_counter
    
    assert +frozen_counter == frozen_counter
    assert ---frozen_counter == -frozen_counter != \
                                             frozen_counter == --frozen_counter
    
    assert re.match('^Frozen(Ordered)?Counter\(.*$',
                    repr(frozen_counter))
    
    assert frozen_counter.copy({'meow': 9}) == \
           frozen_counter.copy(meow=9) == \
           frozen_counter_type(OrderedDict(
               [('a', 5), ('b', 2), ('r', 2), ('c', 1), ('d', 1), ('meow', 9)])
           )
    
    assert pickle.loads(pickle.dumps(frozen_counter)) == frozen_counter
    
def _check_comparison(frozen_counter_type):
    counter_0 = frozen_counter_type('c')
    counter_1 = frozen_counter_type('abc')
    counter_2 = frozen_counter_type('aabc')
    counter_3 = frozen_counter_type('abbc')
    counter_4 = frozen_counter_type('aabbcc')
    
    hierarchy = (
        (counter_4, {counter_3, counter_2, counter_1, counter_0}),
        (counter_3, {counter_1, counter_0}),
        (counter_2, {counter_1, counter_0}),
        (counter_1, {counter_0}),
        (counter_0, set()),
    )
    
    for item, smaller_items in hierarchy:
        if not isinstance(item, frozen_counter_type):
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

def _check_ignores_zero(frozen_counter_type):
    frozen_counter_0 = frozen_counter_type({'a': 0,})
    frozen_counter_1 = frozen_counter_type()
    assert frozen_counter_0 == frozen_counter_1
    
    assert hash(frozen_counter_0) == hash(frozen_counter_1)
    assert {frozen_counter_0, frozen_counter_1} == {frozen_counter_0} == \
                                                             {frozen_counter_1}
    
    frozen_counter_2 = frozen_counter_type(
                       {'a': 0.0, 'b': 2, 'c': decimal_module.Decimal('0.0'),})
    frozen_counter_3 = frozen_counter_type('bb')
    
    assert hash(frozen_counter_2) == hash(frozen_counter_3)
    assert {frozen_counter_2, frozen_counter_3} == {frozen_counter_2} == \
                                                             {frozen_counter_3}


def _check_immutable(frozen_counter_type):
    frozen_counter = frozen_counter_type('abracadabra')
    with cute_testing.RaiseAssertor(TypeError):
        frozen_counter['a'] += 1
    with cute_testing.RaiseAssertor(TypeError):
        frozen_counter['a'] -= 1
    with cute_testing.RaiseAssertor(TypeError):
        frozen_counter['a'] = 7
    

def _check_immutable(frozen_counter_type):
    frozen_counter = frozen_counter_type('abracadabra')
    with cute_testing.RaiseAssertor(TypeError):
        frozen_counter['a'] += 1
    with cute_testing.RaiseAssertor(TypeError):
        frozen_counter['a'] -= 1
    with cute_testing.RaiseAssertor(TypeError):
        frozen_counter['a'] = 7
    
def test_ordered():
    frozen_counter_0 = FrozenCounter('ababb')
    frozen_counter_1 = FrozenCounter('bbbaa')
    assert frozen_counter_0 == frozen_counter_1
    assert hash(frozen_counter_0) == hash(frozen_counter_1)
    
    frozen_ordered_counter_0 = FrozenOrderedCounter('ababb')
    frozen_ordered_counter_1 = FrozenOrderedCounter('bbbaa')
    assert frozen_ordered_counter_0 == frozen_ordered_counter_0
    assert hash(frozen_ordered_counter_0) == hash(frozen_ordered_counter_0)
    assert frozen_ordered_counter_1 == frozen_ordered_counter_1
    assert hash(frozen_ordered_counter_1) == hash(frozen_ordered_counter_1)
    assert frozen_ordered_counter_0 != frozen_ordered_counter_1
    assert frozen_ordered_counter_0 <= frozen_ordered_counter_1
    assert frozen_ordered_counter_0 >= frozen_ordered_counter_1
    
def test_repr():
    assert re.match(
        "^FrozenCounter\\({(?:(?:'b': 3, 'a': 2)|(?:'a': 2, 'b': 3))}\\)$", 
        repr(FrozenCounter('ababb'))
    )
    assert repr(FrozenOrderedCounter('ababb')) == \
                      "FrozenOrderedCounter(OrderedDict([('a', 2), ('b', 3)]))"
    
    