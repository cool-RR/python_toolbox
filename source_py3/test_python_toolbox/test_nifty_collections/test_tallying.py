# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

import uuid
import re
import pickle
import itertools
import collections
import decimal as decimal_module

from python_toolbox import cute_iter_tools
from python_toolbox import sequence_tools
from python_toolbox import cute_testing


from python_toolbox.nifty_collections import (Tally, OrderedTally,
                                              FrozenTally, FrozenOrderedTally,
                                              OrderedDict)

infinity = float('inf')
infinities = (infinity, -infinity)

_check_functions = []
def _test_on(arguments):
    def decorator(check_function):
        check_function.arguments = arguments
        _check_functions.append(check_function)
        return check_function
    return decorator
        


def test():
    assert Tally.is_ordered is False
    assert Tally.is_frozen is False
    assert OrderedTally.is_ordered is True
    assert OrderedTally.is_frozen is False
    assert FrozenTally.is_ordered is False
    assert FrozenTally.is_frozen is True
    assert FrozenOrderedTally.is_ordered is True
    assert FrozenOrderedTally.is_frozen is True
    assert OrderedDict.is_ordered is True
    assert OrderedDict.is_frozen is False
    
    for check_function in _check_functions:
        for argument in _check_function.arguments:
            _check_function(argument)
        

@_test_on(Tally, OrderedTally, FrozenTally, FrozenOrderedTally)
def _check_common(tally_type):
    tally = tally_type('abracadabra')
    assert tally == collections.Counter('abracadabra') == \
           collections.Counter(tally) == \
           tally_type(collections.Counter('abracadabra'))
    
    assert len(tally) == 5
    assert set(tally) == set(tally.keys()) == set('abracadabra')
    assert set(tally.values()) == {1, 2, 5}
    assert set(tally.items()) == \
                             {('a', 5), ('r', 2), ('b', 2), ('c', 1), ('d', 1)}
    assert tally['a'] == 5
    assert tally['missing value'] == 0
    assert len(tally) == 5
    if tally.is_frozen:
        assert {tally, tally} == {tally}
        assert {tally: tally} == {tally: tally}
        assert isinstance(hash(tally), int)
    else:
        with cute_testing.RaiseAssertor(TypeError):
            {tally}
        with cute_testing.RaiseAssertor(TypeError):
            {tally: None,}
        with cute_testing.RaiseAssertor(TypeError):
            assert isinstance(hash(tally), int)
            
    
    assert set(tally.most_common()) == \
                             set(collections.Counter(tally).most_common()) == \
                       set(collections.Counter(tally.elements()).most_common())
    
    assert tally + tally == tally_type('abracadabra' * 2)
    assert tally - tally == tally_type()
    assert tally - tally_type('a') == tally_type('abracadabr')
    assert tally - tally_type('a') == tally_type('abracadabr')
    assert tally | tally_type('a') == tally
    assert tally | tally == tally | tally | tally == tally
    assert tally & tally_type('a') == tally_type('a')
    assert tally & tally == \
           tally & tally & tally == tally
    
    assert tally_type(tally.elements()) == tally
    
    assert +tally == tally
    with cute_testing.RaiseAssertor(TypeError):
        - tally
    
    assert re.match('^(Frozen)?(Ordered)?Tally\(.*$', repr(tally))
    
    assert tally.copy({'meow': 9}) == \
           tally.copy(meow=9) == \
           tally_type(OrderedDict(
               [('a', 5), ('b', 2), ('r', 2), ('c', 1), ('d', 1), ('meow', 9)])
           )
    
    assert pickle.loads(pickle.dumps(tally)) == tally
    
    assert tally_type({'a': 0, 'b': 1,}) == \
                                         tally_type({'c': 0, 'b': 1,})
    
    
