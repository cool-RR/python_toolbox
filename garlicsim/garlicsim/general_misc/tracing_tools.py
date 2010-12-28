# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

from garlicsim.general_misc.third_party import decorator as decorator_module




def count_calls(function):
    
    def _count_calls(function, *args, **kwargs):
        decorated_function.call_count += 1
        return function(*args, **kwargs)
    
    decorated_function = decorator_module.decorator(_count_calls, function)
    
    decorated_function.call_count = 0
    
    return decorated_function