# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `string_tools.get_n_identical_edge_characters`.'''

from python_toolbox.string_tools import get_n_identical_edge_characters


def test():
    '''Test the basics of `get_n_identical_edge_characters`.'''
    assert get_n_identical_edge_characters('qqqwee') == 3
    assert get_n_identical_edge_characters('qqqqwee') == 4
    assert get_n_identical_edge_characters('qqqqwee', head=False) == 2
    assert get_n_identical_edge_characters('1234') == 1
    assert get_n_identical_edge_characters('1234', character='4') == 0
    assert get_n_identical_edge_characters('1234',
                                           character='4',
                                           head=False) == 1
    assert get_n_identical_edge_characters('1234',
                                           character='&',
                                           head=False) == 0
    assert get_n_identical_edge_characters('pppp') == \
           get_n_identical_edge_characters('pppp', head=False) == \
           get_n_identical_edge_characters('pppp', character='p',
                                           head=False) == 4