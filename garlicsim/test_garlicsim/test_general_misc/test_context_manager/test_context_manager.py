# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

from garlicsim.general_misc.context_manager import (ContextManager,
                                                    ContextManagerType,
                                                    SelfHook)

flag = None
exception_caught = None




def test_generator():
    @ContextManagerType
    def MyContextManager(value):
        global flag, exception_caught
        former_value = flag
        flag = value
        try:
            yield
        finally:
            flag = former_value
            
    check_context_manager_type(MyContextManager,
                               self_returning=False,
                               error_catching=False)
    

def test_error_catching_generator():
    
    @ContextManagerType
    def MyContextManager(value):
        global flag, exception_caught
        former_value = flag
        flag = value
        try:
            yield
        except Exception, exception:
            exception_caught = exception
        finally:
            flag = former_value
            
    check_context_manager_type(MyContextManager,
                               self_returning=False,
                               error_catching=True)


def test_self_returning_generator():
    @ContextManagerType
    def MyContextManager(value):
        global flag, exception_caught
        former_value = flag
        flag = value
        try:
            yield SelfHook
        finally:
            flag = former_value
            
    check_context_manager_type(MyContextManager,
                               self_returning=True,
                               error_catching=False)
    


def test_self_returning_error_catching_generator():
    @ContextManagerType
    def MyContextManager(value):
        global flag, exception_caught
        former_value = flag
        flag = value
        try:
            yield SelfHook
        except Exception, exception:
            exception_caught = exception
        finally:
            flag = former_value
            
    check_context_manager_type(MyContextManager,
                               self_returning=True,
                               error_catching=False)    
    
def test_manage_context():
    
    class MyContextManager(ContextManager):
        def __init__(self, value):
            self.value = value
        
        def manage_context(self):
            global flag, exception_caught
            former_value = flag
            flag = self.value
            try:
                yield
            finally:
                flag = former_value
            
    check_context_manager_type(MyContextManager,
                               self_returning=False,
                               error_catching=False)
        
    
def test_error_catching_manage_context():
    
    class MyContextManager(ContextManager):
        def __init__(self, value):
            self.value = value
        
        def manage_context(self):
            global flag, exception_caught
            former_value = flag
            flag = self.value
            try:
                yield
            except Exception, exception:
                exception_caught = exception
            finally:
                flag = former_value
            
    check_context_manager_type(MyContextManager,
                               self_returning=False,
                               error_catching=True)
    
def test_self_returning_manage_context():
    
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
            
    check_context_manager_type(MyContextManager,
                               self_returning=True,
                               error_catching=False)
    
    
def test_self_returning_error_catching_manage_context():
    
    class MyContextManager(ContextManager):
        def __init__(self, value):
            self.value = value
        
        def manage_context(self):
            global flag, exception_caught
            former_value = flag
            flag = self.value
            try:
                yield self
            except Exception, exception:
                exception_caught = exception
            finally:
                flag = former_value
            
    check_context_manager_type(MyContextManager,
                               self_returning=True,
                               error_catching=True)

    
def test_enter_exit():
    
    class MyContextManager(ContextManager):
        def __init__(self, value):
            self.value = value
        
        def __enter__(self):
            global flag
            self._former_value = flag
            flag = self.value
            
        def __exit__(self, type_=None, value=None, traceback=None):
            global flag
            flag = self._former_value
    
    check_context_manager_type(MyContextManager,
                               self_returning=False,
                               error_catching=False)

    
def test_error_catching_enter_exit():
    
    class MyContextManager(ContextManager):
        def __init__(self, value):
            self.value = value
        
        def __enter__(self):
            global flag
            self._former_value = flag
            flag = self.value
            
        def __exit__(self, type_=None, value=None, traceback=None):
            global flag, exception_caught
            flag = self._former_value
            if type_:
                exception_caught = value
                return True
    
    check_context_manager_type(MyContextManager,
                               self_returning=False,
                               error_catching=True)

    
def test_self_returning_enter_exit():
    
    class MyContextManager(ContextManager):
        def __init__(self, value):
            self.value = value
        
        def __enter__(self):
            global flag
            self._former_value = flag
            flag = self.value
            return self
            
        def __exit__(self, type_=None, value=None, traceback=None):
            global flag
            flag = self._former_value
    
    check_context_manager_type(MyContextManager,
                               self_returning=True,
                               error_catching=False)

    
def test_error_catching_self_returning_enter_exit():
    
    class MyContextManager(ContextManager):
        def __init__(self, value):
            self.value = value
        
        def __enter__(self):
            global flag
            self._former_value = flag
            flag = self.value
            return self
            
        def __exit__(self, type_=None, value=None, traceback=None):
            global flag, exception_caught
            flag = self._former_value
            if type_:
                exception_caught = value
                return True
    
    check_context_manager_type(MyContextManager,
                               self_returning=True,
                               error_catching=True)

    
def check_context_manager_type(context_manager_type,
                               self_returning,
                               error_catching):
    
    global flag, exception_caught
    
    assert flag is None
    assert exception_caught is None
    
    with context_manager_type(7) as return_value:
        assert flag == 7
        if self_returning:
            assert isinstance(return_value, context_manager_type)
        else: # self_returning is False
            assert return_value is None
        
    assert flag is None
    assert exception_caught is None
    
    my_context_manager = context_manager_type(1.1)
    assert isinstance(my_context_manager, context_manager_type)
    with my_context_manager as return_value:
        assert flag == 1.1
        if self_returning:
            assert return_value is my_context_manager
        else: # self_returning is False
            assert return_value is None
    
    assert flag is None
    assert exception_caught is None

    @context_manager_type('meow')
    def f():
        assert flag == 'meow'
        
    f()
    assert flag is None
    assert exception_caught is None
    
    # Now while raising exceptions:
    
    try:
        
        with context_manager_type(7) as return_value:
            assert flag == 7
            if self_returning:
                assert isinstance(return_value, context_manager_type)
            else: # self_returning is False
                assert return_value is None
            raise TypeError('ooga booga')
        
    except Exception, exception:
        assert not error_catching
        assert exception_caught is None
        assert type(exception) is TypeError
        assert exception.args[0] == 'ooga booga'
        
    else:
        assert error_catching
        assert type(exception_caught) is TypeError
        assert exception_caught.args[0] == 'ooga booga'
        exception_caught = None
        
    assert flag is None
    
    my_context_manager = context_manager_type(1.1)
    assert isinstance(my_context_manager, context_manager_type) 
    try:
        with my_context_manager as return_value:
            assert flag == 1.1
            if self_returning:
                assert return_value is my_context_manager
            else: # self_returning is False
                assert return_value is None
            {}[3]
    
    except Exception, exception:
        assert not error_catching
        assert exception_caught is None
        assert type(exception) is KeyError
        
    else:
        assert error_catching
        assert type(exception_caught) is KeyError
        exception_caught = None
        
    
    assert flag is None
    assert exception_caught is None

    @context_manager_type('meow')
    def f():
        assert flag == 'meow'
        1/0
        
    
    try:
        f()
    except Exception, exception:
        assert not error_catching
        assert exception_caught is None
        assert type(exception) is ZeroDivisionError
        
    else:
        assert error_catching
        assert (type(exception_caught) is ZeroDivisionError) or \
               (isinstance(exception_caught, basestring) and
                'zero' in exception_caught)
        exception_caught = None
        
    assert flag is None
    
    exception_caught = None
    