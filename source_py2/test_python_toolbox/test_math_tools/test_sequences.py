from python_toolbox.math_tools import abs_stirling


def test_abs_stirling():
    assert tuple(abs_stirling(0, i) for i in range(-1, 2)) == (0, 1, 0, )
    assert tuple(abs_stirling(1, i) for i in range(-1, 3)) == (0, 0, 1, 0, )
    assert tuple(abs_stirling(2, i) for i in range(-1, 4)) == (0, 0, 1, 1, 0)
    assert tuple(abs_stirling(3, i) for i in range(-1, 5)) == (0, 0, 2, 3, 1,
                                                               0)
    assert tuple(abs_stirling(4, i) for i in range(-1, 6)) == (0, 0, 6, 11, 6,
                                                               1, 0)
    assert tuple(abs_stirling(5, i) for i in range(-1, 7)) == (0, 0, 24, 50,
                                                               35, 10, 1, 0)
    
    assert hash(abs_stirling(200, 50)) == 2146881246476041629
    # Doing just hashed comparison because the acutal number is too long. The
    # number was verified with Wolfram Mathematica.


