# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Test module for `binary_search`.'''

from python_toolbox import binary_search
from python_toolbox import nifty_collections
from python_toolbox import misc_tools


def test():
    '''Test the basic workings of `binary_search`.'''
    my_list = [0, 1, 2, 3, 4]

    assert binary_search.binary_search(
        my_list,
        3,
        misc_tools.identity_function,
        binary_search.EXACT
    ) == 3

    assert binary_search.binary_search(
        my_list,
        3.2,
        misc_tools.identity_function,
        binary_search.CLOSEST
    ) == 3

    assert binary_search.binary_search(
        my_list,
        3.2,
        misc_tools.identity_function,
        binary_search.LOW
    ) == 3

    assert binary_search.binary_search(
        my_list,
        3.2,
        misc_tools.identity_function,
        binary_search.HIGH
    ) == 4

    assert binary_search.binary_search(
        my_list,
        3.2,
        misc_tools.identity_function,
        binary_search.BOTH
    ) == (3, 4)

    assert binary_search.binary_search(
        my_list,
        -5,
        misc_tools.identity_function,
        binary_search.BOTH
    ) == (None, 0)

    assert binary_search.binary_search(
        my_list,
        -5,
        misc_tools.identity_function,
        binary_search.LOW
    ) == None

    assert binary_search.binary_search(
        my_list,
        -5,
        misc_tools.identity_function,
        binary_search.HIGH
    ) == 0

    assert binary_search.binary_search(
        my_list,
        -5,
        misc_tools.identity_function,
        binary_search.HIGH_OTHERWISE_LOW
    ) == 0

    assert binary_search.binary_search(
        my_list,
        -5,
        misc_tools.identity_function,
        binary_search.LOW_OTHERWISE_HIGH
    ) == 0

    assert binary_search.binary_search(
        my_list,
        100,
        misc_tools.identity_function,
        binary_search.BOTH
    ) == (4, None)

    assert binary_search.binary_search(
        my_list,
        100,
        misc_tools.identity_function,
        binary_search.LOW
    ) == 4

    assert binary_search.binary_search(
        my_list,
        100,
        misc_tools.identity_function,
        binary_search.HIGH
    ) == None

    assert binary_search.binary_search(
        my_list,
        100,
        misc_tools.identity_function,
        binary_search.LOW_OTHERWISE_HIGH
    ) == 4

    assert binary_search.binary_search(
        my_list,
        100,
        misc_tools.identity_function,
        binary_search.HIGH_OTHERWISE_LOW
    ) == 4

    assert binary_search.binary_search_by_index(
        [(number * 10) for number in my_list],
        32,
        misc_tools.identity_function,
        binary_search.BOTH
    ) == (3, 4)

    assert binary_search.binary_search(
        [],
        32,
        misc_tools.identity_function,
        binary_search.BOTH
    ) == (None, None)

    assert binary_search.binary_search(
        [],
        32,
        misc_tools.identity_function,
    ) == None


def test_single_member():

    assert binary_search.binary_search(
        [7],
        7,
        misc_tools.identity_function,
        binary_search.LOW
    ) == 7

    assert binary_search.binary_search(
        [7],
        7,
        misc_tools.identity_function,
        binary_search.HIGH
    ) == 7

    assert binary_search.binary_search(
        [7],
        7,
        misc_tools.identity_function,
        binary_search.HIGH_IF_BOTH
    ) == 7

    assert binary_search.binary_search(
        [7],
        7,
        misc_tools.identity_function,
        binary_search.LOW_IF_BOTH
    ) == 7

    assert binary_search.binary_search(
        [7],
        7,
        misc_tools.identity_function,
        binary_search.EXACT
    ) == 7

    assert binary_search.binary_search(
        [7],
        7,
        misc_tools.identity_function,
        binary_search.BOTH
    ) == (7, 7)

    assert binary_search.binary_search(
        [7],
        7,
        misc_tools.identity_function,
        binary_search.CLOSEST
    ) == 7

    assert binary_search.binary_search(
        [7],
        7,
        misc_tools.identity_function,
        binary_search.CLOSEST_IF_BOTH
    ) == 7

    assert binary_search.binary_search(
        [7],
        7,
        misc_tools.identity_function,
        binary_search.LOW_OTHERWISE_HIGH
    ) == 7

    assert binary_search.binary_search(
        [7],
        7,
        misc_tools.identity_function,
        binary_search.HIGH_OTHERWISE_LOW
    ) == 7
