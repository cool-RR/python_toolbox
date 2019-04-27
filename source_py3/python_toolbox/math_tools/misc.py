# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import numbers
import math
import random

import python_toolbox.cute_enum


infinity = float('inf')
infinities = (infinity, -infinity)


def cute_floor_div(x, y):
    '''
    Get `x // y`, i.e. `x` divided by `y` floored down.

    This differs from Python's built-in `//` in that it handles infinite
    `x`s in a more mathematically correct way: `infinity // 7` would equal
    `infinity`. (Python's built-in `divmod` would make it `nan`.)
    '''

    if ((x in infinities) and (y != 0)) or \
                                   (y in infinities) and (x not in infinities):
        return x / y
    else:
        return x // y


def cute_divmod(x, y):
    '''
    Get the division and modulo for `x` and `y` as a tuple: `(x // y, x % y)`

    This differs from Python's built-in `divmod` in that it handles infinite
    `x`s in a more mathematically correct way: `infinity // 7` would equal
    `infinity`. (Python's built-in `divmod` would make it `nan`.)
    '''
    if (x in infinities) and (y != 0):
        return (x / y, float('nan'))
    elif (y in infinities) and (x not in infinities):
        return (
            x / y,
            x if (get_sign(x) == get_sign(y)) else float('nan')
        )
    else:
        return divmod(x, y)



def get_sign(x):
    '''Get the sign of a number.'''
    if x > 0:
        return 1
    if x == 0:
        return 0
    assert x < 0
    return -1


def round_to_int(x, up=False):
    '''
    Round a number to an `int`.

    This is mostly used for floating points. By default, it will round the
    number down, unless the `up` argument is set to `True` and then it will
    round up.

    If you want to round a number to the closest `int`, just use
    `int(round(x))`.
    '''
    rounded_down = int(cute_floor_div(x, 1))
    if up:
        return int(x) if (isinstance(x, float) and x.is_integer()) \
               else rounded_down + 1
    else:
        return rounded_down

def ceil_div(x, y):
    '''Divide `x` by `y`, rounding up if there's a remainder.'''
    return cute_floor_div(x, y) + (1 if x % y else 0)


def convert_to_base_in_tuple(number, base):
    '''
    Convert a number to any base, returning result in tuple.

    For example, `convert_to_base_in_tuple(32, base=10)` will be `(3, 2)` while
    `convert_to_base_in_tuple(32, base=16)` will be `(2, 0)`.
    '''
    assert isinstance(number, numbers.Integral)
    assert isinstance(base, numbers.Integral)
    assert base >= 2
    sign_ = get_sign(number)
    if sign_ == 0:
        return (0,)
    elif sign_ == -1:
        raise NotImplementedError

    work_in_progress = []
    while number:
        work_in_progress.append(int(number % base))
        number //= base

    return tuple(reversed(work_in_progress))



def restrict_number_to_range(number, low_cutoff=-infinity,
                             high_cutoff=infinity):
    '''
    If `number` is not in the range between cutoffs, return closest cutoff.

    If the number is in range, simply return it.
    '''
    if number < low_cutoff:
        return low_cutoff
    elif number > high_cutoff:
        return high_cutoff
    else:
        return number


def binomial(big, small):
    '''
    Get the binomial coefficient (big small).

    This is used in combinatorical calculations. More information:
    http://en.wikipedia.org/wiki/Binomial_coefficient
    '''
    if big == small:
        return 1
    if big < small:
        return 0
    else:
        return (math.factorial(big) // math.factorial(big - small)
                                                      // math.factorial(small))


def product(numbers):
    '''Get the product of all the numbers in `numbers`.'''
    from python_toolbox import misc_tools
    return misc_tools.general_product(numbers, start=1)


def is_integer(x):
    '''
    Is `x` an integer?

    Does return `True` for things like 1.0 and `1+0j`.
    '''
    try:
        inted_x = int(x)
    except (TypeError, ValueError, OverflowError):
        return False
    return inted_x == x


class RoundMode(python_toolbox.cute_enum.CuteEnum):
    '''
    A mode that determines how `cute_round` will round.

    See documentation of `cute_round` for more info about each of the different
    round modes.
    '''
    CLOSEST_OR_DOWN = 0
    CLOSEST_OR_UP = 1
    ALWAYS_DOWN = 2
    ALWAYS_UP = 3
    PROBABILISTIC = 4

def cute_round(x, round_mode=RoundMode.CLOSEST_OR_DOWN, *, step=1):
    '''
    Round a number, with lots of different options for rounding.

    Basic usage:

        >>> cute_round(7.456)
        7

    The optional `step=1` argument can be changed to change the definition of a
    round number. e.g., if you set `step=100`, then 1234 will be rounded to
    1200. `step` doesn't have to be an integer.

    There are different rounding modes:

        RoundMode.CLOSEST_OR_DOWN

            Default mode: Round to the closest round number. If we're smack in
            the middle, like 4.5, round down to 4.

        RoundMode.CLOSEST_OR_UP

            Round to the closest round number. If we're smack in the middle,
            like 4.5, round up to 5.

        RoundMode.ALWAYS_DOWN

            Always round down. Even 4.99 gets rounded down to 4.

        RoundMode.ALWAYS_UP

            Always round up. Even 4.01 gets rounded up to 5.

        RoundMode.PROBABILISTIC

            Probabilistic round, giving a random result depending on how close
            the number is to each of the two surrounding round numbers. For
            example, if you round 4.5 with this mode, you'll get either 4 or 5
            with an equal probability. If you'll round 4.1 with this mode,
            there's a 90% chance you'll get 4, and a 10% chance you'll get 5.


    '''
    assert step > 0
    div, mod = divmod(x, step)
    if round_mode == RoundMode.CLOSEST_OR_DOWN:
        round_up = (mod > 0.5 * step)
    elif round_mode == RoundMode.CLOSEST_OR_UP:
        round_up = (mod >= 0.5 * step)
    elif round_mode == RoundMode.ALWAYS_DOWN:
        round_up = False
    elif round_mode == RoundMode.ALWAYS_UP:
        round_up = True
    else:
        assert round_mode == RoundMode.PROBABILISTIC
        round_up = random.random() < mod / step
    return (div + round_up) * step

