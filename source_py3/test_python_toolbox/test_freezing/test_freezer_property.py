# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for `freezing.FreezerProperty`.'''

from python_toolbox.freezing import FreezerProperty, Freezer
from python_toolbox import caching


def test_lone_freezer_property():
    '''Test a class that has only one freezer property without handlers.'''
    
    class A:
        lone_freezer = FreezerProperty()

    a = A()
    assert isinstance(a.lone_freezer, Freezer)
    assert a.lone_freezer.frozen == 0
    with a.lone_freezer:
        assert a.lone_freezer.frozen
        
    
def test_decorate_happy_freezer_property():
    '''Test a freezer property which decorates both handlers.'''
    class C:
        decorate_happy_freeze_counter = caching.CachedProperty(0)
        decorate_happy_thaw_counter = caching.CachedProperty(0)
        decorate_happy_freezer = FreezerProperty()
        @decorate_happy_freezer.on_freeze
        def increment_decorate_happy_freeze_counter(self):
            self.decorate_happy_freeze_counter += 1
        @decorate_happy_freezer.on_thaw
        def increment_decorate_happy_thaw_counter(self):
            self.decorate_happy_thaw_counter += 1

    b = C()
    assert b.decorate_happy_freezer.frozen == 0
    assert b.decorate_happy_freeze_counter == 0
    assert b.decorate_happy_thaw_counter == 0
    with b.decorate_happy_freezer:
        assert b.decorate_happy_freezer.frozen == 1
        assert b.decorate_happy_freeze_counter == 1
        assert b.decorate_happy_thaw_counter == 0
        with b.decorate_happy_freezer:
            assert b.decorate_happy_freezer.frozen == 2
            assert b.decorate_happy_freeze_counter == 1
            assert b.decorate_happy_thaw_counter == 0
        assert b.decorate_happy_freezer.frozen == 1
        assert b.decorate_happy_freeze_counter == 1
        assert b.decorate_happy_thaw_counter == 0
    assert b.decorate_happy_freezer.frozen == 0
    assert b.decorate_happy_freeze_counter == 1
    assert b.decorate_happy_thaw_counter == 1
    
    with b.decorate_happy_freezer:
        assert b.decorate_happy_freezer.frozen == 1
        assert b.decorate_happy_freeze_counter == 2
        assert b.decorate_happy_thaw_counter == 1
    assert b.decorate_happy_freezer.frozen == 0
    assert b.decorate_happy_freeze_counter == 2
    assert b.decorate_happy_thaw_counter == 2
        
    
def test_argument_happy_freezer_property():
    '''Test a freezer property which defines both handlers with arguments.'''
    class C:
        argument_happy_freeze_counter = caching.CachedProperty(0)
        argument_happy_thaw_counter = caching.CachedProperty(0)        
        def increment_argument_happy_freeze_counter(self):
            self.argument_happy_freeze_counter += 1
        def increment_argument_happy_thaw_counter(self):
            self.argument_happy_thaw_counter += 1
        argument_happy_freezer = FreezerProperty(
            on_freeze=increment_argument_happy_freeze_counter,
            on_thaw=increment_argument_happy_thaw_counter,
            name='argument_happy_freezer'
        )
     
    c = C()
    assert c.argument_happy_freezer.frozen == 0
    assert c.argument_happy_freeze_counter == 0
    assert c.argument_happy_thaw_counter == 0
    with c.argument_happy_freezer:
        assert c.argument_happy_freezer.frozen == 1
        assert c.argument_happy_freeze_counter == 1
        assert c.argument_happy_thaw_counter == 0
        with c.argument_happy_freezer:
            assert c.argument_happy_freezer.frozen == 2
            assert c.argument_happy_freeze_counter == 1
            assert c.argument_happy_thaw_counter == 0
        assert c.argument_happy_freezer.frozen == 1
        assert c.argument_happy_freeze_counter == 1
        assert c.argument_happy_thaw_counter == 0
    assert c.argument_happy_freezer.frozen == 0
    assert c.argument_happy_freeze_counter == 1
    assert c.argument_happy_thaw_counter == 1
    
    with c.argument_happy_freezer:
        assert c.argument_happy_freezer.frozen == 1
        assert c.argument_happy_freeze_counter == 2
        assert c.argument_happy_thaw_counter == 1
    assert c.argument_happy_freezer.frozen == 0
    assert c.argument_happy_freeze_counter == 2
    assert c.argument_happy_thaw_counter == 2
    
        
