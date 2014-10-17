# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import cute_testing

from python_toolbox.misc_tools import repeat_getattr


class Object:
    def __init__(self, tag):
        self.tag = tag
    __eq__ = lambda self, other: (self.tag == other.tag)
        

x = Object('x')
x.y = Object('y')
x.y.z = Object('z')
x.y.meow = Object('meow')
        

def test():
    assert repeat_getattr(x, None) == repeat_getattr(x, '') == x
    with cute_testing.RaiseAssertor():
        repeat_getattr(x, 'y')
        
    assert x != x.y != x.y.z != x.y.meow
    assert repeat_getattr(x, '.y') == x.y
    assert repeat_getattr(x, '.y.z') == x.y.z
    assert repeat_getattr(x, '.y.meow') == x.y.meow
    
    assert repeat_getattr(x.y, '.meow') == x.y.meow
    assert repeat_getattr(x.y, '.z') == x.y.z