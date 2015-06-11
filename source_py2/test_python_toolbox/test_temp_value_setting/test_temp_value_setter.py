# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `python_toolbox.temp_value_setting.TempValueSetter`.'''

from python_toolbox import misc_tools
from python_toolbox import cute_testing

from python_toolbox.temp_value_setting import TempValueSetter


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

    
def test_active():
    a = Object()
    a.x = 1
    
    assert a.x == 1
    temp_value_setter = TempValueSetter((a, 'x'), 2)
    assert not temp_value_setter.active
    with temp_value_setter:
        assert a.x == 2
        assert temp_value_setter.active
    assert not temp_value_setter.active
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
    
    
def test_dict_key():
    '''Test `TempValueSetter` with variable inputted as `(dict, key)`.'''
    a = {1: 2}
    
    assert a[1] == 2
    with TempValueSetter((a, 1), 'meow'):
        assert a[1] == 'meow'
    assert a[1] == 2
    
    b = {}
    
    assert sum not in b
    with TempValueSetter((b, sum), 7):
        assert b[sum] == 7
    assert sum not in b

    
def test_as_decorator():
    '''Test `TempValueSetter` used as a decorator.'''
    
    @misc_tools.set_attributes(x=1)
    def a(): pass
    
    @TempValueSetter((a, 'x'), 2)
    def f():
        assert a.x == 2
    assert a.x == 1
    f()
    assert a.x == 1
    
    cute_testing.assert_polite_wrapper(f)