@_test_on(Tally, OrderedTally, FrozenTally, FrozenOrderedTally)
def _check_comparison(tally_type):
    tally_0 = tally_type('c')
    tally_1 = tally_type('abc')
    tally_2 = tally_type('aabc')
    tally_3 = tally_type('abbc')
    tally_4 = tally_type('aabbcc')
    not_a_tally = {}
    
    hierarchy = (
        (tally_4, {tally_3, tally_2, tally_1, tally_0}),
        (tally_3, {tally_1, tally_0}),
        (tally_2, {tally_1, tally_0}),
        (tally_1, {tally_0}),
        (tally_0, set()),
    )
    
    for item, smaller_items in hierarchy:
        if not isinstance(item, tally_type):
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
            
        with cute_testing.RaiseAssertor(TypeError):
            item <= not_a_tally
        with cute_testing.RaiseAssertor(TypeError):
            item < not_a_tally
        with cute_testing.RaiseAssertor(TypeError):
            item > not_a_tally
        with cute_testing.RaiseAssertor(TypeError):
            item >= not_a_tally
        with cute_testing.RaiseAssertor(TypeError):
            not_a_tally <= item 
        with cute_testing.RaiseAssertor(TypeError):
            not_a_tally < item 
        with cute_testing.RaiseAssertor(TypeError):
            not_a_tally > item 
        with cute_testing.RaiseAssertor(TypeError):
            not_a_tally >= item 

@_test_on(Tally, OrderedTally, FrozenTally, FrozenOrderedTally)
def _check_ignores_zero(tally_type):
    frozen_tally_0 = tally_type({'a': 0,})
    frozen_tally_1 = tally_type()
    assert frozen_tally_0 == frozen_tally_1
    
    assert hash(frozen_tally_0) == hash(frozen_tally_1)
    assert {frozen_tally_0, frozen_tally_1} == {frozen_tally_0} == \
                                                             {frozen_tally_1}
    
    frozen_tally_2 = tally_type(
                       {'a': 0.0, 'b': 2, 'c': decimal_module.Decimal('0.0'),})
    frozen_tally_3 = tally_type('bb')
    
    assert hash(frozen_tally_2) == hash(frozen_tally_3)
    assert {frozen_tally_2, frozen_tally_3} == {frozen_tally_2} == \
                                                             {frozen_tally_3}


@_test_on(Tally, OrderedTally, FrozenTally, FrozenOrderedTally)
def _check_mutating(tally_type):
    frozen_tally = tally_type('abracadabra')
    with cute_testing.RaiseAssertor(TypeError):
        frozen_tally['a'] += 1
    with cute_testing.RaiseAssertor(TypeError):
        frozen_tally['a'] -= 1
    with cute_testing.RaiseAssertor(TypeError):
        frozen_tally['a'] = 7
    

    
@_test_on(Tally, OrderedTally, FrozenTally, FrozenOrderedTally)
def _check_only_positive_ints_or_zero(tally_type):
    assert tally_type(
        OrderedDict([('a', 0), ('b', 0.0), ('c', 1), ('d', 2.0),
                     ('e', decimal_module.Decimal('3.0'))])) == \
                                                          tally_type('cddeee')
    with cute_testing.RaiseAssertor(TypeError):
        tally_type({'a': 1.1,})
    with cute_testing.RaiseAssertor(TypeError):
        tally_type({'a': -2,})
    with cute_testing.RaiseAssertor(TypeError):
        tally_type({'a': -3,})
    with cute_testing.RaiseAssertor(TypeError):
        tally_type({'a': decimal_module.Decimal('-3'),})
    with cute_testing.RaiseAssertor(TypeError):
        tally_type({'a': infinity,})
    with cute_testing.RaiseAssertor(TypeError):
        tally_type({'a': -infinity,})
    with cute_testing.RaiseAssertor(TypeError):
        tally_type({'a': 'whatever',})
    with cute_testing.RaiseAssertor(TypeError):
        tally_type({'a': b'whateva',})
    with cute_testing.RaiseAssertor(TypeError):
        tally_type({'a': ('still', 'nope'),})
    
    

@_test_on(Tally, OrderedTally, FrozenTally, FrozenOrderedTally)
def _check_ordered():
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
    

@_test_on(Tally, OrderedTally, FrozenTally, FrozenOrderedTally)
def test_repr():
    assert re.match(
        "^FrozenTally\\({(?:(?:'b': 3, 'a': 2)|(?:'a': 2, 'b': 3))}\\)$", 
        repr(FrozenTally('ababb'))
    )
    assert repr(FrozenOrderedTally('ababb')) == \
                                     "FrozenOrderedTally([('a', 2), ('b', 3)])"
    
    
