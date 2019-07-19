# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import generator_stop

import re
import pickle
import abc
import collections
import decimal as decimal_module
import unittest
import copy

from python_toolbox import cute_iter_tools
from python_toolbox import temp_value_setting
from python_toolbox import sequence_tools
from python_toolbox import cute_testing

from python_toolbox import nifty_collections
from python_toolbox.nifty_collections import (Bag, OrderedBag,
                                              FrozenBag, FrozenOrderedBag,
                                              OrderedDict)

infinity = float('inf')
infinities = (infinity, -infinity)

class BaseBagTestCase(cute_testing.TestCase, metaclass=abc.ABCMeta):
    __test__ = False
    def test_common(self):
        bag = self.bag_type('abracadabra')
        if not issubclass(self.bag_type, nifty_collections.Ordered):
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
        assert 'a' in bag
        assert 'r' in bag
        assert 'R' not in bag
        assert 'x' not in self.bag_type({'x': 0,})

        assert bag != 7

        assert set(bag.most_common()) == set(bag.most_common(len(bag))) == \
                               set(collections.Counter(bag).most_common()) == \
                         set(collections.Counter(bag.elements).most_common())

        assert bag.most_common(1) == (('a', 5),)
        assert set(bag.most_common(3)) == set((('a', 5), ('b', 2), ('r', 2)))

        assert bag + bag == self.bag_type('abracadabra' * 2)
        assert bag - bag == self.bag_type()
        assert bag - self.bag_type('a') == self.bag_type('abracadabr')
        assert bag - self.bag_type('a') == self.bag_type('abracadabr')
        assert bag | self.bag_type('a') == bag
        assert bag | bag == bag | bag | bag == bag
        assert bag & self.bag_type('a') == self.bag_type('a')
        assert bag & bag == \
               bag & bag & bag == bag

        assert self.bag_type(bag.elements) == bag

        with cute_testing.RaiseAssertor(TypeError):
            + bag
        with cute_testing.RaiseAssertor(TypeError):
            - bag

        assert re.match(r'^(Frozen)?(Ordered)?Bag\(.*$', repr(bag))

        assert bag.copy() == bag

        assert pickle.loads(pickle.dumps(bag)) == bag

        assert self.bag_type({'a': 0, 'b': 1,}) == \
                                             self.bag_type({'c': 0, 'b': 1,})

    def test_bool(self):
        bag = self.bag_type('meow')
        assert bool(bag) is True
        assert bag
        assert bool(self.bag_type()) is bool(self.bag_type('')) is \
                                        bool(self.bag_type({'d': 0,})) is False
        if not isinstance(bag, collections.abc.Hashable):
            bag.clear()
            assert bool(bag) is False
            assert not bag


    def test_n_elements(self):
        bag = self.bag_type('meow')
        assert bag.n_elements == 4
        assert bag.n_elements == 4 # Testing again because now it's a data
                                   # attribute.
        if not isinstance(bag, collections.abc.Hashable):
            bag['x'] = 1
            assert bag.n_elements == 5
            assert bag.n_elements == 5


    def test_frozen_bag_bag(self):
        bag = self.bag_type('meeeow')
        assert bag.frozen_bag_bag == \
                                  nifty_collections.FrozenBagBag({3: 1, 1: 3,})
        if not isinstance(bag, collections.abc.Hashable):
            bag['o'] += 2
            assert bag.frozen_bag_bag == \
                                  nifty_collections.FrozenBagBag({3: 2, 1: 2,})


    def test_no_visible_dict(self):
        bag = self.bag_type('abc')
        with cute_testing.RaiseAssertor(AttributeError):
            bag.data
        with cute_testing.RaiseAssertor(AttributeError):
            bag.dict



    def test_repr(self):
        bag = self.bag_type('ababb')
        assert eval(repr(bag)) == bag
        assert re.match(self._repr_result_pattern, repr(bag))

        empty_bag = self.bag_type()
        assert eval(repr(empty_bag)) == empty_bag
        assert repr(empty_bag) == '%s()' % self.bag_type.__name__


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
                assert smaller_item <= item
                assert smaller_item < item
                assert not smaller_item >= item
                assert not smaller_item > item
                assert smaller_item != item
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

        if issubclass(self.bag_type, collections.abc.Hashable):
            assert hash(bag_0) == hash(bag_1)
            assert {bag_0, bag_1} == {bag_0} == {bag_1}

        bag_2 = \
         self.bag_type({'a': 0.0, 'b': 2, 'c': decimal_module.Decimal('0.0'),})
        bag_3 = self.bag_type('bb')

        if issubclass(self.bag_type, collections.abc.Hashable):
            assert hash(bag_2) == hash(bag_3)
            assert {bag_2, bag_3} == {bag_2} == {bag_3}

    def test_copy(self):
        class O: pass
        o = O()
        bag = self.bag_type({o: 3})
        bag_shallow_copy = copy.copy(bag)
        bag_deep_copy = copy.deepcopy(bag)
        assert bag_shallow_copy == bag != bag_deep_copy
        assert next(iter(bag_shallow_copy)) == next(iter(bag_shallow_copy)) \
                                                   != next(iter(bag_deep_copy))
        assert next(iter(bag_shallow_copy)) is next(iter(bag_shallow_copy)) \
                                               is not next(iter(bag_deep_copy))


    def test_move_to_end(self):
        # Overridden in test cases for bag types where it's implemented.
        bag = self.bag_type('aaabbc')
        with cute_testing.RaiseAssertor(AttributeError):
            bag.move_to_end('c')
        with cute_testing.RaiseAssertor(AttributeError):
            bag.move_to_end('x', last=False)


    def test_sort(self):
        # Overridden in test cases for bag types where it's implemented.
        bag = self.bag_type('aaabbc')
        with cute_testing.RaiseAssertor(AttributeError):
            bag.sort()

    def test_operations_with_foreign_operands(self):
        bag = self.bag_type('meeeeow')
        with cute_testing.RaiseAssertor(TypeError): bag | 'foo'
        with cute_testing.RaiseAssertor(TypeError): 'foo' | bag
        with cute_testing.RaiseAssertor(TypeError): bag & 'foo'
        with cute_testing.RaiseAssertor(TypeError): 'foo' & bag
        with cute_testing.RaiseAssertor(TypeError): bag + 'foo'
        with cute_testing.RaiseAssertor(TypeError): 'foo' + bag
        with cute_testing.RaiseAssertor(TypeError): bag - 'foo'
        with cute_testing.RaiseAssertor(TypeError): 'foo' - bag
        with cute_testing.RaiseAssertor(TypeError): bag * 'foo'
        with cute_testing.RaiseAssertor(TypeError): 'foo' * bag
        with cute_testing.RaiseAssertor(TypeError): bag / 'foo'
        with cute_testing.RaiseAssertor(TypeError): 'foo' / bag
        with cute_testing.RaiseAssertor(TypeError): bag / 3
        with cute_testing.RaiseAssertor(TypeError): 3 / bag
        with cute_testing.RaiseAssertor(TypeError): bag // 'foo'
        with cute_testing.RaiseAssertor(TypeError): 'foo' // bag
        with cute_testing.RaiseAssertor(TypeError): bag % 'foo'
        with cute_testing.RaiseAssertor(TypeError): 3 % bag
        with cute_testing.RaiseAssertor(TypeError): bag ** 'foo'
        with cute_testing.RaiseAssertor(TypeError): 'foo' ** bag
        with cute_testing.RaiseAssertor(TypeError): divmod(bag, 'foo')
        with cute_testing.RaiseAssertor(TypeError): divmod('foo', bag)
        if not isinstance(bag, collections.abc.Hashable):
            with cute_testing.RaiseAssertor(TypeError): bag |= 'foo'
            with cute_testing.RaiseAssertor(TypeError): bag &= 'foo'
            with cute_testing.RaiseAssertor(TypeError): bag += 'foo'
            with cute_testing.RaiseAssertor(TypeError): bag -= 'foo'
            with cute_testing.RaiseAssertor(TypeError): bag *= 'foo'
            with cute_testing.RaiseAssertor(TypeError): bag /= 'foo'
            with cute_testing.RaiseAssertor(TypeError): bag //= 'foo'
            with cute_testing.RaiseAssertor(TypeError): bag %= 'foo'
            with cute_testing.RaiseAssertor(TypeError): bag **= 'foo'

    def test_operations(self):
        bag_0 = self.bag_type('abbccc')
        bag_1 = self.bag_type('bcc')
        bag_2 = self.bag_type('cddddd')

        assert bag_0 + bag_1 == self.bag_type('abbccc' + 'bcc')
        assert bag_1 + bag_0 == self.bag_type('bcc' + 'abbccc')
        assert bag_0 + bag_2 == self.bag_type('abbccc' + 'cddddd')
        assert bag_2 + bag_0 == self.bag_type('cddddd' + 'abbccc')
        assert bag_1 + bag_2 == self.bag_type('bcc' + 'cddddd')
        assert bag_2 + bag_1 == self.bag_type('cddddd' + 'bcc')

        assert bag_0 - bag_1 == self.bag_type('abc')
        assert bag_1 - bag_0 == self.bag_type()
        assert bag_0 - bag_2 == self.bag_type('abbcc')
        assert bag_2 - bag_0 == self.bag_type('ddddd')
        assert bag_1 - bag_2 == self.bag_type('bc')
        assert bag_2 - bag_1 == self.bag_type('ddddd')

        assert bag_0 * 2 == self.bag_type('abbccc' * 2)
        assert bag_1 * 2 == self.bag_type('bcc' * 2)
        assert bag_2 * 2 == self.bag_type('cddddd' * 2)
        assert 3 * bag_0 == self.bag_type('abbccc' * 3)
        assert 3 * bag_1 == self.bag_type('bcc' * 3)
        assert 3 * bag_2 == self.bag_type('cddddd' * 3)

        # We only allow floor division on bags, not regular divison, because a
        # decimal bag is unheard of.
        with cute_testing.RaiseAssertor(TypeError):
            bag_0 / 2
        with cute_testing.RaiseAssertor(TypeError):
            bag_1 / 2
        with cute_testing.RaiseAssertor(TypeError):
            bag_2 / 2
        with cute_testing.RaiseAssertor(TypeError):
            bag_0 / self.bag_type('ab')
        with cute_testing.RaiseAssertor(TypeError):
            bag_1 / self.bag_type('ab')
        with cute_testing.RaiseAssertor(TypeError):
            bag_2 / self.bag_type('ab')

        assert bag_0 // 2 == self.bag_type('bc')
        assert bag_1 // 2 == self.bag_type('c')
        assert bag_2 // 2 == self.bag_type('dd')
        assert bag_0 // self.bag_type('ab') == 1
        assert bag_1 // self.bag_type('ab') == 0
        assert bag_2 // self.bag_type('ab') == 0

        with cute_testing.RaiseAssertor(ZeroDivisionError):
            bag_0 // 0
        with cute_testing.RaiseAssertor(ZeroDivisionError):
            bag_0 // self.bag_type()

        assert bag_0 % 2 == self.bag_type('ac') == bag_0 - ((bag_0 // 2) * 2) \
               == self.bag_type(OrderedDict((key, count % 2) for (key, count)
                                                             in bag_0.items()))
        assert bag_1 % 2 == self.bag_type('b') == bag_1 - ((bag_1 // 2) * 2) \
               == self.bag_type(OrderedDict((key, count % 2) for (key, count)
                                                             in bag_1.items()))
        assert bag_2 % 2 == self.bag_type('cd') == bag_2 - ((bag_2 // 2) * 2)\
               == self.bag_type(OrderedDict((key, count % 2) for (key, count)
                                                             in bag_2.items()))
        assert bag_0 % self.bag_type('ac') == self.bag_type('bbcc')
        assert bag_1 % self.bag_type('b') == self.bag_type('cc')
        assert bag_2 % self.bag_type('cd') == self.bag_type('dddd')

        assert bag_0 ** 2 == pow(bag_0, 2) == self.bag_type('abbbbccccccccc')
        assert bag_1 ** 2 == pow(bag_1, 2) == self.bag_type('bcccc')
        assert bag_2 ** 2 == pow(bag_2, 2) == \
                                    self.bag_type('cddddddddddddddddddddddddd')
        assert pow(bag_0, 2, 3) == self.bag_type('ab')
        assert pow(bag_1, 2, 3) == self.bag_type('bc')
        assert pow(bag_2, 2, 3) == self.bag_type('cd')

        assert divmod(bag_0, 3) == (bag_0 // 3, bag_0 % 3)
        assert divmod(bag_1, 3) == (bag_1 // 3, bag_1 % 3)
        assert divmod(bag_2, 3) == (bag_2 // 3, bag_2 % 3)
        assert divmod(bag_0, self.bag_type('cd')) == \
                    (bag_0 // self.bag_type('cd'), bag_0 % self.bag_type('cd'))
        assert divmod(bag_1, self.bag_type('cd')) == \
                    (bag_1 // self.bag_type('cd'), bag_1 % self.bag_type('cd'))
        assert divmod(bag_2, self.bag_type('cd')) == \
                    (bag_2 // self.bag_type('cd'), bag_2 % self.bag_type('cd'))



    def test_get_contained_bags(self):
        bag = self.bag_type('abracadabra')
        contained_bags = bag.get_contained_bags()
        assert len(contained_bags) == 6 * 3 * 2 * 2 * 3
        had_full_one = False
        for contained_bag in contained_bags:
            assert contained_bag <= bag
            if contained_bag == bag:
                assert had_full_one is False
                had_full_one = True
            else:
                assert contained_bag < bag
            if isinstance(bag, nifty_collections.Ordered):
                assert cute_iter_tools.is_sorted(
                    tuple(contained_bag.keys()),
                    key=tuple(bag.keys()).index
                )

        contained_bags_tuple = tuple(contained_bags)
        assert self.bag_type('abraca') in contained_bags_tuple
        assert self.bag_type('bd') in contained_bags_tuple
        assert self.bag_type() in contained_bags_tuple
        assert self.bag_type('x') not in contained_bags_tuple



class BaseMutableBagTestCase(BaseBagTestCase):

    def test_get_mutable(self):
        bag = self.bag_type('abracadabra')
        assert not hasattr(bag, 'get_mutable')
        with cute_testing.RaiseAssertor(AttributeError):
            bag.get_mutable()

    def test_get_frozen(self):
        bag = self.bag_type('abracadabra')
        frozen_bag = bag.get_frozen()
        assert isinstance(frozen_bag, collections.abc.Hashable)
        if isinstance(bag, nifty_collections.Ordered):
            assert tuple(bag.items()) == tuple(frozen_bag.items())
        else:
            assert set(bag.items()) == set(frozen_bag.items())
        assert type(frozen_bag).__name__ == f'Frozen{type(bag).__name__}'
        assert frozen_bag.get_mutable() == bag

    def test_hash(self):
        bag = self.bag_type('abracadabra')
        assert not isinstance(bag, collections.abc.Hashable)
        assert not issubclass(self.bag_type, collections.abc.Hashable)
        with cute_testing.RaiseAssertor(TypeError):
            {bag}
        with cute_testing.RaiseAssertor(TypeError):
            {bag: None,}
        with cute_testing.RaiseAssertor(TypeError):
            hash(bag)


    def test_mutating(self):
        bag = bag_reference = self.bag_type('abracadabra')
        bag['a'] += 1
        assert bag == self.bag_type('abracadabra' + 'a')
        assert bag is bag_reference

        bag = bag_reference = self.bag_type('abracadabra')
        bag['a'] -= 1
        assert bag == self.bag_type('abracadabr')
        assert bag is bag_reference

        bag = bag_reference = self.bag_type('abracadabra')
        bag['a'] *= 2
        assert bag == self.bag_type('abracadabra' + 'a' * 5)
        assert bag is bag_reference

        bag = bag_reference = self.bag_type('abracadabra')
        with cute_testing.RaiseAssertor(TypeError):
            bag['a'] /= 2 # Won't work because `bag['a']` happens to be odd.

        bag = bag_reference = self.bag_type('abracadabra')
        bag['a'] //= 2
        assert bag == self.bag_type('abracdbr')
        assert bag is bag_reference

        bag = bag_reference = self.bag_type('abracadabra')
        bag['a'] %= 2
        assert bag == self.bag_type('abrcdbr')
        assert bag is bag_reference

        bag = bag_reference = self.bag_type('abracadabra')
        bag['a'] **= 2
        assert bag == self.bag_type('abracadabra' + 'a' * 20)
        assert bag is bag_reference

        bag = bag_reference = self.bag_type('abracadabra')
        bag |= self.bag_type('axyzz')
        assert bag == self.bag_type('abracadabra' + 'xyzz')
        assert bag is bag_reference

        bag = bag_reference = self.bag_type('abracadabra')
        bag &= self.bag_type('axyzz')
        assert bag == self.bag_type('a')
        assert bag is bag_reference

        bag = bag_reference = self.bag_type('abracadabra')
        bag += bag
        assert bag == self.bag_type('abracadabra' * 2)
        assert bag is bag_reference

        bag = bag_reference = self.bag_type('abracadabra')
        bag -= bag
        assert bag == self.bag_type()
        assert bag is bag_reference

        bag = bag_reference = self.bag_type('abracadabra')
        bag *= 2
        assert bag == self.bag_type('abracadabra' * 2)
        assert bag is bag_reference

        # We only allow floor division on bags, not regular divison, because a
        # decimal bag is unheard of.
        bag = bag_reference = self.bag_type('abracadabra')
        with cute_testing.RaiseAssertor(TypeError):
            bag /= 2

        bag = bag_reference = self.bag_type('abracadabra')
        bag //= 2
        assert bag == self.bag_type('aabr')
        assert bag is bag_reference

        bag = bag_reference = self.bag_type('abracadabra')
        bag //= self.bag_type('aabr')
        assert bag == 2
        assert bag is not bag_reference

        bag = bag_reference = self.bag_type('abracadabra')
        bag %= 2
        assert bag == self.bag_type('acd')
        assert bag is bag_reference

        bag = bag_reference = self.bag_type('abracadabra')
        bag %= self.bag_type('aabr')
        assert bag == self.bag_type('acd')
        assert bag is bag_reference

        bag = bag_reference = self.bag_type('abracadabra')
        bag **= 2
        assert bag == self.bag_type('abracadabra' + 'a' * 20 + 'b' * 2 +
                                    'r' * 2)
        assert bag is bag_reference

        bag = bag_reference = self.bag_type('abracadabra')
        bag['a'] = 7
        assert bag == self.bag_type('abracadabra' + 'aa')
        assert bag is bag_reference

        bag = bag_reference = self.bag_type('abracadabra')
        assert bag.setdefault('a', 7) == 5
        assert bag == self.bag_type('abracadabra')
        assert bag is bag_reference

        bag = bag_reference = self.bag_type('abracadabra')
        assert bag.setdefault('x', 7) == 7
        assert bag == self.bag_type('abracadabra' + 'x' * 7)
        assert bag is bag_reference

        bag = bag_reference = self.bag_type('abracadabra')
        assert bag.pop('a', 7) == 5
        assert bag == self.bag_type('brcdbr')
        assert bag.pop('x', 7) == 7
        assert bag == self.bag_type('brcdbr')
        assert bag is bag_reference

        bag = bag_reference = self.bag_type('abracadabra')
        key, value = bag.popitem()
        assert key in 'abracadabra'
        if isinstance(bag, nifty_collections.Ordered):
            assert key == 'd'
        assert bag == self.bag_type([c for c in 'abracadabra' if c != key])
        other_key, other_value = bag.popitem()
        assert other_key in 'abracadabra'
        assert bag == self.bag_type([c for c in 'abracadabra'
                                                 if c not in {key, other_key}])
        assert bag is bag_reference
        if isinstance(bag, nifty_collections.Ordered):
            assert key == 'd'
            assert other_key == 'c'
            first_key, first_value = bag.popitem(last=False)
            assert (first_key, first_value) == ('a', 5)
        else:
            with cute_testing.RaiseAssertor(TypeError):
                bag.popitem(last=False)

        bag = bag_reference = self.bag_type('abracadabra')
        del bag['a']
        assert bag == self.bag_type('brcdbr')

        bag = bag_reference = self.bag_type('abracadabra')
        bag.update(self.bag_type('axy'))
        assert bag == self.bag_type('abrcdbrxy')
        assert bag is bag_reference

    def test_clear(self):
        bag = self.bag_type('meow')
        bag.clear()
        assert not bag
        assert bag == self.bag_type()



class BaseFrozenBagTestCase(BaseBagTestCase):

    def test_get_mutable(self):
        bag = self.bag_type('abracadabra')
        mutable_bag = bag.get_mutable()
        assert not isinstance(mutable_bag, collections.abc.Hashable)
        if isinstance(bag, nifty_collections.Ordered):
            assert tuple(bag.items()) == tuple(mutable_bag.items())
        else:
            assert set(bag.items()) == set(mutable_bag.items())
        assert type(bag).__name__ == f'Frozen{type(mutable_bag).__name__}'
        assert mutable_bag.get_frozen() == bag


    def test_get_frozen(self):
        bag = self.bag_type('abracadabra')
        assert not hasattr(bag, 'get_frozen')
        with cute_testing.RaiseAssertor(AttributeError):
            bag.get_frozen()


    def test_hash(self):
        bag = self.bag_type('abracadabra')
        assert isinstance(bag, collections.abc.Hashable)
        assert issubclass(self.bag_type, collections.abc.Hashable)
        assert {bag, bag} == {bag}
        assert {bag: bag} == {bag: bag}
        assert isinstance(hash(bag), int)


    def test_mutating(self):
        bag = self.bag_type('abracadabra')
        bag_reference = bag
        assert bag is bag_reference

        with cute_testing.RaiseAssertor(TypeError):
            bag['a'] += 1
        with cute_testing.RaiseAssertor(TypeError):
            bag['a'] -= 1
        with cute_testing.RaiseAssertor(TypeError):
            bag['a'] *= 2
        with cute_testing.RaiseAssertor(TypeError):
            bag['a'] /= 2
        with cute_testing.RaiseAssertor(TypeError):
            bag['a'] //= 2
        with cute_testing.RaiseAssertor(TypeError):
            bag['a'] %= 2
        with cute_testing.RaiseAssertor(TypeError):
            bag['a'] **= 2

        bag = bag_reference
        bag |= self.bag_type('axyzz')
        assert bag == self.bag_type('abracadabra' + 'xyzz')
        assert bag is not bag_reference

        bag = bag_reference
        bag &= self.bag_type('axyzz')
        assert bag == self.bag_type('a')
        assert bag is not bag_reference

        bag = bag_reference
        bag += bag
        assert bag == bag_reference * 2
        assert bag is not bag_reference

        bag = bag_reference
        bag -= self.bag_type('ab')
        assert bag == bag_reference - self.bag_type('ab') == \
                                                     self.bag_type('abracadar')
        assert bag is not bag_reference

        bag = bag_reference
        bag *= 3
        assert bag == bag_reference + bag_reference + bag_reference
        assert bag is not bag_reference

        # We only allow floor division on bags, not regular divison, because a
        # decimal bag is unheard of.
        bag = bag_reference
        with cute_testing.RaiseAssertor(TypeError):
            bag /= 2

        bag = bag_reference
        bag //= 3
        assert bag == self.bag_type('a')
        assert bag is not bag_reference

        bag = bag_reference
        bag //= self.bag_type('aabr')
        assert bag == 2
        assert bag is not bag_reference

        bag = bag_reference
        bag %= 2
        assert bag == bag_reference % 2 == self.bag_type('acd')
        assert bag is not bag_reference

        bag = bag_reference
        bag %= self.bag_type('aabr')
        assert bag == self.bag_type('acd')
        assert bag is not bag_reference

        bag = bag_reference
        with cute_testing.RaiseAssertor(TypeError):
            bag['a'] = 7
        with cute_testing.RaiseAssertor(AttributeError):
            bag.setdefault('a', 7)
        with cute_testing.RaiseAssertor(AttributeError):
            bag.pop('a', 7)
        with cute_testing.RaiseAssertor(AttributeError):
            bag.popitem()
        with cute_testing.RaiseAssertor(TypeError):
            del bag['a']
        with cute_testing.RaiseAssertor(AttributeError):
            bag.update(bag)

    def test_clear(self):
        bag = self.bag_type('meow')
        with cute_testing.RaiseAssertor(AttributeError):
            bag.clear()
        assert bag == self.bag_type('meow')




class BaseOrderedBagTestCase(BaseBagTestCase):

    def test_reversed(self):
        bag = self.bag_type('mississippi')

        # Cached only for a frozen type:
        assert (bag.reversed is bag.reversed) == \
               (bag.reversed.reversed is bag.reversed.reversed) == \
               isinstance(bag, collections.abc.Hashable)

        assert bag.reversed == bag.reversed
        assert bag.reversed.reversed == bag.reversed.reversed

        assert Bag(bag) == Bag(bag.reversed)
        assert OrderedBag(bag) != OrderedBag(bag.reversed)

        assert Bag(bag.elements) == Bag(bag.reversed.elements)
        assert OrderedBag(bag.elements) != OrderedBag(bag.reversed.elements)
        assert OrderedBag(bag.elements) == \
                             OrderedBag(reversed(tuple(bag.reversed.elements)))

        assert set(bag.keys()) == set(bag.reversed.keys())
        assert tuple(bag.keys()) == tuple(reversed(tuple(bag.reversed.keys())))

    def test_ordering(self):
        ordered_bag_0 = self.bag_type('ababb')
        ordered_bag_1 = self.bag_type('bbbaa')
        assert ordered_bag_0 == ordered_bag_0
        if issubclass(self.bag_type, collections.abc.Hashable):
            assert hash(ordered_bag_0) == hash(ordered_bag_0)
        assert ordered_bag_1 == ordered_bag_1
        if issubclass(self.bag_type, collections.abc.Hashable):
            assert hash(ordered_bag_1) == hash(ordered_bag_1)
        assert ordered_bag_0 != ordered_bag_1
        assert ordered_bag_0 <= ordered_bag_1
        assert ordered_bag_0 >= ordered_bag_1


    def test_builtin_reversed(self):
        bag = self.bag_type('abracadabra')
        assert tuple(reversed(bag)) == tuple(reversed(tuple(bag)))


    def test_index(self):
        bag = self.bag_type('aaabbc')
        if not isinstance(bag, collections.abc.Hashable):
            bag['d'] = 0
        assert bag.index('a') == 0
        assert bag.index('b') == 1
        assert bag.index('c') == 2
        with cute_testing.RaiseAssertor(ValueError):
            bag.index('d')
        with cute_testing.RaiseAssertor(ValueError):
            bag.index('x')
        with cute_testing.RaiseAssertor(ValueError):
            bag.index(('meow',))



class BaseUnorderedBagTestCase(BaseBagTestCase):

    def test_reversed(self):
        bag = self.bag_type('mississippi')
        with cute_testing.RaiseAssertor(AttributeError):
            bag.reversed


    def test_ordering(self):
        bag_0 = self.bag_type('ababb')
        bag_1 = self.bag_type('bbbaa')
        assert bag_0 == bag_1
        if issubclass(self.bag_type, collections.abc.Hashable):
            assert hash(bag_0) == hash(bag_1)


    def test_builtin_reversed(self):
        bag = self.bag_type('abracadabra')
        with cute_testing.RaiseAssertor(TypeError):
            reversed(bag)


    def test_index(self):
        bag = self.bag_type('aaabbc')
        if not isinstance(bag, collections.abc.Hashable):
            bag['d'] = 0
        with cute_testing.RaiseAssertor(AttributeError):
            bag.index('a')
        with cute_testing.RaiseAssertor(AttributeError):
            bag.index('x')


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

    _repr_result_pattern = ("^OrderedBag\\(OrderedDict\\(\\[\\('a', 2\\), "
                            "\\('b', 3\\)\\]\\)\\)$")

    def test_move_to_end(self):
        bag = self.bag_type('aaabbc')
        bag.move_to_end('c')
        assert FrozenOrderedBag(bag) == FrozenOrderedBag('aaabbc')
        bag.move_to_end('a')
        assert FrozenOrderedBag(bag) == FrozenOrderedBag('bbcaaa')
        bag.move_to_end('c', last=False)
        assert FrozenOrderedBag(bag) == FrozenOrderedBag('cbbaaa')

        with cute_testing.RaiseAssertor(KeyError):
            bag.move_to_end('x')
        with cute_testing.RaiseAssertor(KeyError):
            bag.move_to_end('x', last=False)

    def test_sort(self):
        bag = self.bag_type('aaabbc')
        bag.sort()
        assert FrozenOrderedBag(bag) == FrozenOrderedBag('aaabbc')
        bag.sort(key='cba'.index)
        assert FrozenOrderedBag(bag) == FrozenOrderedBag('cbbaaa')


class FrozenBagTestCase(BaseFrozenBagTestCase, BaseUnorderedBagTestCase):
    __test__ = True
    bag_type = FrozenBag

    _repr_result_pattern = ("^FrozenBag\\({(?:(?:'b': 3, 'a': 2)|"
                            "(?:'a': 2, 'b': 3))}\\)$")

class FrozenOrderedBagTestCase(BaseFrozenBagTestCase,
                               BaseOrderedBagTestCase):
    __test__ = True
    bag_type = FrozenOrderedBag

    _repr_result_pattern = ("^FrozenOrderedBag\\(OrderedDict\\(\\[\\('a', 2\\), "
                            "\\('b', 3\\)\\]\\)\\)$")



class BagTestCaseWithSlowCountElements(BagTestCase):

    def manage_context(self):
        with temp_value_setting.TempValueSetter(
            (nifty_collections.bagging, '_count_elements'),
            nifty_collections.bagging._count_elements_slow):
            yield self
    # Wait, did he just make a test class for the case when the C-optimized
    # counting function isn't available?
    #
    # Yes I did.
    #
    # *Yes.*
    #
    # *I.*
    #
    # *Did.*


