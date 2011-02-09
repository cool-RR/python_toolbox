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
    
    Safe to use only on decorators that cannot take a function as their first
    argument.
    
    blocktodo: What about decorated classes?
    '''
    if isinstance(decorator_builder, type):
        raise NotImplementedError # blocktodo: maybe think about this.
    name = decorator_builder.__name__
    def inner(*args, **kwargs):
        if (not kwargs) and len(args) == 1 \
           and isinstance(args[0], types.FunctionType):
            (function,) = args
            function_name = function.__name__
            raise Exception('It seems that you forgot to add parentheses '
                            'after `@%s` when decorating the `%s` '
                            'function.' % (name, function_name))
        else:
            return decorator_builder(*args, **kwargs)
        