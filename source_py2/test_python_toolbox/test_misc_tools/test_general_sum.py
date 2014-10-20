# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.misc_tools import general_sum


def test():
    assert general_sum((1, 2, 3)) == 6
    assert general_sum((1, 2, 3, 4)) == 10
    assert general_sum(('abra', 'ca', 'dabra')) == 'abracadabra'
    assert general_sum(((0, 1), (0, 2), (0, 3))) == (0, 1, 0, 2, 0, 3)
    
    assert general_sum(((0, 1), (0, 2), (0, 3)), start=(9,)) == (9, 0, 1, 0,
                                                                 2, 0, 3)