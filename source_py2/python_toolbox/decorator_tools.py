# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Tools for decorators.'''

import functools
import inspect
import types

from python_toolbox.third_party import decorator as michele_decorator_module

def decorator(caller, func=None):
    '''
    Create a decorator.
    
    `decorator(caller)` converts a caller function into a decorator;
    `decorator(caller, func)` decorates a function using a caller.
    '''
    if func is not None: # returns a decorated function
        evaldict = func.func_globals.copy()
        evaldict['_call_'] = caller
        evaldict['_func_'] = func
        result = michele_decorator_module.FunctionMaker.create(
            func, "return _call_(_func_, %(shortsignature)s)",
            evaldict, undecorated=func)
        result.__wrapped__ = func
        return result
    else: # returns a decorator
        if isinstance(caller, functools.partial):
            return functools.partial(decorator, caller)
        # otherwise assume caller is a function
        first = inspect.getargspec(caller)[0][0] # first arg
        evaldict = caller.func_globals.copy()
        evaldict['_call_'] = caller
        evaldict['decorator'] = decorator
        return michele_decorator_module.FunctionMaker.create(
            '%s(%s)' % (caller.__name__, first), 
            'return decorator(_call_, %s)' % first,
            evaldict, undecorated=caller,
            doc=caller.__doc__, module=caller.__module__)

 
def helpful_decorator_builder(decorator_builder):
    '''
    Take a decorator builder and return a "helpful" version of it.
    
    A decorator builder is a function that returns a decorator. A decorator
    is used like this:

        @foo
        def bar():
            pass
            
    While a decorator *builder* is used like this 
    
        @foo()
        def bar():
            pass
            
    The parentheses are the difference.
    
    Sometimes the user forgets to put parentheses after the decorator builder;
    in that case, a helpful decorator builder is one that raises a helpful
    exception, instead of an obscure one. Decorate your decorator builders with
    `helpful_decorator_builder` to make them raise a helpful exception when the
    user forgets the parentheses.
            
    Limitations:
    
      - Do not use this on decorators that may take a function object as their
        first argument.
    
      - Cannot be used on classes.
      
    '''

    assert isinstance(decorator_builder, types.FunctionType)
    
    def inner(same_decorator_builder, *args, **kwargs):
        
        if args and isinstance(args[0], types.FunctionType):            
            function = args[0]
            function_name = function.__name__
            decorator_builder_name = decorator_builder.__name__
            raise TypeError('It seems that you forgot to add parentheses '
                            'after `@%s` when decorating the `%s` '
                            'function.' % (decorator_builder_name,
                            function_name))
        else:
            return decorator_builder(*args, **kwargs)
        
    return decorator(inner, decorator_builder)
        