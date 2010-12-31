# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

from garlicsim.general_misc.context_manager import ContextManager


def test_generator():
    
    flag = None
    @ContextManager
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

    
def test_plain_function():
    
    flag = None
    @ContextManager
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
        
    
    