# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

from garlicsim.general_misc.context_manager import (ContextManager,
                                                    ContextManagerType)

flag = None


def test_generator():
    
    
    @ContextManagerType
    def MyContextManager(value):
        global flag
        former_value = flag
        flag = value
        try:
            yield
        finally:
            flag = former_value
            
    assert flag is None
    with MyContextManager(7):
        assert flag == 7
    assert flag is None
    
    my_context_manager = MyContextManager(1.1)
    with my_context_manager:
        assert flag == 1.1
    assert flag is None

    @MyContextManager('meow')
    def f():
        assert flag == 'meow'
        
    f()
    assert flag is None

    
def test_manage_context():
    
    class MyContextManager(ContextManager):
        def __init__(self, value):
            self.value = value
        
        def manage_context(self):
            global flag
            former_value = flag
            flag = value
            try:
                yield my_context_manager
            finally:
                flag = former_value
            
    assert flag is None
    with MyContextManager(7):
        assert flag == 7
    assert flag is None
    
    my_context_manager = MyContextManager(1.1)
    with my_context_manager:
        assert flag == 1.1
    assert flag is None

    @MyContextManager('meow')
    def f():
        assert flag == 'meow'
        
    f()
    assert flag is None

def test_enter_exit():
    
    class MyClassGenerator(ContextManager):
        def __init__(self, value):
            self.value = value
        
        def __enter__(self):
            global flag
            former_value = flag
            flag = value
            
        def __exit__(self, *args, **kwargs):
            global flag
            flag = former_value
            
    assert flag is None
    with MyContextManager(7):
        assert flag == 7
    assert flag is None
    
    my_context_manager = MyContextManager(1.1)
    with my_context_manager:
        assert flag == 1.1
    assert flag is None

    @MyContextManager('meow')
    def f():
        assert flag == 'meow'
        
    f()
    assert flag is None

    