# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `python_toolbox.nifty_collections.LazyTuple`.'''

import uuid
import pickle
import itertools
import collections
import decimal as decimal_module

from python_toolbox import cute_iter_tools
from python_toolbox import sequence_tools
from python_toolbox import cute_testing


from python_toolbox.nifty_collections import FrozenCounter


def test():
    frozen_counter = FrozenCounter('abracadabra')
    assert frozen_counter == collections.Counter('abracadabra') == \
           collections.Counter(frozen_counter) == \
           FrozenCounter(collections.Counter('abracadabra'))
    
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
    
    assert frozen_counter.copy({'meow': 9}) == \
           frozen_counter.copy(meow=9) == \
           FrozenCounter({'a': 5, 'r': 2, 'b': 2, 'c': 1, 'd': 1,
                          'meow': 9,})
    
    assert set(frozen_counter.most_common()) == \
                         set(collections.Counter(frozen_counter).most_common())
    
    assert frozen_counter + frozen_counter == FrozenCounter('abracadabra'*2)
    assert frozen_counter - frozen_counter == FrozenCounter()
    assert frozen_counter - FrozenCounter('a') == FrozenCounter('abracadabr')
    assert frozen_counter - FrozenCounter('a') == FrozenCounter('abracadabr')
    assert frozen_counter | FrozenCounter('a') == frozen_counter
    assert frozen_counter | frozen_counter == \
           frozen_counter | frozen_counter | frozen_counter == \
                                                                 frozen_counter
    assert frozen_counter & FrozenCounter('a') == FrozenCounter('a')
    assert frozen_counter & frozen_counter == \
           frozen_counter & frozen_counter & frozen_counter == \
                                                                 frozen_counter
    
    assert FrozenCounter(frozen_counter.elements()) == frozen_counter
    
    assert +frozen_counter == frozen_counter
    assert ---frozen_counter == -frozen_counter != \
                                             frozen_counter == --frozen_counter
    
    assert repr(frozen_counter).startswith('FrozenCounter(')
    
    assert pickle.loads(pickle.dumps(frozen_counter)) == frozen_counter
    
def test_ordering():
    counter_0 = FrozenCounter('c')
    counter_1 = FrozenCounter('abc')
    counter_2 = FrozenCounter('aabc')
    counter_3 = FrozenCounter('abbc')
    counter_4 = FrozenCounter('aabbcc')
    
    hierarchy = (
        (counter_4, {counter_3, counter_2, counter_1, counter_0}),
        (counter_3, {counter_1, counter_0}),
        (counter_2, {counter_1, counter_0}),
        (counter_1, {counter_0}),
        (counter_0, set()),
    )
    
    for item, smaller_items in hierarchy:
        if not isinstance(item, FrozenCounter):
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

def test_ignores_zero():
    frozen_counter_0 = FrozenCounter({'a': 0,})
    frozen_counter_1 = FrozenCounter()
    assert frozen_counter_0 == frozen_counter_1
    
    assert hash(frozen_counter_0) == hash(frozen_counter_1)
    assert {frozen_counter_0, frozen_counter_1} == {frozen_counter_0} == \
                                                             {frozen_counter_1}
    
    frozen_counter_2 = FrozenCounter(
                       {'a': 0.0, 'b': 2, 'c': decimal_module.Decimal('0.0'),})
    frozen_counter_3 = FrozenCounter('bb')
    
    assert hash(frozen_counter_2) == hash(frozen_counter_3)
    assert {frozen_counter_2, frozen_counter_3} == {frozen_counter_2} == \
                                                             {frozen_counter_3}


def test_immutable():
    frozen_counter = FrozenCounter('abracadabra')
    with cute_testing.RaiseAssertor(TypeError):
        frozen_counter['a'] += 1
    with cute_testing.RaiseAssertor(TypeError):
        frozen_counter['a'] -= 1
    with cute_testing.RaiseAssertor(TypeError):
        frozen_counter['a'] = 7
    