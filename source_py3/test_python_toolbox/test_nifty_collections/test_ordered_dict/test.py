# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `nifty_collections.ordered_dict.OrderedDict`.'''

from python_toolbox import cute_testing

from python_toolbox.nifty_collections.ordered_dict import OrderedDict


def test_sort():
    '''Test the `OrderedDict.sort` method.'''
    ordered_dict = OrderedDict(((1, 'a'), (2, 'b'), (3, 'c')))
    ordered_dict_copy = ordered_dict.copy()
    assert ordered_dict == ordered_dict_copy
    ordered_dict.sort()
    assert ordered_dict == ordered_dict_copy

    ordered_dict_copy.sort(key=(lambda x: -x))
    assert ordered_dict != ordered_dict_copy
    assert ordered_dict == dict(ordered_dict) == ordered_dict_copy

    ordered_dict[4] = ordered_dict_copy[4] = 'd'
    assert ordered_dict != ordered_dict_copy
    assert ordered_dict == dict(ordered_dict) == ordered_dict_copy

    ordered_dict_copy.sort(key=ordered_dict_copy.__getitem__)
    assert ordered_dict == ordered_dict_copy

    ordered_dict_copy.sort(key=(lambda x: -x))
    assert ordered_dict != ordered_dict_copy
    assert ordered_dict == dict(ordered_dict) == ordered_dict_copy

    ordered_dict.sort(key=(lambda x: -x))
    assert ordered_dict == ordered_dict_copy


    second_ordered_dict = OrderedDict(((1+2j, 'b'), (2+3j, 'c'), (3+1j, 'a')))
    second_ordered_dict.sort('imag')
    assert second_ordered_dict == \
                           OrderedDict(((3+1j, 'a'), (1+2j, 'b'), (2+3j, 'c')))

    second_ordered_dict.sort('real', reverse=True)
    assert second_ordered_dict == \
                           OrderedDict(((3+1j, 'a'), (2+3j, 'c'), (1+2j, 'b')))



def test_index():
    '''Test the `OrderedDict.index` method.'''
    ordered_dict = OrderedDict(((1, 'a'), (2, 'b'), (3, 'c')))
    assert ordered_dict.index(1) == 0
    assert ordered_dict.index(3) == 2
    assert ordered_dict.index(2) == 1

    ordered_dict[2] = 'b'

    assert ordered_dict.index(1) == 0
    assert ordered_dict.index(3) == 2
    assert ordered_dict.index(2) == 1

    ordered_dict['meow'] = 'frr'

    assert ordered_dict.index('meow') == 3

    with cute_testing.RaiseAssertor(ValueError):
        ordered_dict.index('Non-existing key')


def test_builtin_reversed():
    '''Test the `OrderedDict.__reversed__` method.'''

    ordered_dict = OrderedDict(((1, 'a'), (2, 'b'), (3, 'c')))
    assert list(reversed(ordered_dict)) == [3, 2, 1]

def test_reversed():
    ordered_dict = OrderedDict(((1, 'a'), (2, 'b'), (3, 'c')))
    assert ordered_dict.reversed == OrderedDict(((3, 'c'), (2, 'b'), (1, 'a')))
    assert type(ordered_dict.reversed) is type(ordered_dict) is OrderedDict