# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import numbers
import math

from python_toolbox import cute_testing

from python_toolbox.math_tools import cute_floor_div, cute_divmod
from python_toolbox import logic_tools
from python_toolbox import math_tools

infinity = float('inf')
infinities = (infinity, -infinity)


def cute_equal(*items):
    # For testing purposes, we need `nan == nan`, so we use `cute_equal`.
    if all(isinstance(item, numbers.Number) for item in items):
        if all(map(math.isnan, items)): return True
        else: return logic_tools.all_equivalent(items)
    else:
        assert all(isinstance(item, tuple) for item in items)
        return all(cute_equal(*sub_items) for sub_items in zip(*items))


def test_degenerate_cases():
    degenerate_cases = (
        (4, 5), (-1234, 23), (0, 512), (452.5, 613.451), (234.234, -3453),
        (-23.3, 4), (infinity, infinity), (infinity, -infinity),
        (-infinity, infinity), (-infinity, -infinity)
    )
    for degenerate_case in degenerate_cases:
        assert cute_equal(cute_divmod(*degenerate_case),
                          divmod(*degenerate_case))
        assert cute_equal(cute_divmod(*degenerate_case)[0],
                          cute_floor_div(*degenerate_case),
                          degenerate_case[0] // degenerate_case[1])


def test_illegal_cases():
    illegal_cases = (
        (4, 0), (infinity, 0), (-infinity, 0)
    )
    for illegal_case in illegal_cases:
        with cute_testing.RaiseAssertor() as raise_assertor_0:
            cute_divmod(*illegal_case)
        with cute_testing.RaiseAssertor() as raise_assertor_1:
            divmod(*illegal_case)
        with cute_testing.RaiseAssertor() as raise_assertor_2:
            cute_floor_div(*illegal_case)
        assert logic_tools.all_equivalent((
            type(raise_assertor_0.exception),
            type(raise_assertor_1.exception),
            type(raise_assertor_2.exception),
        ))
    
        
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
        assert cute_equal(cute_quotient,
                          cute_floor_div(meaningful_numerator,
                                         meaningful_denominator))
        assert (cute_quotient ==
                          (meaningful_numerator / meaningful_denominator)) or \
        (0 <= ((meaningful_numerator / meaningful_denominator)
                                                          - cute_quotient) < 1)
        

    