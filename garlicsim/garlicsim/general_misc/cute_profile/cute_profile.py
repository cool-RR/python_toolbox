# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `profile_ready` decorator.

See its documentation for more details.
'''

import functools

from garlicsim.general_misc import decorator_tools

from . import base_profile


def profile_ready(condition=None, off_after=True, sort=2):
    '''
    Decorator for setting a function to be ready for profiling.
    
    For example:
    
        @profile_ready()
        def f(x, y):
            do_something_long_and_complicated()
            
    The advantages of this over regular `cProfile` are:
    
     1. It doesn't interfere with the function's return value.
     
     2. You can set the function to be profiled *when* you want, on the fly.
     
    How can you set the function to be profiled? There are a few ways:
    
    You can set `f.profiling_on=True` for the function to be profiled on the
    next call. It will only be profiled once, unless you set
    `f.off_after=False`, and then it will be profiled every time until you set
    `f.profiling_on=False`.
    
    You can also set `f.condition`. You set it to a condition function taking
    as arguments the decorated function and any arguments (positional and
    keyword) that were given to the decorated function. If the condition
    function returns `True`, profiling will be on for this function call,
    `f.condition` will be reset to `None` afterwards, and profiling will be
    turned off afterwards as well. (Unless, again, `f.off_after` is set to
    `False`.)
    
    `sort` is an `int` specifying which column the results will be sorted by.
    '''
    
    
    def decorator(function):
        
        def inner(function_, *args, **kwargs):
            
            if decorated_function.condition is not None:
                
                if decorated_function.condition is True or \
                   decorated_function.condition(
                       decorated_function.original_function,
                       *args,
                       **kwargs
                       ):
                    
                    decorated_function.profiling_on = True
                    
            if decorated_function.profiling_on:
                
                if decorated_function.off_after:
                    decorated_function.profiling_on = False
                    decorated_function.condition = None
                    
                # This line puts it in locals, weird:
                decorated_function.original_function
                
                base_profile.runctx(
                    'result = '
                    'decorated_function.original_function(*args, **kwargs)',
                    globals(), locals(), sort=decorated_function.sort
                )                
                return locals()['result']
            
            else: # decorated_function.profiling_on is False
                
                return decorated_function.original_function(*args, **kwargs)
            
        decorated_function = decorator_tools.decorator(inner, function)
        
        decorated_function.original_function = function
        decorated_function.profiling_on = None
        decorated_function.condition = condition
        decorated_function.off_after = off_after
        decorated_function.sort = sort
        
        return decorated_function
    
    return decorator

