# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import sys

import pytest

from python_toolbox.math_tools import get_median


def test_median():
    assert get_median((1, 2, 3)) == 2
    assert get_median((1, 2, 3, 4)) == 2.5
    assert get_median((1, 2, 3, 4, 5)) == 3
    assert get_median((-1, -2, -3, -4, -5)) == -3
    assert get_median((-0.5, -2, -3, -4, -5.5)) == -3
    assert get_median((-0.5, -2, -3, -4, -50.5)) == -3
    assert get_median((10000.5, -2, -3, -14, -50.5)) == -3
    assert get_median((10000.5, -2, -4, -14, -50.5)) == -4
    assert get_median((1000, 1000, 10000.5, -2, -4, -14, -50.5)) == -2