# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `cute_iter_tools.enumerate`.'''


from python_toolbox import nifty_collections
from python_toolbox import cute_iter_tools


def test():
    '''Test the basic workings of `cute_iter_tools.enumerate`.'''

    for i, j in cute_iter_tools.enumerate(range(5)):
        assert i == j

    for i, j in cute_iter_tools.enumerate(range(5), reverse_index=True):
        assert i + j == 4

    for i, j in cute_iter_tools.enumerate(range(4, -1, -1), reverse_index=True):
        assert i == j

    lazy_tuple = cute_iter_tools.enumerate(range(4, -1, -1), reverse_index=True,
                                           lazy_tuple=True)

    assert isinstance(lazy_tuple, nifty_collections.LazyTuple)
    assert not lazy_tuple.collected_data

    for i, j in lazy_tuple:
        assert i == j

    assert lazy_tuple.is_exhausted