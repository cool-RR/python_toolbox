# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

from garlicsim.general_misc import misc_tools



class FunctionWrappingType(type):
    def __call__(self, name, bases, namespace_dict):
        my_type = super(type, self).__call__(self, name, bases, namespace_dict)
        my_getted_vars = misc_tools.getted_vars(
            my_type,
            _getattr=super(type, self).__getattribute__
        )
        functions_to_wrap = 
        my_type._FunctionWrappingType__functions_to_wrap = [
            
            ]
        
    def __getattr_
    