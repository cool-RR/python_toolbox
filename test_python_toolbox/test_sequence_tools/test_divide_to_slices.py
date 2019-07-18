# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.sequence_tools import divide_to_slices


def test():
    assert divide_to_slices(range(10), 3) == \
                                       [range(0, 4), range(4, 7), range(7, 10)]
