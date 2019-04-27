# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import abc

from python_toolbox import misc_tools

from .context_manager import ContextManager


class DelegatingContextManager(ContextManager):
    '''
    Object which delegates its context manager interface to another object.

    You set the delegatee context manager as `self.delegatee_context_manager`,
    and whenever someone tries to use the current object as a context manager,
    the `__enter__` and `__exit__` methods of the delegatee object will be
    called. No other methods of the delegatee will be used.

    This is useful when you are tempted to inherit from some context manager
    class, but you don't to inherit all the other methods that it defines.
    '''

    delegatee_context_manager = None
    '''
    The context manager whose `__enter__` and `__exit__` method will be used.

    You may implement this as either an instance attribute or a property.
    '''

    __enter__ = misc_tools.ProxyProperty(
        '.delegatee_context_manager.__enter__'
    )
    __exit__ = misc_tools.ProxyProperty(
        '.delegatee_context_manager.__exit__'
    )