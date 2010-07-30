# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import types

from garlicsim.general_misc import misc_tools



class FunctionAnchoringType(type):
    def __call__(self, name, bases, namespace_dict):
        my_type = super(type, self).__call__(self, name, bases, namespace_dict)
        my_getted_vars = misc_tools.getted_vars(my_type)
        functions_to_anchor = [value for value in my_getted_vars.itervalues()
                               if isinstance(value, types.FunctionType)]
        for function in functions_to_anchor:
            module_name = function.__module__
            module = __import__(function.__module__, fromlist=[''])
            function_name = function.__name__
            anchor_address = '.'.join(module_name, function_name)
            try:
                already_defined_object = \
                    misc_tools.get_object_from_address(anchor_address)
            except AttributeError:
                # Good, there is no object defined under our anchor address.
                # This is the normal case.
                setattr(module, function_name, function)
            else:
                # Something already exists at the anchor address; Let's be
                # careful.
                if already_defined_object is not function:
                    raise Exception # toododoc
        return my_type
                    
    