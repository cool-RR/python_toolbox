# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines various functions related to context managers.

See their documentation for more information.
'''

import sys

from .context_manager_type import ContextManagerType
from .context_manager import ContextManager


@ContextManagerType
def nested(*managers):
    # Code from `contextlib`
    exits = []
    vars = []
    exc = (None, None, None)
    try:
        for mgr in managers:
            exit = mgr.__exit__
            enter = mgr.__enter__
            vars.append(enter())
            exits.append(exit)
        yield vars
    except:
        exc = sys.exc_info()
    finally:
        while exits:
            exit = exits.pop()
            try:
                if exit(*exc):
                    exc = (None, None, None)
            except:
                exc = sys.exc_info()
        if exc != (None, None, None):
            # Don't rely on sys.exc_info() still containing
            # the right information. Another exception may
            # have been raised and caught by an exit method
            raise exc[1].with_traceback(exc[2])
    
    
def idempotentify(context_manager):
    '''
    Wrap a context manager so repeated calls to enter and exit will be ignored.
    
    This means that if you call `__enter__` a second time on the context
    manager, nothing will happen. The `__enter__` method won't be called and an
    exception would not be raised. Same goes for the `__exit__` method, after
    calling it once, if you try to call it again it will be a no-op. But now
    that you've called `__exit__` you can call `__enter__` and it will really
    do the enter action again, and then `__exit__` will be available again,
    etc.
    
    This is useful when you have a context manager that you want to put in an
    `ExitStack`, but you also possibly want to exit it manually before the
    `ExitStack` closes. This way you don't risk an exception by having the
    context manager exit twice.
    '''
    class _IdempotentContextManager:
        # Not inheriting from `ContextManager` because this class is internal
        # and not used beyond `idempotentify`, so no need for the extra
        # baggage.
        _entered = False
        _enter_value = None
        
        def __init__(self, wrapped_context_manager):
            self.__wrapped__ = wrapped_context_manager
            
        
        def __enter__(self):
            if not self._entered:
                self._enter_value = self.__wrapped__.__enter__()
                self._entered = True
            return self._enter_value
                
            
        def __exit__(self, exc_type, exc_value, exc_traceback):
            if self._entered:
                exit_value = self.__wrapped__.__exit__(exc_type, exc_value,
                                                       exc_traceback)
                self._entered = False
                return exit_value
                
    return _IdempotentContextManager(context_manager)
    
            