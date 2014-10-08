# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

import uuid
import re
import pickle
import itertools
import collections
import decimal as decimal_module
from python_toolbox.third_party import unittest2

import nose

from python_toolbox import cute_iter_tools
from python_toolbox import sequence_tools
from python_toolbox import cute_testing


from python_toolbox import nifty_collections
from python_toolbox.nifty_collections import (Bag, OrderedBag,
                                              FrozenBag, FrozenOrderedBag,
                                              OrderedDict)

infinity = float('inf')
infinities = (infinity, -infinity)

class BaseBagTestCase(cute_testing.TestCase):
    def test_common(self):
        bag = self.bag_type('abracadabra')
        assert bag == collections.Counter('abracadabra') == \
               collections.Counter(bag) == \
               self.bag_type(collections.Counter('abracadabra'))
        
        assert len(bag) == 5
        assert set(bag) == set(bag.keys()) == set('abracadabra')
        assert set(bag.values()) == {1, 2, 5}
        assert set(bag.items()) == \
                                 {('a', 5), ('r', 2), ('b', 2), ('c', 1), ('d', 1)}
        assert bag['a'] == 5
        assert bag['missing value'] == 0
        assert len(bag) == 5
        
        assert set(bag.most_common()) == \
                                 set(collections.Counter(bag).most_common()) == \
                           set(collections.Counter(bag.elements()).most_common())
        
        assert bag + bag == self.bag_type('abracadabra' * 2)
        assert bag - bag == self.bag_type()
        assert bag - self.bag_type('a') == self.bag_type('abracadabr')
        assert bag - self.bag_type('a') == self.bag_type('abracadabr')
        assert bag | self.bag_type('a') == bag
        assert bag | bag == bag | bag | bag == bag
        assert bag & self.bag_type('a') == self.bag_type('a')
        assert bag & bag == \
               bag & bag & bag == bag
        
        assert self.bag_type(bag.elements()) == bag
        
        assert +bag == bag
        with cute_testing.RaiseAssertor(TypeError):
            - bag
        
        assert re.match('^(Frozen)?(Ordered)?Bag\(.*$', repr(bag))
        
        assert bag.copy() == bag
        
        assert pickle.loads(pickle.dumps(bag)) == bag
        
        assert self.bag_type({'a': 0, 'b': 1,}) == \
                                             self.bag_type({'c': 0, 'b': 1,})
        
    def test_repr(self):
        assert re.match(
            self._repr_result_pattern, 
            repr(self.bag_type('ababb'))
        )
        

    def test_no_subtract(self):
        # It's a silly method, yo.
        assert not hasattr(self.bag_type, 'subtract')
        

    def test_comparison(self):
        bag_0 = self.bag_type('c')
        bag_1 = self.bag_type('abc')
        bag_2 = self.bag_type('aabc')
        bag_3 = self.bag_type('abbc')
        bag_4 = self.bag_type('aabbcc')
        not_a_bag = {}
        
        hierarchy = (
            (bag_4, [bag_3, bag_2, bag_1, bag_0]),
            (bag_3, [bag_1, bag_0]),
            (bag_2, [bag_1, bag_0]),
            (bag_1, [bag_0]),
            (bag_0, []), 
        )
        
        for item, smaller_items in hierarchy:
            if not isinstance(item, self.bag_type):
                continue
            for smaller_item in smaller_items:
                assert not item <= smaller_item
                assert not item < smaller_item
                assert item >= smaller_item
                assert item > smaller_item
                assert item != smaller_item
            not_smaller_items = [item for item in next(zip(*hierarchy)) if
                                                     item not in smaller_items]
            for not_smaller_item in not_smaller_items:
                assert not item < smaller_item
                
            with cute_testing.RaiseAssertor(TypeError):
                item <= not_a_bag
            with cute_testing.RaiseAssertor(TypeError):
                item < not_a_bag
            with cute_testing.RaiseAssertor(TypeError):
                item > not_a_bag
            with cute_testing.RaiseAssertor(TypeError):
                item >= not_a_bag
            with cute_testing.RaiseAssertor(TypeError):
                not_a_bag <= item 
            with cute_testing.RaiseAssertor(TypeError):
                not_a_bag < item 
            with cute_testing.RaiseAssertor(TypeError):
                not_a_bag > item 
            with cute_testing.RaiseAssertor(TypeError):
                not_a_bag >= item 

    def test_only_positive_ints_or_zero(self):
        assert self.bag_type(
            OrderedDict([('a', 0), ('b', 0.0), ('c', 1), ('d', 2.0),
                         ('e', decimal_module.Decimal('3.0'))])) == \
                                                        self.bag_type('cddeee')
        with cute_testing.RaiseAssertor(TypeError):
            self.bag_type({'a': 1.1,})
        with cute_testing.RaiseAssertor(TypeError):
            self.bag_type({'a': -2,})
        with cute_testing.RaiseAssertor(TypeError):
            self.bag_type({'a': -3,})
        with cute_testing.RaiseAssertor(TypeError):
            self.bag_type({'a': decimal_module.Decimal('-3'),})
        with cute_testing.RaiseAssertor(TypeError):
            self.bag_type({'a': infinity,})
        with cute_testing.RaiseAssertor(TypeError):
            self.bag_type({'a': -infinity,})
        with cute_testing.RaiseAssertor(TypeError):
            self.bag_type({'a': 'whatever',})
        with cute_testing.RaiseAssertor(TypeError):
            self.bag_type({'a': b'whateva',})
        with cute_testing.RaiseAssertor(TypeError):
            self.bag_type({'a': ('still', 'nope'),})
        
    def test_ignores_zero(self):
        bag_0 = self.bag_type({'a': 0,})
        bag_1 = self.bag_type()
        assert bag_0 == bag_1
        
        if issubclass(self.bag_type, collections.Hashable):
            assert hash(bag_0) == hash(bag_1)
            assert {bag_0, bag_1} == {bag_0} == {bag_1}
        
        bag_2 = \
         self.bag_type({'a': 0.0, 'b': 2, 'c': decimal_module.Decimal('0.0'),})
        bag_3 = self.bag_type('bb')
        
        if issubclass(self.bag_type, collections.Hashable):
            assert hash(bag_2) == hash(bag_3)
            assert {bag_2, bag_3} == {bag_2} == {bag_3}
    
    
        
        
