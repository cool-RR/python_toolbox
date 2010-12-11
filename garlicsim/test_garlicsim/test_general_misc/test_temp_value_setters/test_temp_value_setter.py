from __future__ import with_statement
from garlicsim.general_misc.temp_value_setters import TempValueSetter


class Object(object):
    pass


def test_simple():
    a = Object()
    a.x = 1
    
    assert a.x == 1
    with TempValueSetter((a, 'x'), 2):
        assert a.x == 2
    assert a.x == 1
    

def test_setter_getter():
    a = Object()
    a.x = 1
    getter = lambda: getattr(a, 'x')
    setter = lambda value: setattr(a, 'x', value)
    
    
    assert a.x == 1
    with TempValueSetter((getter, setter), 2):
        assert a.x == 2
    assert a.x == 1