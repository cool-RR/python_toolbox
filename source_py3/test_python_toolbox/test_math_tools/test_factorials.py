from python_toolbox.math_tools import (inverse_factorial, from_factoradic,
                                       to_factoradic)

def test_inverse_factorial():
    assert inverse_factorial(0, round_up=True) == 0
    assert inverse_factorial(0, round_up=False) == 0
    assert inverse_factorial(1, round_up=True) == 1
    assert inverse_factorial(1, round_up=False) == 1
    assert inverse_factorial(2, round_up=True) == 2
    assert inverse_factorial(2, round_up=False) == 2
    assert inverse_factorial(6, round_up=True) == 3
    assert inverse_factorial(6, round_up=False) == 3
    assert inverse_factorial(24, round_up=True) == 4
    assert inverse_factorial(24, round_up=False) == 4
    
    assert inverse_factorial(25, round_up=True) == 5
    assert inverse_factorial(25, round_up=False) == 4
    assert inverse_factorial(26, round_up=True) == 5
    assert inverse_factorial(26, round_up=False) == 4
    assert inverse_factorial(0.1, round_up=True) == 1
    assert inverse_factorial(0.1, round_up=False) == 0
    assert inverse_factorial(1.1, round_up=True) == 2
    assert inverse_factorial(1.1, round_up=False) == 1


def test_factoradics():
    for i in range(100):
        assert from_factoradic(to_factoradic(i)) == i
    assert tuple(map(to_factoradic, range(10))) == (
        (0,), (1, 0,), (1, 0, 0), (1, 1, 0), (2, 0, 0), (2, 1, 0),
        (1, 0, 0, 0), (1, 0, 1, 0), (1, 1, 0, 0), (1, 1, 1, 0)
    )

