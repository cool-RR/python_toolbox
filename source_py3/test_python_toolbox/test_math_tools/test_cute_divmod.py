# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import cute_testing

from python_toolbox.math_tools import cute_divmod


def test_degenerate_cases():
    degenerate_cases = (
        (4, 5), (-1234, 23), (0, 512), (452.5, 613.451), (234.234, -3453),
        (-23.3, 4)
    )
    for degenerate_case in degenerate_cases:
        assert cute_divmod(*degenerate_case) == divmod(*degenerate_case)
        
    
    illegal_cases
    
    