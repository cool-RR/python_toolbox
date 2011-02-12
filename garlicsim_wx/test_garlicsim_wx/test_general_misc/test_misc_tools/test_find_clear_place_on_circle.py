# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `find_clear_place_on_circle`.'''

from garlicsim_wx.general_misc.misc_tools import find_clear_place_on_circle

def test_wraparound():
    result = find_clear_place_on_circle((0.3, 0.5, 0.8), 1)
    assert result == 0.05