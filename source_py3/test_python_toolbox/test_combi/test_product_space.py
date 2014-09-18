# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.combi import *


def test_product_spaces():
    huge_perm_space = PermSpace(range(100))
    big_perm_space = PermSpace(range(150), fixed_map={1: 5, 70: 3,},
                               degrees=(3, 5))
    product_space = ProductSpace((huge_perm_space, big_perm_space))
    assert product_space.length == \
                                 huge_perm_space.length * big_perm_space.length
    (perm_0, perm_1) = product_space[10**10]
    assert perm_0 in huge_perm_space
    assert perm_1 in big_perm_space
    assert (perm_0, perm_1) in product_space
    assert product_space.index((perm_0, perm_1)) == 10 ** 10
    assert ( ~ perm_0,  ~ perm_1) in product_space
