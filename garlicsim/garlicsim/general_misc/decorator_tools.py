# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Tools for decorators.'''

import functools
import inspect

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
        return michele_decorator_module.FunctionMaker.create(
            func, "return _call_(_func_, %(shortsignature)s)",
            evaldict, undecorated=func)
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

    


