# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `TempValueSetter` class.

See its documentation for more details.
'''

from garlicsim.general_misc import address_tools


class TempValueSetter(object):
    '''
    Context manager for temporarily setting a value to a variable.
    
    The value is set to the variable before the suite starts, and gets reset
    back to the old value after the suite finishes.
    '''
    
    def __init__(self, variable, value):
        '''
        Construct the `TempValueSetter`.
        
        `variable` may be either an (`object`, `attribute_string`) pair or a
        `(getter, setter)` pair.
        
        `value` is the temporary value to set to the variable.
        '''
        try:
            first, second = variable
        except Exception:
            raise Exception("`variable` must be either `(my_object, "
                            "'my_attribute')` or `(getter, setter)`.")
        if callable(second):
            if not callable(first):
                raise Exception("`variable` must be either `(my_object, "
                                "'my_attribute')` or `(getter, setter)`.")
            self.getter, self.setter = first, second
        else:
            if not isinstance(second, basestring):
                raise Exception("`variable` must be either `(my_object, "
                                "'my_attribute')` or `(getter, setter)`.")
            
            parent, attribute_name = first, second
            self.getter = lambda: getattr(parent, attribute_name)
            self.setter = lambda value: setattr(parent, attribute_name, value)
            
        self.getter = self.getter
        '''Getter for getting the current value of the variable.'''
        
        self.setter = self.setter
        '''Setter for Setting the the variable's value.'''
        
        self.value = value
        '''The value to temporarily set to the variable.'''

        
    def __enter__(self):
        
        self.old_value = self.getter()
        '''The old value of the variable, before entering the suite.'''
        
        self.setter(self.value)

        # because of mac changing working directory:
        
        # In `__exit__` we'll want to check if anyone changed the value of the
        # variable in the suite, which is unallowed. But we can't compare to
        # `.value`, because sometimes when you set a value to a variable, some
        # mechanism modifies that value fore various reasons, resulting in a
        # supposedly equivalent, but not identical, value. For example this
        # happens when you set the current working directory on Mac OS.
        #
        # So here we record the value right after setting, and after any
        # possible processing the system did to it:
        self._value_right_after_setting = self.getter()
        
        
    def __exit__(self, *args, **kwargs):

        # Asserting no-one inside the suite changed our variable:
        assert self.getter() == self._value_right_after_setting
        
        self.setter(self.old_value)
        
        