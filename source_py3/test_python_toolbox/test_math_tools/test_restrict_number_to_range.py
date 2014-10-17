# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.


import sys

import nose

from python_toolbox.math_tools import restrict_number_to_range


def test_restrict_number_to_range():
    my_restrict = lambda number: restrict_number_to_range(number, 
                                                          low_cutoff=3.5, 
                                                          high_cutoff=7.8)
    assert list(map(my_restrict, range(10))) == [
        3.5, 3.5, 3.5, 3.5, 4, 5, 6, 7, 7.8, 7.8
    ]