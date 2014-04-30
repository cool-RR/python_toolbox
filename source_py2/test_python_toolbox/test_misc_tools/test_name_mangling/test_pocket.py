# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.misc_tools import pocket


def test():
    assert pocket() == None
    assert pocket() == None
    assert pocket(7) == None
    assert pocket() == 7
    assert pocket() == 7
    assert pocket(8) == None
    assert pocket() == 8
    assert pocket() == 8
    if pocket(1+1):
        pass
    assert pocket() == 2
