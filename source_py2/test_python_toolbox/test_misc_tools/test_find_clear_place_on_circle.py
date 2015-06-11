# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import nose.tools

from python_toolbox.misc_tools import find_clear_place_on_circle

def test_wraparound():
    '''Test when clear place is on the wraparound.'''
    result = find_clear_place_on_circle((0.3, 0.5, 0.8), 1)
    nose.tools.assert_almost_equal(result, 0.05)