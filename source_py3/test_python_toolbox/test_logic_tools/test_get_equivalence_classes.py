# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import itertools

from python_toolbox import nifty_collections
from python_toolbox.logic_tools import get_equivalence_classes


def test():
    assert get_equivalence_classes([1, 2, 3, 1j, 2j, 3j, 1+1j, 2+2j, 3+3j],
                                   abs) == {
        1: {1, 1j},
        2: {2, 2j},
        3: {3, 3j},
        abs(1 + 1j): {1 + 1j},
        abs(2 + 2j): {2 + 2j},
        abs(3 + 3j): {3 + 3j},
    }


    assert get_equivalence_classes({1: 2, 3: 4, 'meow': 2}) == \
                                                       {2: {1, 'meow'}, 4: {3}}
    
def test_iterable_input():
    assert get_equivalence_classes(range(1, 5), str) == \
                                 {'1': {1}, '2': {2}, '3': {3}, '4': {4},}
    
    assert get_equivalence_classes([1, 2+3j, 4, 5-6j], 'imag') \
                                          == {0: {1, 4}, 3: {2+3j}, -6: {5-6j}}
    
    
def test_big_container():
    # Insertion order:
    
    assert (
        get_equivalence_classes(
            nifty_collections.OrderedDict(((1, 2), (3, 4), ('meow', 2))),
            big_container=nifty_collections.OrderedDict
        ) ==
        get_equivalence_classes(
            nifty_collections.OrderedDict(((1, 2), (3, 4), ('meow', 2))),
            big_container=nifty_collections.OrderedDict()
        ) == nifty_collections.OrderedDict([(2, {1, 'meow'}), (4, {3})])
    )
    
    assert (
        get_equivalence_classes(
            nifty_collections.OrderedDict(((1, 2), (3, 4), ('meow', 2))),
            big_container=dict
        ) == 
        get_equivalence_classes(
            nifty_collections.OrderedDict(((1, 2), (3, 4), ('meow', 2))),
            big_container={}
        ) == {2: {1, 'meow'}, 4: {3}}
    )
    
    assert get_equivalence_classes(
        nifty_collections.OrderedDict((('meow', 2), (1, 2), (3, 4))),
        big_container=nifty_collections.OrderedDict((('foo', 'bar'),))) == \
    nifty_collections.OrderedDict([('foo', 'bar'), (2, {1, 'meow'}), (4, {3})])
    
    assert get_equivalence_classes(
        nifty_collections.OrderedDict(((3, 4), (1, 2), ('meow', 2))),
        big_container=nifty_collections.OrderedDict) == \
    nifty_collections.OrderedDict([(4, {3}), (2, {1, 'meow'})])
    
    assert get_equivalence_classes(
        nifty_collections.OrderedDict(((1, 2), (3, 4), ('meow', 2))),
        small_container=tuple, 
        big_container=nifty_collections.OrderedDict) == \
    nifty_collections.OrderedDict([(2, (1, 'meow')), (4, (3,))])
    
    assert get_equivalence_classes(
        nifty_collections.OrderedDict((('meow', 2), (1, 2), (3, 4))),
        container=tuple, 
        big_container=nifty_collections.FrozenOrderedDict) == \
    nifty_collections.FrozenOrderedDict([(2, ('meow', 1)), (4, (3,))])
    
