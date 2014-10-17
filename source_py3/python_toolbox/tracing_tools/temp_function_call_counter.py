# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines the `TempFunctionCallCounter` context manager.

See its documentation for more details.
'''

import sys

from python_toolbox import cute_iter_tools
from python_toolbox import address_tools

from python_toolbox.temp_value_setting import TempValueSetter
from .count_calls import count_calls


class TempFunctionCallCounter(TempValueSetter):
    '''
    Temporarily counts the number of calls made to a function.
    
    Example:
    
        f()
        with TempFunctionCallCounter(f) as counter:
            f()
            f()
        assert counter.call_count == 2
        
    '''
    
    def __init__(self, function):
        '''
        Construct the `TempFunctionCallCounter`.
        
        For `function`, you may pass in either a function object, or a
        `(parent_object, function_name)` pair, or a `(getter, setter)` pair.
        '''
        
        if cute_iter_tools.is_iterable(function):
            first, second = function
            if isinstance(second, str):
                actual_function = getattr(first, second)
            else:
                assert callable(first) and callable(second)
                actual_function = first() # `first` is the getter in this case.
                
        else: # not cute_iter_tools.is_iterable(function)
            assert callable(function)
            actual_function = function
            try:
                address = address_tools.object_to_string.get_address(function)
                parent_object_address, function_name = address.rsplit('.', 1)
                parent_object = address_tools.resolve(parent_object_address)
            except Exception:
                raise Exception("Couldn't obtain parent/name pair from "
                                "function; supply one manually or "
                                "alternatively supply a getter/setter pair.")
            first, second = parent_object, function_name
            
        self.call_counting_function = count_calls(actual_function)
        
        TempValueSetter.__init__(
            self,
            (first, second),
            value=self.call_counting_function
        )
        
        
    call_count = property(
        lambda self: getattr(self.call_counting_function, 'call_count', 0)
    )
    '''The number of calls that were made to the function.'''
    
    