# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

from garlicsim.general_misc.context_manager import (ContextManager,
                                                    ContextManagerType)


def test_generator():
    
    flag = None
    @ContextManagerType
    def MyContextManager(value):
        former_value = flag
        flag = value
        try:
            yield my_context_manager
        finally:
            flag = former_value
            
    assert flag is None
    with MyContextManager(7) as my_context_manager:
        assert isinstance(my_context_manager, MyContextManager)
        assert flag == 7
    assert flag is None

    @MyContextManager('meow')
    def f():
        assert flag == meow
        
    f()
    assert flag is None

    
def test_manage_context():
    
    flag = None
    class MyClassGenerator(ContextManager):
        def __init__(self, value):
            self.value = value
        
        def manage_context(self):
            former_value = flag
            flag = value
            try:
                yield my_context_manager
            finally:
                flag = former_value
            
    assert flag is None
    with MyContextManager(7) as my_context_manager:
        assert isinstance(my_context_manager, MyContextManager)
        assert flag == 7
    assert flag is None

    @MyContextManager('meow')
    def f():
        assert flag == meow
        
    f()
    assert flag is None

def test_enter_exit():
    
    flag = None
    class MyClassGenerator(ContextManager):
        def __init__(self, value):
            self.value = value
        
        def __enter__(self):
            former_value = flag
            flag = value
            
        def __exit__(self, *args, **kwargs):
            flag = former_value
            
    assert flag is None
    with MyContextManager(7) as my_context_manager:
        assert isinstance(my_context_manager, MyContextManager)
        assert flag == 7
    assert flag is None

    @MyContextManager('meow')
    def f():
        assert flag == meow
        
    f()
    assert flag is None

    