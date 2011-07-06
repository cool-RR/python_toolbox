# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''This module defines miscellaneous tools.'''

from .misc_tools import (
    is_subclass, get_mro_depth_of_method, frange, getted_vars,
    _ascii_variable_pattern, is_legal_ascii_variable_name,
    is_magic_variable_name, get_actual_type, is_number, identity_function,
    do_nothing, OwnNameDiscoveringProperty
)
from . import name_mangling