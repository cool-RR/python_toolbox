# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import pytest

from python_toolbox import nifty_collections
from python_toolbox import cute_iter_tools
from python_toolbox.cute_iter_tools import is_sorted


infinity = float('inf')


def test():
    r = (1, 2, 3, 7, 10)
    assert is_sorted(r) is True
    assert is_sorted(r, rising=False) is False
    assert is_sorted(r[::-1], rising=False) is True
    assert is_sorted(r, strict=True) is True
    assert is_sorted(r, rising=False, strict=True) is False
    assert is_sorted(r, key=lambda x: x % 3) is False
    assert is_sorted(r, rising=False, key=lambda x: x % 3) is False
    assert is_sorted(r, key=lambda x: -x) is False
    assert is_sorted(r, rising=False, key=lambda x: -x) is True
    assert is_sorted(r, rising=False, strict=True, key=lambda x: -x) is True
