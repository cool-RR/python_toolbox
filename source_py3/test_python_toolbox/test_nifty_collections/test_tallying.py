# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

import uuid
import re
import pickle
import itertools
import collections
import decimal as decimal_module

import nose

from python_toolbox import cute_iter_tools
from python_toolbox import sequence_tools
from python_toolbox import cute_testing


from python_toolbox.nifty_collections import (Tally, OrderedTally,
                                              FrozenTally, FrozenOrderedTally,
                                              OrderedDict)

infinity = float('inf')
infinities = (infinity, -infinity)

class BaseTallyTestCase(cute_testing.TestCase):
    def test_common(self, tally_type):
        tally = self.tally_type('abracadabra')
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
        
        assert set(tally.most_common()) == \
                                 set(collections.Counter(tally).most_common()) == \
                           set(collections.Counter(tally.elements()).most_common())
        
        assert tally + tally == self.tally_type('abracadabra' * 2)
        assert tally - tally == self.tally_type()
        assert tally - tally_type('a') == self.tally_type('abracadabr')
        assert tally - tally_type('a') == self.tally_type('abracadabr')
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
        
        assert self.tally_type({'a': 0, 'b': 1,}) == \
                                             self.tally_type({'c': 0, 'b': 1,})
        
    def test_repr(self):
        assert re.match(
            self._repr_result_pattern, 
            repr(self.tally_type('ababb'))
        )
        

    def test_comparison(self):
        tally_0 = self.tally_type('c')
        tally_1 = self.tally_type('abc')
        tally_2 = self.tally_type('aabc')
        tally_3 = self.tally_type('abbc')
        tally_4 = self.tally_type('aabbcc')
        not_a_tally = {}
        
        hierarchy = (
            (tally_4, {tally_3, tally_2, tally_1, tally_0}),
            (tally_3, {tally_1, tally_0}),
            (tally_2, {tally_1, tally_0}),
            (tally_1, {tally_0}),
            (tally_0, set()),
        )
        
        for item, smaller_items in hierarchy:
            if not isinstance(item, self.tally_type):
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

    def test_only_positive_ints_or_zero(self):
        assert self.tally_type(
            OrderedDict([('a', 0), ('b', 0.0), ('c', 1), ('d', 2.0),
                         ('e', decimal_module.Decimal('3.0'))])) == \
                                                      self.tally_type('cddeee')
        with cute_testing.RaiseAssertor(TypeError):
            self.tally_type({'a': 1.1,})
        with cute_testing.RaiseAssertor(TypeError):
            self.tally_type({'a': -2,})
        with cute_testing.RaiseAssertor(TypeError):
            self.tally_type({'a': -3,})
        with cute_testing.RaiseAssertor(TypeError):
            self.tally_type({'a': decimal_module.Decimal('-3'),})
        with cute_testing.RaiseAssertor(TypeError):
            self.tally_type({'a': infinity,})
        with cute_testing.RaiseAssertor(TypeError):
            self.tally_type({'a': -infinity,})
        with cute_testing.RaiseAssertor(TypeError):
            self.tally_type({'a': 'whatever',})
        with cute_testing.RaiseAssertor(TypeError):
            self.tally_type({'a': b'whateva',})
        with cute_testing.RaiseAssertor(TypeError):
            self.tally_type({'a': ('still', 'nope'),})
        
    def test_ignores_zero(tally_type):
        tally_0 = tally_type({'a': 0,})
        tally_1 = tally_type()
        assert tally_0 == tally_1
        
        if tally_type.is_frozen:
            assert hash(tally_0) == hash(tally_1)
            assert {tally_0, tally_1} == {tally_0} == {tally_1}
        
        tally_2 = tally_type(
                           {'a': 0.0, 'b': 2, 'c': decimal_module.Decimal('0.0'),})
        tally_3 = tally_type('bb')
        
        if tally_type.is_frozen:
            assert hash(tally_2) == hash(tally_3)
            assert {tally_2, tally_3} == {tally_2} == {tally_3}
    
    
        
        
class BaseMutableTallyTestCase(BaseTallyTestCase):
    is_frozen = False
    
    def test_hash(self):
        tally = self.tally_type('abracadabra')
        with cute_testing.RaiseAssertor(TypeError):
            {tally}
        with cute_testing.RaiseAssertor(TypeError):
            {tally: None,}
        with cute_testing.RaiseAssertor(TypeError):
            hash(tally)
        
    
class BaseFrozenTallyTestCase(BaseTallyTestCase):
    is_frozen = True
    
    def test_hash(self):
        tally = self.tally_type('abracadabra')
        assert {tally, tally} == {tally}
        assert {tally: tally} == {tally: tally}
        assert isinstance(hash(tally), int)
    
    
class BaseOrderedTallyTestCase(BaseTallyTestCase):
    is_ordered = True
    
    def test_ordering(self):
        ordered_tally_0 = self.tally_type('ababb')
        ordered_tally_1 = self.tally_type('bbbaa')
        assert ordered_tally_0 == ordered_tally_0
        assert hash(ordered_tally_0) == hash(ordered_tally_0)
        assert ordered_tally_1 == ordered_tally_1
        assert hash(ordered_tally_1) == hash(ordered_tally_1)
        assert ordered_tally_0 != ordered_tally_1
        assert ordered_tally_0 <= ordered_tally_1
        assert ordered_tally_0 >= ordered_tally_1
          
    
class BaseUnorderedTallyTestCase(BaseTallyTestCase):
    is_ordered = False
    
    def test_ordering(self):
        tally_0 = self.tally_type('ababb')
        tally_1 = self.tally_type('bbbaa')
        assert tally_0 == tally_1
        assert hash(tally_0) == hash(tally_1)
        
###############################################################################

# Now start the concrete test classes:

    
class TallyTestCase(BaseMutableTallyTestCase, BaseUnorderedTallyTestCase):
    tally_type = Tally

    _repr_result_pattern = ("^Tally\\({(?:(?:'b': 3, 'a': 2)|"
                            "(?:'a': 2, 'b': 3))}\\)$")

class OrderedTallyTestCase(BaseMutableTallyTestCase,
                           BaseOrderedTallyTestCase):
    tally_type = OrderedTally
    
    _repr_result_pattern = ("^OrderedTally\\(\\[\\('a', 2\\), "
                            "\\('b', 3\\)\\]\\)$")

        

    
    
class FrozenTallyTestCase(BaseFrozenTallyTestCase, BaseUnorderedTallyTestCase):
    tally_type = FrozenTally
    
    _repr_result_pattern = ("^FrozenTally\\({(?:(?:'b': 3, 'a': 2)|"
                            "(?:'a': 2, 'b': 3))}\\)$")

class FrozenOrderedTallyTestCase(BaseFrozenTallyTestCase,
                           BaseOrderedTallyTestCase):
    tally_type = FrozenOrderedTally
    
    _repr_result_pattern = ("^FrozenOrderedTally\\(\\[\\('a', 2\\), "
                            "\\('b', 3\\)\\]\\)$")


    

@_test_on(Tally, OrderedTally, FrozenTally, FrozenOrderedTally)
def test_mutating(tally_type):
    tally = tally_type('abracadabra')
    with cute_testing.RaiseAssertor(TypeError):
        tally['a'] += 1
    with cute_testing.RaiseAssertor(TypeError):
        tally['a'] -= 1
    with cute_testing.RaiseAssertor(TypeError):
        tally['a'] = 7
    

    
