import math

from python_toolbox import math_tools
from python_toolbox import cute_iter_tools

infinity = float('inf')


class MISSING_ELEMENT: 
    '''blocktotodoc'''
        
        
def get_short_factorial_string(number, minus_one=False):
    '''blocktotodoc'''
    assert number >= 0 and \
                    isinstance(number, math_tools.PossiblyInfiniteIntegral)
    if number == infinity:
        return "float('inf')"
    elif number <= 10:
        return str(math.factorial(number) - int(minus_one))
    else:
        assert number > 10
        return '%s!%s' % (number, ' - 1' if minus_one else '')
        

    