# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''
This module defines various functions related to context managers.

See their documentation for more information.
'''

import sys
import types
import string
import random

from python_toolbox import caching

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
    

def _wrap_context_manager_or_class(thing, wrapper_factory):
    if hasattr(type(thing), '__enter__'):
        # It's a context manager.
        return wrapper_factory(thing)
    else:
        assert issubclass(thing, ContextManager)
        # It's a context manager class.
        property_name = '__%s_context_manager_%s' % (
            thing.__name__,
            ' '.join(random.choice(string.ascii_letters) for _ in range(20))
        )
        return type(
            thing.__name__,
            (thing,),
            {
                property_name: caching.CachedProperty(wrapper_factory),
                '__enter__':
                         lambda self: getattr(self, property_name).__enter__(),
                '__exit__': lambda self, exc_type, exc_value, exc_traceback:
                        getattr(self, property_name).
                                  __exit__(exc_type, exc_value, exc_traceback),
                           
            }
        )
        
        


def as_idempotent(context_manager):
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

    Note: The first value returned by `__enter__` will be returned by all the
    subsequent no-op `__enter__` calls.
    '''
    return _wrap_context_manager_or_class(
        context_manager, _IdempotentContextManager
    )
    
            
def as_reentrant(context_manager):
    '''
    Wrap a context manager to make it reentant.
    
    A context manager wrapped with `as_reentrant` could be entered multiple
    times, and only after it's been exited the same number of times that it has
    been entered will the original `__exit__` method be called.
    
    Note: The first value returned by `__enter__` will be returned by all the
    subsequent no-op `__enter__` calls.
    '''
    return _wrap_context_manager_or_class(
        context_manager, _ReentrantContextManager
    )
    

class _IdempotentContextManager(ContextManager):
    _entered = False
    _enter_value = None
    
    def __init__(self, wrapped_context_manager):
        self.__wrapped__ = wrapped_context_manager
        
    
    def __enter__(self):
        if not self._entered:
            self._enter_value = self.__wrapped__.__enter__()
            self._entered = True
        return self._enter_value
            
        
    def __exit__(self, exc_type=None, exc_value=None, exc_traceback=None):
        if self._entered:
            exit_value = self.__wrapped__.__exit__(exc_type, exc_value,
                                                   exc_traceback)
            self._entered = False
            self._enter_value = None
            return exit_value

class _ReentrantContextManager(ContextManager):

    def __init__(self, wrapped_context_manager):
        self.__wrapped__ = wrapped_context_manager
        
    depth = caching.CachedProperty(
        0,
        doc='''
            The number of nested suites that entered this context manager.
            
            When the context manager is completely unused, it's `0`. When
            it's first used, it becomes `1`. When its entered again, it
            becomes `2`. If it is then exited, it returns to `1`, etc.
            '''
    )

    _enter_value = None
    
    def __enter__(self):
        if self.depth == 0:
            self._enter_value = self.__wrapped__.__enter__()
        self.depth += 1
        return self._enter_value
    
    
    def __exit__(self, exc_type=None, exc_value=None, exc_traceback=None):
        assert self.depth >= 1
        if self.depth == 1:
            exit_value = self.__wrapped__.__exit__(
                exc_type, exc_value, exc_traceback
            )
            self._enter_value = None
        else:
            exit_value = None
        self.depth -= 1
        return exit_value

                

