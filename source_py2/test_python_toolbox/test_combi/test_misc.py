# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import cute_testing
from python_toolbox import math_tools

from python_toolbox import combi


def test():
    assert combi.misc.get_short_factorial_string(7) == \
                                                   str(math_tools.factorial(7))
    assert combi.misc.get_short_factorial_string(7, minus_one=True) == \
                                               str(math_tools.factorial(7) - 1)
    
    assert combi.misc.get_short_factorial_string(17) == '17!'
    assert combi.misc.get_short_factorial_string(17, minus_one=True) == \
                                                                      '17! - 1'
    
    assert combi.misc.get_short_factorial_string(float('inf')) == \
                                                             '''float('inf')'''
    assert combi.misc.get_short_factorial_string(float('inf'),
                                          minus_one=True) == '''float('inf')'''

def test_things_in_root_namespace():
    combi.binomial
    combi.Bag
    combi.OrderedBag
    combi.FrozenBag
    combi.FrozenOrderedBag