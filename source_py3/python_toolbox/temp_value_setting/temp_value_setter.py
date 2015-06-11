# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''
Defines the `TempValueSetter` class.

See its documentation for more details.
'''

from python_toolbox.context_management import ContextManager


__all__ = ['TempValueSetter']


class NotInDict:
    '''Object signifying that the key was not found in the dict.'''
    # todo: make uninstanciable


class TempValueSetter(ContextManager):
    '''
    Context manager for temporarily setting a value to a variable.
    
    The value is set to the variable before the suite starts, and gets reset
    back to the old value after the suite finishes.
    '''
    
    def __init__(self, variable, value, assert_no_fiddling=True):
        '''
        Construct the `TempValueSetter`.
        
        `variable` may be either an `(object, attribute_string)`, a `(dict,
        key)` pair, or a `(getter, setter)` pair.
        
        `value` is the temporary value to set to the variable.
        '''
        
        self.assert_no_fiddling = assert_no_fiddling
        

        #######################################################################
        # We let the user input either an `(object, attribute_string)`, a
        # `(dict, key)` pair, or a `(getter, setter)` pair. So now it's our job
        # to inspect `variable` and figure out which one of these options the
        # user chose, and then obtain from that a `(getter, setter)` pair that
        # we could use.
        
        bad_input_exception = Exception(
            '`variable` must be either an `(object, attribute_string)` pair, '
            'a `(dict, key)` pair, or a `(getter, setter)` pair.'
        )
        
        try:
            first, second = variable
        except Exception:
            raise bad_input_exception
        if hasattr(first, '__getitem__') and hasattr(first, 'get') and \
           hasattr(first, '__setitem__') and hasattr(first, '__delitem__'):
            # `first` is a dictoid; so we were probably handed a `(dict, key)`
            # pair.
            self.getter = lambda: first.get(second, NotInDict)
            self.setter = lambda value: (first.__setitem__(second, value) if 
                                         value is not NotInDict else
                                         first.__delitem__(second))
            ### Finished handling the `(dict, key)` case. ###
            
        elif callable(second):
            # `second` is a callable; so we were probably handed a `(getter,
            # setter)` pair.
            if not callable(first):
                raise bad_input_exception
            self.getter, self.setter = first, second
            ### Finished handling the `(getter, setter)` case. ###
        else:
            # All that's left is the `(object, attribute_string)` case.
            if not isinstance(second, str):
                raise bad_input_exception
            
            parent, attribute_name = first, second
            self.getter = lambda: getattr(parent, attribute_name)
            self.setter = lambda value: setattr(parent, attribute_name, value)
            ### Finished handling the `(object, attribute_string)` case. ###

        #
        #
        ### Finished obtaining a `(getter, setter)` pair from `variable`. #####
        
            
        self.getter = self.getter
        '''Getter for getting the current value of the variable.'''
        
        self.setter = self.setter
        '''Setter for Setting the the variable's value.'''
        
        self.value = value
        '''The value to temporarily set to the variable.'''
        
        self.active = False

        
    def __enter__(self):
        
        self.active = True
        
        self.old_value = self.getter()
        '''The old value of the variable, before entering the suite.'''
        
        self.setter(self.value)

        # In `__exit__` we'll want to check if anyone changed the value of the
        # variable in the suite, which is unallowed. But we can't compare to
        # `.value`, because sometimes when you set a value to a variable, some
        # mechanism modifies that value for various reasons, resulting in a
        # supposedly equivalent, but not identical, value. For example this
        # happens when you set the current working directory on Mac OS.
        #
        # So here we record the value right after setting, and after any
        # possible processing the system did to it:
        self._value_right_after_setting = self.getter()
        
        return self
        
        
    def __exit__(self, exc_type, exc_value, exc_traceback):

        if self.assert_no_fiddling:
            # Asserting no-one inside the suite changed our variable:
            assert self.getter() == self._value_right_after_setting
        
        self.setter(self.old_value)
        
        self.active = False