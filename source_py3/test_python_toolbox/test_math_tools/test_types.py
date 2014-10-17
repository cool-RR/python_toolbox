# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.math_tools import (infinity, PossiblyInfiniteIntegral,
                                       PossiblyInfiniteReal)


def test_possibly_infinite_integral():
    matches = [0, 1, -100, 102341, 232, 10 ** 1000, infinity, -infinity,
               True, False]
    non_matches = [0.3, 1j, -100.313, None, 'meow', (1, 2)]
    for match in matches:
        assert isinstance(match, PossiblyInfiniteIntegral)
    for non_match in non_matches:
        assert not isinstance(non_match, PossiblyInfiniteIntegral)
        

def test_possibly_infinite_real():
    matches = [0, 1, -100, 102341, 232, 10 ** 1000, infinity, -infinity,
               0.2, 1.5, -100.7, 102341.345, 232.23424, True, False]
    non_matches = [1j, None, 'meow', (1, 2)]
    for match in matches:
        assert isinstance(match, PossiblyInfiniteReal)
    for non_match in non_matches:
        assert not isinstance(non_match, PossiblyInfiniteReal)
