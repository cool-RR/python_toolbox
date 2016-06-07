# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import cute_testing
from python_toolbox import sequence_tools

from python_toolbox.combi import *


def test():
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
    repr(~perm_0)
    repr(~perm_1)
    assert (~perm_0, ~perm_1) in product_space
    assert repr(product_space) == (
        '<ProductSpace: 933262154439441526816992388562667004907159682643816214'
        '685929638952175999932299156089414639761565182862536979208272237582511'
        '85210916864000000000000000000000000 * 208755412068>'
    )
    
    assert product_space
    assert not ProductSpace(((),))
    assert not ProductSpace(((), {}))
    with cute_testing.RaiseAssertor(IndexError):
        product_space[product_space.length]
    with cute_testing.RaiseAssertor(IndexError):
        product_space[product_space.length + 7]
    with cute_testing.RaiseAssertor(IndexError):
        product_space[-product_space.length - 1]
    with cute_testing.RaiseAssertor(IndexError):
        product_space[-product_space.length - 100]
    
    # In the following asserts, using `CuteRange` rather than `xrange` because
    # the latter doesn't have a functional `__hash__`.
    
    assert set((
        ProductSpace(
            (sequence_tools.CuteRange(4),
             sequence_tools.CuteRange(3))
        ),
        ProductSpace(
            (sequence_tools.CuteRange(4),
             sequence_tools.CuteRange(3))
        ),
        ProductSpace(
            (sequence_tools.CuteRange(3),
             sequence_tools.CuteRange(4))
        ))) == set((
            ProductSpace(
                (sequence_tools.CuteRange(4),
                 sequence_tools.CuteRange(3))
            ), 
            ProductSpace(
                (sequence_tools.CuteRange(3),
                 sequence_tools.CuteRange(4))
            )
    ))
    
    assert ProductSpace(
        (sequence_tools.CuteRange(4),
         sequence_tools.CuteRange(3))
        ) == ProductSpace(
            (sequence_tools.CuteRange(4),
             sequence_tools.CuteRange(3))
        )
    
    assert ProductSpace(
        (sequence_tools.CuteRange(4),
         sequence_tools.CuteRange(3))) != \
           ProductSpace(
               (sequence_tools.CuteRange(3),
                sequence_tools.CuteRange(4))
           )
    