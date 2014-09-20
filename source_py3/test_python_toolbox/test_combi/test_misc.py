# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import cute_testing
from python_toolbox import math_tools

from python_toolbox.combi import *


def test():
    assert misc.get_short_factorial_string(7) == str(math_tools.factorial(7))
    assert misc.get_short_factorial_string(7, minus_one=True) == \
                                               str(math_tools.factorial(7) - 1)
    
    assert misc.get_short_factorial_string(17) == '17!'
    assert misc.get_short_factorial_string(17, minus_one=True) == '17! - 1'
    
    assert misc.get_short_factorial_string(float('inf')) == '''float('inf')'''
    assert misc.get_short_factorial_string(float('inf'),
                                          minus_one=True) == '''float('inf')'''
