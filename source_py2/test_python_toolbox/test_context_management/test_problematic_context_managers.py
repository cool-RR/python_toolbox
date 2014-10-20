# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing module for various problematic context managers.'''

import nose

from python_toolbox import cute_testing

from python_toolbox.context_management import (ContextManager,
                                                    ContextManagerType,
                                                    SelfHook)

def test_defining_enter_and_manage_context():
    '''
    Test context manager class defining both `__enter__` and `manage_context`.
    '''
    
    with cute_testing.RaiseAssertor(
        Exception,
        'both an `__enter__` method and a'
        ):
        
        class MyContextManager(ContextManager):
            def manage_context(self):
                yield self
            def __enter__(self):
                return self

            
def test_defining_exit_and_manage_context():
    '''
    Test context manager class defining both `__exit__` and `manage_context`.
    '''
    
    with cute_testing.RaiseAssertor(
        Exception,
        'both an `__exit__` method and a'
        ):
        
        class MyContextManager(ContextManager):
            def manage_context(self):
                yield self
            def __exit__(self, *exc):
                pass

            
def test_defining_enter_on_top_of_manage_context():
    '''
    Test an `__enter__`-definer inheriting from a `manage_context`-definer.
    '''
    class MyBaseContextManager(ContextManager):
        def manage_context(self):
            yield self
            
    with cute_testing.RaiseAssertor(
        Exception,
        "defines an `__enter__` method, but not an `__exit__` method"
        ):
        
        class MyContextManager(MyBaseContextManager):
            def __enter__(self):
                return self
            
            
def test_defining_exit_on_top_of_manage_context():
    '''
    Test an `__exit__`-definer inheriting from a `manage_context`-definer.
    '''
    
    class MyBaseContextManager(ContextManager):
        def manage_context(self):
            yield self
            
    with cute_testing.RaiseAssertor(
        Exception,
        "defines an `__exit__` method, but not an `__enter__` method"
        ):
        
        class MyContextManager(MyBaseContextManager):
            def __exit__(self, *exc):
                pass