def test_mix_freezer_property():
    '''
    Test freezer property which mixes decorated and arg-specified handlers.
    '''
    class D:
        mix_freeze_counter = caching.CachedProperty(0)
        mix_thaw_counter = caching.CachedProperty(0)
        def increment_mix_freeze_counter(self):
            self.mix_freeze_counter += 1
        mix_freezer = FreezerProperty(on_freeze=increment_mix_freeze_counter)
        @mix_freezer.on_thaw
        def increment_mix_thaw_counter(self):
            self.mix_thaw_counter += 1
     
    d = D()
    assert d.mix_freezer.frozen == 0
    assert d.mix_freeze_counter == 0
    assert d.mix_thaw_counter == 0
    with d.mix_freezer:
        assert d.mix_freezer.frozen == 1
        assert d.mix_freeze_counter == 1
        assert d.mix_thaw_counter == 0
        with d.mix_freezer:
            assert d.mix_freezer.frozen == 2
            assert d.mix_freeze_counter == 1
            assert d.mix_thaw_counter == 0
        assert d.mix_freezer.frozen == 1
        assert d.mix_freeze_counter == 1
        assert d.mix_thaw_counter == 0
    assert d.mix_freezer.frozen == 0
    assert d.mix_freeze_counter == 1
    assert d.mix_thaw_counter == 1
    
    with d.mix_freezer:
        assert d.mix_freezer.frozen == 1
        assert d.mix_freeze_counter == 2
        assert d.mix_thaw_counter == 1
    assert d.mix_freezer.frozen == 0
    assert d.mix_freeze_counter == 2
    assert d.mix_thaw_counter == 2
        
    
def test_different_type_freezer_property():
    '''Test a freezer property that specifies a non-default freezer type.'''
    
    class CustomFreezer(Freezer):
        def __init__(self, obj):
            self.obj = obj
            
        def freeze_handler(self):
            self.obj.different_type_freeze_counter += 1
            
        def thaw_handler(self):
            self.obj.different_type_thaw_counter += 1
    
    class E:
        different_type_freeze_counter = caching.CachedProperty(0)
        different_type_thaw_counter = caching.CachedProperty(0)
        different_type_freezer = FreezerProperty(
            freezer_type=CustomFreezer,
            doc='A freezer using a custom freezer class.'
        )
     
    e = E()
    assert E.different_type_freezer.__doc__ == \
           'A freezer using a custom freezer class.'
    assert e.different_type_freezer.frozen == 0
    assert e.different_type_freeze_counter == 0
    assert e.different_type_thaw_counter == 0
    with e.different_type_freezer:
        assert e.different_type_freezer.frozen == 1
        assert e.different_type_freeze_counter == 1
        assert e.different_type_thaw_counter == 0
        with e.different_type_freezer:
            assert e.different_type_freezer.frozen == 2
            assert e.different_type_freeze_counter == 1
            assert e.different_type_thaw_counter == 0
        assert e.different_type_freezer.frozen == 1
        assert e.different_type_freeze_counter == 1
        assert e.different_type_thaw_counter == 0
    assert e.different_type_freezer.frozen == 0
    assert e.different_type_freeze_counter == 1
    assert e.different_type_thaw_counter == 1
    
    with e.different_type_freezer:
        assert e.different_type_freezer.frozen == 1
        assert e.different_type_freeze_counter == 2
        assert e.different_type_thaw_counter == 1
    assert e.different_type_freezer.frozen == 0
    assert e.different_type_freeze_counter == 2
    assert e.different_type_thaw_counter == 2