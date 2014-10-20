# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from __future__ import division

from python_toolbox import cute_iter_tools


def test():
    ratio = cute_iter_tools.get_ratio('real', [1, 2, 3, 1j, 2j, 3j, 4j])
    assert ratio == 3 / 7