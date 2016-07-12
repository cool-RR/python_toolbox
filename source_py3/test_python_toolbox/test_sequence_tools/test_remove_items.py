# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import cute_testing
from python_toolbox import sequence_tools

from python_toolbox.sequence_tools import remove_items

def test():
    x = list(range(10))
    remove_items(range(4, 8), x)
    assert x == [0, 1, 2, 3, 8, 9]
    
    x = list(range(10))
    remove_items(range(4, 8), x, assert_contained_first=True)
    assert x == [0, 1, 2, 3, 8, 9]