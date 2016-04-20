# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import inspect

from python_toolbox.math_tools import cute_round, RoundMode

def almost_equals(x, y):
    return (abs(1-(x / y)) < (10 ** -10))
    

class CuteRoundTestCase:
    def test_closest_or_down(self):
        full_arg_spec = inspect.getfullargspec(cute_round)
        assert RoundMode.CLOSEST_OR_DOWN in full_arg_spec.defaults
                                                          
        assert almost_equals(cute_round(7.456), 7)
        assert almost_equals(cute_round(7.654), 8)
        assert almost_equals(cute_round(7.5), 7)
        assert almost_equals(cute_round(7.456, step=0.1), 7.5)
        assert almost_equals(cute_round(7.456, step=0.2), 7.4)
        assert almost_equals(cute_round(7.456, step=0.01), 7.46)
