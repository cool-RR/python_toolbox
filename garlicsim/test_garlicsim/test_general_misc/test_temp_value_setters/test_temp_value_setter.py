# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Testing module for `garlicsim.general_misc.temp_value_setters.TempValueSetter`.
'''

from __future__ import with_statement
from garlicsim.general_misc.temp_value_setters import TempValueSetter


class Object(object):
    pass 


def test_simple():
    '''
    Test `TempValueSetter` with variable inputted as `(obj, attribute_name)`.
    '''
    a = Object()
    a.x = 1
    
    assert a.x == 1
    with TempValueSetter((a, 'x'), 2):
        assert a.x == 2
    assert a.x == 1
    

def test_setter_getter():
    '''Test `TempValueSetter` with variable inputted as `(getter, setter)`.'''
    a = Object()
    a.x = 1
    getter = lambda: getattr(a, 'x')
    setter = lambda value: setattr(a, 'x', value)
    
    
    assert a.x == 1
    with TempValueSetter((getter, setter), 2):
        assert a.x == 2
    assert a.x == 1
    

def test_as_decorator():
    '''Test `TempValueSetter` used as a decorator.'''
    def a():
        pass
    a.x = 1
    
    @TempValueSetter((a, 'x'), 2)
    def f():
        assert a.x == 2
    assert a.x == 1
    f()
    assert a.x == 1