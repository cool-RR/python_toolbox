# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `DecoratingContextManager` class.

See its documentation for more information.
'''

from __future__ import with_statement

from garlicsim.general_misc import decorator_tools


class DecoratingContextManager(object):
    '''
    blocktododoc
    '''
    
    def __call__(self, function):
        '''Decorate `function` to use this context manager when it's called.'''
        def inner(function_, *args, **kwargs):
            with self:
                return function_(*args, **kwargs)
        return decorator_tools.decorator(inner, function)