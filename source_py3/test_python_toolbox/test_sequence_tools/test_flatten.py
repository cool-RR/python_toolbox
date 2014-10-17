# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `sequence_tools.flatten`.'''

from python_toolbox.sequence_tools import flatten


def test():
    '''Test the basic workings of `sequence_tools.flatten`.'''
    assert flatten([]) == flatten(()) == []
    assert flatten([[1], [2], [3]]) == flatten(([1], [2], [3])) == [1, 2, 3]
    assert flatten(((1,), (2,), (3,))) == flatten([(1,), (2,), (3,)]) == \
           (1, 2, 3)