class BaseMutableBagTestCase(BaseBagTestCase):
    def test_hash(self):
        bag = self.bag_type('abracadabra')
        assert not isinstance(bag, collections.Hashable)
        assert not issubclass(self.bag_type, collections.Hashable)
        with cute_testing.RaiseAssertor(TypeError):
            {bag}
        with cute_testing.RaiseAssertor(TypeError):
            {bag: None,}
        with cute_testing.RaiseAssertor(TypeError):
            hash(bag)
            
    def test_mutating(self):
        bag = self.bag_type('abracadabra')
        with cute_testing.RaiseAssertor(TypeError):
            bag['a'] += 1
        with cute_testing.RaiseAssertor(TypeError):
            bag['a'] -= 1
        with cute_testing.RaiseAssertor(TypeError):
            bag['a'] = 7
        
    
    def test_mutating(self):
        bag = self.bag_type('abracadabra')
        bag['a'] += 1
        assert bag == self.bag_type('abracadabra' + 'a')
            
        bag = self.bag_type('abracadabra')
        bag['a'] -= 1
        assert bag == self.bag_type('abracadabr')

        bag = self.bag_type('abracadabra')
        bag['a'] %= 2
        assert bag == self.bag_type('abrcdbr')

        bag = self.bag_type('abracadabra')
        bag += bag
        assert bag == self.bag_type('abracadabra' * 2)

        bag = self.bag_type('abracadabra')
        bag -= bag
        assert bag == self.bag_type()

        bag = self.bag_type('abracadabra')
        bag %= 2
        assert bag == self.bag_type('acd')

        bag = self.bag_type('abracadabra')
        bag['a'] = 7
        assert bag == self.bag_type('abracadabra' + 'aa')

        bag = self.bag_type('abracadabra')
        assert bag.setdefault('a', 7) == 5
        assert bag == self.bag_type('abracadabra')
        
        bag = self.bag_type('abracadabra')
        assert bag.setdefault('x', 7) == 7
        assert bag == self.bag_type('abracadabra' + 'x' * 7)

        bag = self.bag_type('abracadabra')
        assert bag.pop('a', 7) == 5
        assert bag == self.bag_type('brcdbr')
        assert bag.pop('x', 7) == 7
        assert bag == self.bag_type('brcdbr')

        bag = self.bag_type('abracadabra')
        key, value = bag.popitem()
        assert key in 'abracadabra'
        if isinstance(bag, nifty_collections.Ordered):
            assert key == 'a'
        assert bag == self.bag_type([c for c in 'abracadabra' if c != key])
        other_key, other_value = bag.popitem()
        assert other_key in 'abracadabra'
        if isinstance(bag, nifty_collections.Ordered):
            assert key == 'd'
        assert bag == self.bag_type([c for c in 'abracadabra'
                                                 if c not in {key, other_key}])

        bag = self.bag_type('abracadabra')
        del bag['a']
        assert bag == self.bag_type('brcdbr')

        bag = self.bag_type('abracadabra')
        bag.update(bag)
        assert bag == self.bag_type('abracadabra')
            
        
    
