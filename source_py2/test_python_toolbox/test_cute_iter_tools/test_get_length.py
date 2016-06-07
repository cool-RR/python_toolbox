# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `cute_iter_tools.get_length`.'''

from python_toolbox.cute_iter_tools import get_length


def test():
    '''Test the basic workings of `get_length`.'''
    assert get_length(range(3)) == 3
    assert get_length(xrange(4)) == 4
    assert get_length(set(xrange(5))) == 5
    assert get_length(iter(set(xrange(16, 10, -1)))) == 6
    