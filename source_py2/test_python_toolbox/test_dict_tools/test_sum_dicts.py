# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import dict_tools


def test():
    '''Test the basic workings of `sum_dicts`.'''
    dict_1 = {1: 2, 3: 4, 5: 6,               1j: 1, 2j: 1, 3j: 1,}
    dict_2 = {'a': 'b', 'c': 'd', 'e': 'f',          2j: 2, 3j: 2,}
    dict_3 = {'A': 'B', 'C': 'D', 'E': 'F',                 3j: 3,}
    
    assert dict_tools.sum_dicts((dict_1, dict_2, dict_3)) == {
        1: 2, 3: 4, 5: 6,               
        'a': 'b', 'c': 'd', 'e': 'f',   
        'A': 'B', 'C': 'D', 'E': 'F',
        1j: 1, 2j: 2, 3j: 3,
    }
    
    assert dict_tools.sum_dicts((dict_3, dict_2, dict_1)) == {
        1: 2, 3: 4, 5: 6,               
        'a': 'b', 'c': 'd', 'e': 'f',   
        'A': 'B', 'C': 'D', 'E': 'F',
        1j: 1, 2j: 1, 3j: 1,
    }