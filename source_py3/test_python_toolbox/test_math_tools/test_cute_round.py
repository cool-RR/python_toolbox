# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import inspect

from python_toolbox import nifty_collections
from python_toolbox import cute_testing

from python_toolbox.math_tools import cute_round, RoundMode

def almost_equals(x, y):
    return (abs(1-(x / y)) < (10 ** -10))


class CuteRoundTestCase(cute_testing.TestCase):
    def test_closest_or_down(self):
        full_arg_spec = inspect.getfullargspec(cute_round)
        assert RoundMode.CLOSEST_OR_DOWN in full_arg_spec.defaults

        assert almost_equals(cute_round(7.456), 7)
        assert almost_equals(cute_round(7.654), 8)
        assert almost_equals(cute_round(7.5), 7)
        assert almost_equals(cute_round(7.456, step=0.1), 7.5)
        assert almost_equals(cute_round(7.456, step=0.2), 7.4)
        assert almost_equals(cute_round(7.456, step=0.01), 7.46)

    def test_closest_or_up(self):
        assert almost_equals(
            cute_round(7.456, RoundMode.CLOSEST_OR_UP), 7
        )
        assert almost_equals(
            cute_round(7.654, RoundMode.CLOSEST_OR_UP), 8
        )
        assert almost_equals(
            cute_round(7.5, RoundMode.CLOSEST_OR_UP), 8
        )
        assert almost_equals(
            cute_round(7.456, RoundMode.CLOSEST_OR_UP, step=0.1), 7.5
        )
        assert almost_equals(
            cute_round(7.456, RoundMode.CLOSEST_OR_UP, step=0.2), 7.4
        )
        assert almost_equals(
            cute_round(7.456, RoundMode.CLOSEST_OR_UP, step=0.01), 7.46
        )

    def test_always_up(self):
        assert almost_equals(
            cute_round(7.456, RoundMode.ALWAYS_UP), 8
        )
        assert almost_equals(
            cute_round(7.654, RoundMode.ALWAYS_UP), 8
        )
        assert almost_equals(
            cute_round(7.5, RoundMode.ALWAYS_UP), 8
        )
        assert almost_equals(
            cute_round(7.456, RoundMode.ALWAYS_UP, step=0.1), 7.5
        )
        assert almost_equals(
            cute_round(7.456, RoundMode.ALWAYS_UP, step=0.2), 7.6
        )
        assert almost_equals(
            cute_round(7.456, RoundMode.ALWAYS_UP, step=0.01), 7.46
        )

    def test_always_down(self):
        assert almost_equals(
            cute_round(7.456, RoundMode.ALWAYS_DOWN), 7
        )
        assert almost_equals(
            cute_round(7.654, RoundMode.ALWAYS_DOWN), 7
        )
        assert almost_equals(
            cute_round(7.5, RoundMode.ALWAYS_DOWN), 7
        )
        assert almost_equals(
            cute_round(7.456, RoundMode.ALWAYS_DOWN, step=0.1), 7.4
        )
        assert almost_equals(
            cute_round(7.456, RoundMode.ALWAYS_DOWN, step=0.2), 7.4
        )
        assert almost_equals(
            cute_round(7.456, RoundMode.ALWAYS_DOWN, step=0.01), 7.45
        )

    def test_probabilistic(self):
        def get_bag(*args, **kwargs):
            kwargs.update({'round_mode': RoundMode.PROBABILISTIC,})
            return nifty_collections.Bag(
                cute_round(*args, **kwargs) for i in range(1000)
            )

        bag = get_bag(5, step=5)
        assert bag[5] == 1000

        bag = get_bag(6, step=5)
        assert 300 <= bag[5] <= 908
        assert 2 <= bag[10] <= 600

        bag = get_bag(7.5, step=5)
        assert 100 <= bag[5] <= 900
        assert 100 <= bag[10] <= 900

        bag = get_bag(10, step=5)
        assert bag[10] == 1000

