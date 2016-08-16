# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import collections.abc

from python_toolbox.third_party import unittest2

import nose

from python_toolbox import cute_iter_tools
from python_toolbox import cute_testing

from python_toolbox import nifty_collections
from python_toolbox.nifty_collections import (
    DoubleDict, FrozenDict, OrderedDict,
    DoubleFrozenDict, DoubleOrderedDict,
    FrozenOrderedDict, DoubleFrozenOrderedDict
)

from abstract_one_base_test_cases import *


###############################################################################


class AbstractDoubleFrozenDictTestCase(AbstractDoubleDictTestCase, 
                                       AbstractFrozenDictTestCase):
    pass


class AbstractDoubleNotFrozenDictTestCase(AbstractDoubleDictTestCase,
                                          AbstractNotFrozenDictTestCase):
    def test_changing_affects_inverse(self):
        d = self.d_type(((1, 2), (3, 4), (5, 6)))
        inverse = d.inverse
        assert len(d) == len(inverse) == 3

        d[7] = 8
        assert inverse[8] == 7
        assert len(d) == len(inverse) == 4
        
        del d[3]
        assert len(d) == len(inverse) == 3
        assert '4' not in inverse
        
        d.clear()
        assert len(d) == len(inverse) == 0
        assert '2' not in inverse
        
    def test_del_key_error(self):
        d = self.d_type(((1, 2), (3, 4), (5, 6)))
        del d[1]
        with cute_testing.RaiseAssertor(KeyError):
            del d[1]
        with cute_testing.RaiseAssertor(KeyError):
            del d['woof']
        


class AbstractNotDoubleFrozenDictTestCase(AbstractFrozenDictTestCase,
                                          AbstractNotDoubleDictTestCase):
    pass


class AbstractNotDoubleNotFrozenDictTestCase(AbstractNotDoubleDictTestCase,
                                             AbstractNotFrozenDictTestCase):
    pass


###############################################################################


class AbstractDoubleOrderedDictTestCase(AbstractDoubleDictTestCase,
                                        AbstractOrderedDictTestCase):
    def test_double_ordered_without_modifying(self):
        d = self.make_big_dict()
        assert tuple(d.inverse.keys()) == tuple(d.values())
        assert tuple(d.inverse.values()) == tuple(d.keys())
        
        some_pair = tuple(d.items())[47]
        assert d.index(some_pair[0]) == 47
        assert d.inverse.index(some_pair[1]) == 47
        

class AbstractDoubleNotOrderedDictTestCase(AbstractDoubleDictTestCase,
                                           AbstractNotOrderedDictTestCase):
    pass


class AbstractNotDoubleOrderedDictTestCase(AbstractOrderedDictTestCase,
                                           AbstractNotDoubleDictTestCase):
    pass


class AbstractNotDoubleNotOrderedDictTestCase(AbstractNotDoubleDictTestCase,
                                              AbstractNotOrderedDictTestCase):
    pass


###############################################################################


class AbstractFrozenOrderedDictTestCase(AbstractFrozenDictTestCase,
                                        AbstractOrderedDictTestCase):
    pass


class AbstractFrozenNotOrderedDictTestCase(AbstractFrozenDictTestCase,
                                           AbstractNotOrderedDictTestCase):
    pass


class AbstractNotFrozenOrderedDictTestCase(AbstractOrderedDictTestCase,
                                           AbstractNotFrozenDictTestCase):
    def test_move_to_end(self):
        d = self.d_type(((1, 2), (3, 4), (5, 6)))
        assert tuple(d.items()) == ((1, 2), (3, 4), (5, 6))
        assert d.index(3) == 1
        assert tuple(d) == (1, 3, 5)
        
        d.move_to_end(3)
        assert tuple(d.items()) == ((1, 2), (5, 6), (3, 4))
        assert d.index(3) == 2
        assert tuple(d) == (1, 5, 3)
        
        assert d.index(5) == 1
        d.move_to_end(5, last=False)
        assert tuple(d.items()) == ((5, 6), (1, 2), (3, 4))
        assert d.index(5) == 0
        assert tuple(d) == (5, 1, 3)
        
    def test_new_item_at_end(self):
        d = self.d_type(((1, 2), (5, 6)))
        d[3] = 4
        assert tuple(d.items()) == ((1, 2), (5, 6), (3, 4))

    def test_new_item_at_end(self):
        d = self.d_type(((1, 2), (5, 6), (3, 4)))
        d.sort()
        assert tuple(d.items()) == ((1, 2), (3, 4), (5, 6))
        d.sort(reverse=True)
        assert tuple(d.items()) == ((5, 6), (3, 4), (1, 2))


class AbstractNotFrozenNotOrderedDictTestCase(AbstractNotFrozenDictTestCase,
                                              AbstractNotOrderedDictTestCase):
    pass


