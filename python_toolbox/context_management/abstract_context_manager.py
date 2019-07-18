# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

import sys
import types
import abc

from python_toolbox import decorator_tools

from .mixins.decorating_context_manager_mixin import _DecoratingContextManagerMixin
from .context_manager_type import ContextManagerType
from .self_hook import SelfHook


class AbstractContextManager(metaclass=abc.ABCMeta):
    '''
    A no-frills context manager.

    This class is used mostly to check whether an object is a context manager:

        >>> isinstance(threading.Lock(), AbstractContextManager)
        True

    '''
    @abc.abstractmethod
    def __enter__(self):
        '''Prepare for suite execution.'''


    @abc.abstractmethod
    def __exit__(self, exc_type, exc_value, exc_traceback):
        '''Cleanup after suite execution.'''

    @classmethod
    def __subclasshook__(cls, candidate_class):
        if cls is AbstractContextManager:
            return (
                hasattr(candidate_class, '__enter__') and
                candidate_class.__enter__ is not None and
                hasattr(candidate_class, '__exit__') and
                candidate_class.__exit__ is not None
            )
        else:
            return NotImplemented


