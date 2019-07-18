# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.combi.perming.calculating_length import *

def test_recurrent_perm_space_length():
    assert calculate_length_of_recurrent_perm_space(3, (3, 1, 1)) == 13
    assert calculate_length_of_recurrent_perm_space(2, (3, 2, 2, 1)) == 15
    assert calculate_length_of_recurrent_perm_space(3, (3, 2, 2, 1)) == 52


def test_recurrent_comb_space_length():
    assert calculate_length_of_recurrent_comb_space(3, (3, 1, 1)) == 4
    assert calculate_length_of_recurrent_comb_space(2, (3, 2, 2, 1)) == 9
    assert calculate_length_of_recurrent_comb_space(3, (3, 2, 2, 1)) == 14
