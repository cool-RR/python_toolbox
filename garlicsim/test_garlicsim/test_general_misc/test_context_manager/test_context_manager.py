# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

from garlicsim.general_misc.context_manager import (ContextManager,
                                                    ContextManagerType)

flag = None
exception_caught = None


def test_generator():
    
    global exception_caught
    assert exception_caught is None
    
    @ContextManagerType
    def MyContextManager(value):
        global flag
        former_value = flag
        flag = value
        try:
            yield
        except Exception, exception:
            exception_caught = exception
        finally:
            flag = former_value
            
    check_context_manager_type(MyContextManager)
    

    
def test_manage_context():
    
    class MyContextManager(ContextManager):
        def __init__(self, value):
            self.value = value
        
        def manage_context(self):
            global flag
            former_value = flag
            flag = self.value
            try:
                yield self
            finally:
                flag = former_value
            
    check_context_manager_type(MyContextManager)

    
def test_enter_exit():
    
    class MyContextManager(ContextManager):
        def __init__(self, value):
            self.value = value
        
        def __enter__(self):
            global flag
            self._former_value = flag
            flag = self.value
            
        def __exit__(self, *args, **kwargs):
            global flag
            flag = self._former_value
            
    
    check_context_manager_type(MyContextManager)

    
def check_context_manager_type(context_manager_type):
    
    global flag, exception_caught
    
    assert flag is None
    assert exception_caught is None
    
    with context_manager_type(7):
        assert flag == 7
        
    assert flag is None
    assert exception_caught is None
    
    my_context_manager = context_manager_type(1.1)
    with my_context_manager:
        assert flag == 1.1
    
    assert flag is None
    assert exception_caught is None

    @context_manager_type('meow')
    def f():
        assert flag == 'meow'
        
    f()
    assert flag is None
    assert exception_caught is None
    
    # Now while raising exceptions:
    
    with context_manager_type(7):
        assert flag == 7
        raise TypeError('ooga booga')
    
    assert type(exception_caught) is TypeError
    assert exception_caught.args[0] == 'ooga booga'
    exception_caught = None
        
    assert flag is None
    
    my_context_manager = context_manager_type(1.1)
    with my_context_manager:
        assert flag == 1.1
    
    assert flag is None
    assert exception_caught is None

    @context_manager_type('meow')
    def f():
        assert flag == 'meow'
        1/0
        
    f()
    assert flag is None
    assert type(exception_caught) is ZeroDivisionError
    exception_caught = None
    