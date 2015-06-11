# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

import nose.tools

from python_toolbox import cute_testing

from python_toolbox.misc_tools import limit_positional_arguments


def test():
    def f(x=1, y=2, z=3):
        return (x, y, z)
    
    assert f() == (1, 2, 3)
    assert f(4, 5, 6) == (4, 5, 6)
    
    @limit_positional_arguments(2)
    def g(x=1, y=2, z=3):
        return (x, y, z)
    
    assert g('a', 'b') == ('a', 'b', 3)
    
    with cute_testing.RaiseAssertor(TypeError):
        g('a', 'b', 'c')
          
    assert g('a', 'b', z='c') == ('a', 'b', 'c')
    assert g(x='a', y='b', z='c') == ('a', 'b', 'c')
    