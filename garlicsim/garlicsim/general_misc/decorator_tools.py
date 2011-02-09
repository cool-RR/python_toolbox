# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Tools for decorators.'''

import functools
import inspect
import types

from garlicsim.general_misc.third_party import decorator as \
                                               michele_decorator_module

def decorator(caller, func=None):
    """
    decorator(caller) converts a caller function into a decorator;
    decorator(caller, func) decorates a function using a caller.
    """
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
    
    Do not use this on decorators that may take a function object as their
    first argument.
    
    Note: When used on a class, replaces the class's `__call__` method
    *in-place*, without creating a new class. It returns the same class that
    was fed into it.
    
    blocktodo: What about decorated classes?
    '''
    is_class = isinstance(decorator_builder, type)
    if is_class:
        decorator_builder_class = decorator_builder
        old_call_function = decorator_builder_class.__call__
        def decorator_builder(*args, **kwargs):
            return old_call_function(decorator_builder_class,
                                     *args, **kwargs)
    else: # We're decorating a normal function:
        assert isinstance(decorator_builder, types.FunctionType)
        
    decorator_builder_name = decorator_builder.__name__
    
    def inner(_, *args, **kwargs):
        
        if args and isinstance(args[0], types.FunctionType):
            
            function = args[0]
            function_name = function.__name__
            raise TypeError('It seems that you forgot to add parentheses '
                            'after `@%s` when decorating the `%s` '
                            'function.' % (decorator_builder_name,
                            function_name))
        else:
            return decorator_builder(*args, **kwargs)
        
    if is_class:
        #from garlicsim.general_misc import monkeypatching_tools
        #monkeypatching_tools.monkeypatch_method(
            #decorator_builder_class,
            #name='__call__'
            #)(inner)
        decorator_builder_class.__call__ = classmethod(inner)
        
        return decorator_builder_class
        
    else: # We're decorating a normal function:
        return decorator(inner, decorator_builder)
        