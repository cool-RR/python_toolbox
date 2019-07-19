# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `python_toolbox.math_tools.convert_to_base_in_tuple`.'''

import sys

from python_toolbox.math_tools import convert_to_base_in_tuple
from python_toolbox import cute_testing


def test():
    assert convert_to_base_in_tuple(51346616, 16) == (3, 0, 15, 7, 12, 11, 8)
    assert convert_to_base_in_tuple(2341263462323, 2) == (
        1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1,
        1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1
    )



def test_trivial():
    assert convert_to_base_in_tuple(0, 2) == \
           convert_to_base_in_tuple(0, 10) == \
           convert_to_base_in_tuple(0, 16) == \
           convert_to_base_in_tuple(0, 23423) == (0,)
    assert convert_to_base_in_tuple(1, 2) == \
           convert_to_base_in_tuple(1, 10) == \
           convert_to_base_in_tuple(1, 16) == \
           convert_to_base_in_tuple(1, 23423) == (1,)
    assert convert_to_base_in_tuple(7, 10) == \
           convert_to_base_in_tuple(7, 16) == \
           convert_to_base_in_tuple(7, 23423) == (7,)


def test_negative():
    with cute_testing.RaiseAssertor(NotImplementedError):
        convert_to_base_in_tuple(-1, 7)
    with cute_testing.RaiseAssertor(NotImplementedError):
        convert_to_base_in_tuple(-13462, 4)
    with cute_testing.RaiseAssertor(NotImplementedError):
        convert_to_base_in_tuple(-23451759010224, 11)
