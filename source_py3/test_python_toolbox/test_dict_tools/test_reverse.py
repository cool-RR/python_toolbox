# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Test package for `dict_tools.devour_items`.'''

from python_toolbox import dict_tools


def test():
    '''Test the basic workings of `devour_items`.'''
    my_dict = {1: 2, 3: 4, 5: 6,}
    assert set(dict_tools.devour_items(my_dict)) == {(1, 2), (3, 4), (5, 6)}
    assert not my_dict
    