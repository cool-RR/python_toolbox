# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

from garlicsim.general_misc.third_party import decorator as decorator_module


@decorator_module.decorator
def count_calls(function, *args, **kwargs):
    
    if not hasattr(function, 'call_count'):
        function.call_count = 0
        
    function.call_count +=1
    return function(*args, **kwargs)