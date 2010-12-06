# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import sys
import types

from garlicsim.general_misc import misc_tools
from garlicsim.general_misc import import_tools



class FunctionAnchoringType(type):
    # tododoc: consider putting this only in _py3
    def __new__(mcls, name, bases, namespace_dict):
        my_type = super(FunctionAnchoringType, mcls).__new__(mcls,
                                                             name,
                                                             bases,
                                                             namespace_dict)
        my_getted_vars = misc_tools.getted_vars(my_type)
        functions_to_anchor = [value for value in my_getted_vars.itervalues()
                               if isinstance(value, types.FunctionType)]
        for function in functions_to_anchor:
            module_name = function.__module__
            module = sys.modules[module_name]
            function_name = function.__name__
            anchor_address = '.'.join((module_name, function_name))
            try:
                # tododoc: fucking shit here
                already_defined_object = \
                    misc_tools.get_object_from_address(anchor_address)
            except AttributeError:
                # Good, there is no object defined under our anchor address.
                # This is the normal case.
                setattr(module, function_name, function)
            else:
                # Something already exists at the anchor address; let's be
                # careful.
                if already_defined_object is not function:
                    raise Exception # toododoc
        return my_type
                    
    