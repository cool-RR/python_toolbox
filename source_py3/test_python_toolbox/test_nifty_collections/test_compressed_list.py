# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import sequence_tools

from python_toolbox.nifty_collections import CompressedList


def test():
    original_list = [1, 4, 4, 4, 0, 1, 2, 2, 1, 4, 3, 1, 0, 1, 4, 2, 0, 3, 3,
                     2, 4, 2, 0, 3, 2, 0, 2, 3, 2, 3, 3, 0, 1, 1, 2, 0, 2, 4,
                     3, 1, 3, 0, 0, 3, 0, 1, 4, 1, 4, 4]
    cl = CompressedList(original_list)
    assert set(map(len, map(set, zip(original_list, cl)))) == {1}
    
    print(cl)