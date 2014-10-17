# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import sys

import nose

from python_toolbox.math_tools import get_mean


def test_mean():
    assert get_mean((1, 2, 3)) == 2
    assert get_mean((1, 2, 3, 4)) == 2.5
    assert get_mean((1, 2, 3, 4, 5)) == 3
    assert get_mean((-1, -2, -3, -4, -5)) == -3
    assert get_mean((-0.5, -2, -3, -4, -5.5)) == -3
    assert 1821.666 < get_mean((1000, 10000.5, -2, -4, -14, -50.5)) < 1821.667