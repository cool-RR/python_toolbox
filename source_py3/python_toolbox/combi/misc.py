import collections
import types
import sys
import math
import numbers

from python_toolbox import dict_tools
from python_toolbox import nifty_collections
from python_toolbox import caching

from layout_rabbit import shy_math_tools
from layout_rabbit import shy_sequence_tools
from layout_rabbit import shy_cute_iter_tools

infinity = float('inf')

        
        
        
def get_short_factorial_string(number, minus_one=False):
    assert number >= 0 and \
                    isinstance(number, shy_math_tools.PossiblyInfiniteIntegral)
    if number == infinity:
        return "float('inf')"
    elif number <= 10:
        return str(math.factorial(number) - int(minus_one))
    else:
        assert number > 10
        return '%s!%s' % (number, ' - 1' if minus_one else '')
        

    