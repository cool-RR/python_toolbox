# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

from python_toolbox import decorator_tools


class DecoratingContextManager:
    '''
    Context manager that can decorate a function to use it.
    
    Example:
    
        my_context_manager = DecoratingContextManager()
        
        @my_context_manager
        def f():
            pass # Anything that happens here is surrounded by the
                 # equivalent of `my_context_manager`.
        
    '''
    
    def __call__(self, function):
        '''Decorate `function` to use this context manager when it's called.'''
        def inner(function_, *args, **kwargs):
            with self:
                return function_(*args, **kwargs)
        return decorator_tools.decorator(inner, function)