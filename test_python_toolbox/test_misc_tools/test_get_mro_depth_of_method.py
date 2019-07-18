# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox.misc_tools import get_mro_depth_of_method


def test():
    '''Test the basic workings of `get_mro_depth_of_method`.'''
    class A:
        def a_method(self):
            pass

    class B(A):
        def b_method(self):
            pass

    class C(A):
        def c_method(self):
            pass

    class D:
        def d_method(self):
            pass

    class E(B, D, C):
        def e_method(self):
            pass

    assert get_mro_depth_of_method(A, 'a_method') == 0

    assert get_mro_depth_of_method(B, 'a_method') == 1
    assert get_mro_depth_of_method(B, 'b_method') == 0

    assert get_mro_depth_of_method(C, 'a_method') == 1
    assert get_mro_depth_of_method(C, 'c_method') == 0

    assert get_mro_depth_of_method(D, 'd_method') == 0

    assert get_mro_depth_of_method(E, 'e_method') == 0
    assert get_mro_depth_of_method(E, 'b_method') == 1
    assert get_mro_depth_of_method(E, 'd_method') == 2
    assert get_mro_depth_of_method(E, 'c_method') == 3
    assert get_mro_depth_of_method(E, 'a_method') == 4
