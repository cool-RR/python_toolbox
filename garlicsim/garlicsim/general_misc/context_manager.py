# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `ContextManager` class.

See its documentation for more information.
'''

from garlicsim.general_misc.third_party import decorator as decorator_module


class ContextManager(object):
    
    def __call__(self, function):
        def inner(*args, **kwargs):
            with self:
                return function(*args, **kwargs)
        return decorator_module.decorator(inner, function)
    
    def __enter__(self):
        pass
    
    def __exit__(self, *args, **kwargs):
        pass