# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

import numbers

from python_toolbox import cute_testing

from python_toolbox.math_tools import cute_divmod
from python_toolbox import math_tools


infinity = float('inf')
infinities = (infinity, -infinity)

def cute_equal(x, y):
    # For testing purposes, we need `nan == nan`, so we use `cute_equal`.
    if (isinstance(x, numbers.Number) and isinstance(y, numbers.Number)):
        if (x is float('nan')) and (y is float('nan')): return True
        else: return x == y
    else:
        assert (isinstance(x, tuple) and isinstance(y, tuple))
        return all(cute_equal(xx, yy) for xx, yy in zip(x, y))

def test_degenerate_cases():
    degenerate_cases = (
        (4, 5), (-1234, 23), (0, 512), (452.5, 613.451), (234.234, -3453),
        (-23.3, 4), (infinity, infinity), (infinity, -infinity),
        (-infinity, infinity), (-infinity, -infinity)
    )
    for degenerate_case in degenerate_cases:
        assert cute_equal(cute_divmod(*degenerate_case),
                          divmod(*degenerate_case))


def test_illegal_cases():
    illegal_cases = (
        (4, 0), (infinity, 0), (-infinity, 0)
    )
    for illegal_case in illegal_cases:
        with cute_testing.RaiseAssertor() as raise_assertor_0:
            cute_divmod(*illegal_case)
        with cute_testing.RaiseAssertor() as raise_assertor_1:
            divmod(*illegal_case)
        assert raise_assertor_0.exception == raise_assertor_1.exception
    
        
def test_meaningful_cases():
    meaningful_cases = (
        (infinity, 3), (infinity, 300.5), (infinity, -3), (infinity, -300.5), 
        (-infinity, 3), (-infinity, 300.5), (-infinity, -3), (-infinity, -300.5), 
        (3, infinity), (3, -infinity), (-3, infinity), (-3, -infinity), 
        (300.5, infinity), (300.5, -infinity),
                                       (-300.5, infinity), (-300.5, -infinity),
        (0, infinity), (0, -infinity),
    )
    for meaningful_numerator, meaningful_denominator in meaningful_cases:
        cute_quotient, cute_remainder = cute_divmod(meaningful_numerator,
                                                    meaningful_denominator)
        regular_quotient, regular_remainder = divmod(meaningful_numerator,
                                                     meaningful_denominator)
        assert not cute_equal((cute_quotient, cute_remainder), 
                              (regular_quotient, regular_remainder))
        assert cute_quotient == math_tools.round_to_int(
            meaningful_numerator / meaningful_denominator,
        )

    