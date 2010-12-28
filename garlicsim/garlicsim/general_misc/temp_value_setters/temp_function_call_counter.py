# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `` class.

See its documentation for more details.
'''

import sys

from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc import address_tools

from .temp_value_setter import TempValueSetter
from garlicsim.general_misc.tracing_tools import count_calls


class TempFunctionCallCounter(TempValueSetter):
    '''
    
    allows:
    function
    (parent_object, function_name)
    (getter, setter)
    '''
    
    def __init__(self, function):    
        
        if cute_iter_tools.is_iterable(function):
            first, second = function
            if isinstance(second, basestring):
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
                raise Exception("couldn't guess from function, please do "
                                "getter/setter or parent/name") # tododoc
            first, second = parent_object, function_name
            
        self.call_counting_function = count_calls(actual_function)
        
        TempValueSetter.__init__(
            self,
            (first, second),
            value=call_counting_function
        )
        
        
    call_count = property(lambda self: self.call_counting_function.call_count)
    
    