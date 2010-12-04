# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

from garlicsim.general_misc import address_tools


class TempValueSetter(object):
    def __init__(self, variable, value):
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
        '''tododoc'''
        
        self.setter = self.setter
        '''tododoc'''
        
        self.value = value

        
    def __enter__(self):
        
        self.old_value = self.getter()
        self.setter(self.value)
        
    def __exit__(self, *args, **kwargs):
        assert self.getter() == self.value
        self.setter(self.old_value)