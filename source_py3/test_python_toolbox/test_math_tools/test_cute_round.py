# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.math_tools import cute_round

def almost_equals(x, y):
    return (abs(1-(x / y)) < (10 ** -10))
    

def test_cute_round():
    assert almost_equals(cute_round(7.456), 7)
    assert almost_equals(cute_round(7.456, up=True), 8)
    assert almost_equals(cute_round(7.456, step=0.1), 7.4)
    assert almost_equals(cute_round(7.456, step=0.1, up=True), 7.5)
    assert almost_equals(cute_round(7.456, step=0.2), 7.4)
    assert almost_equals(cute_round(7.456, step=0.2, up=True), 7.6)
    assert almost_equals(cute_round(7.456, step=0.01), 7.45)
    assert almost_equals(cute_round(7.456, step=0.01, up=True), 7.46)