class BaseFrozenBagTestCase(BaseBagTestCase):
    
    def test_hash(self):
        bag = self.bag_type('abracadabra')
        assert isinstance(bag, collections.Hashable)
        assert issubclass(self.bag_type, collections.Hashable)
        assert {bag, bag} == {bag}
        assert {bag: bag} == {bag: bag}
        assert isinstance(hash(bag), int)
    

    def test_mutating(bag_type):
        bag = bag_type('abracadabra')
        with cute_testing.RaiseAssertor(TypeError):
            bag['a'] += 1
        with cute_testing.RaiseAssertor(TypeError):
            bag['a'] -= 1
        with cute_testing.RaiseAssertor(TypeError):
            bag['a'] %= 2
        with cute_testing.RaiseAssertor(TypeError):
            bag += bag
        with cute_testing.RaiseAssertor(TypeError):
            bag -= bag
        with cute_testing.RaiseAssertor(TypeError):
            bag %= bag
        with cute_testing.RaiseAssertor(TypeError):
            bag['a'] = 7
        with cute_testing.RaiseAssertor(TypeError):
            bag.setdefault('a', 7)
        with cute_testing.RaiseAssertor(TypeError):
            bag.pop('a', 7)
        with cute_testing.RaiseAssertor(TypeError):
            bag.popitem()
        with cute_testing.RaiseAssertor(TypeError):
            del bag['a']
        with cute_testing.RaiseAssertor(TypeError):
            bag.update(bag)
            
        
              
class BaseOrderedBagTestCase(BaseBagTestCase):
    
    def test_ordering(self):
        ordered_bag_0 = self.bag_type('ababb')
        ordered_bag_1 = self.bag_type('bbbaa')
        assert ordered_bag_0 == ordered_bag_0
        assert hash(ordered_bag_0) == hash(ordered_bag_0)
        assert ordered_bag_1 == ordered_bag_1
        assert hash(ordered_bag_1) == hash(ordered_bag_1)
        assert ordered_bag_0 != ordered_bag_1
        assert ordered_bag_0 <= ordered_bag_1
        assert ordered_bag_0 >= ordered_bag_1
          
    
class BaseUnorderedBagTestCase(BaseBagTestCase):
    
    def test_ordering(self):
        bag_0 = self.bag_type('ababb')
        bag_1 = self.bag_type('bbbaa')
        assert bag_0 == bag_1
        assert hash(bag_0) == hash(bag_1)
        
###############################################################################

# Now start the concrete test classes:

    
class BagTestCase(BaseMutableBagTestCase, BaseUnorderedBagTestCase):
    __test__ = True
    bag_type = Bag

    _repr_result_pattern = ("^Bag\\({(?:(?:'b': 3, 'a': 2)|"
                            "(?:'a': 2, 'b': 3))}\\)$")

class OrderedBagTestCase(BaseMutableBagTestCase,
                           BaseOrderedBagTestCase):
    __test__ = True
    bag_type = OrderedBag
    
    _repr_result_pattern = ("^OrderedBag\\(\\[\\('a', 2\\), "
                            "\\('b', 3\\)\\]\\)$")

        

    
    
class FrozenBagTestCase(BaseFrozenBagTestCase, BaseUnorderedBagTestCase):
    __test__ = True
    bag_type = FrozenBag
    
    _repr_result_pattern = ("^FrozenBag\\({(?:(?:'b': 3, 'a': 2)|"
                            "(?:'a': 2, 'b': 3))}\\)$")

class FrozenOrderedBagTestCase(BaseFrozenBagTestCase,
                               BaseOrderedBagTestCase):
    __test__ = True
    bag_type = FrozenOrderedBag
    
    _repr_result_pattern = ("^FrozenOrderedBag\\(\\[\\('a', 2\\), "
                            "\\('b', 3\\)\\]\\)$")


    

