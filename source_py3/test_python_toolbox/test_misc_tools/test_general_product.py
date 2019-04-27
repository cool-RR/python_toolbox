# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.misc_tools import general_product


def test():
    assert general_product((1, 2, 3)) == 6
    assert general_product((1, 2, 3, 4)) == 24
    assert general_product(((0, 1), 2, 3)) == (0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0,
                                               1)
    assert general_product((2, 3), start=(0, 1)) == (0, 1, 0, 1, 0, 1, 0, 1, 0,
                                                     1, 0, 1)
