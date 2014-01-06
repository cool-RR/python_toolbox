# Copyright 2009-2014 Ram Rachum.
# This program is distributed under the MIT license.

'''This module defines miscellaneous tools.'''

from .misc_tools import (
    is_subclass, get_mro_depth_of_method, frange, getted_vars,
    _ascii_variable_pattern, is_legal_ascii_variable_name,
    is_magic_variable_name, get_actual_type, is_number, identity_function,
    do_nothing, OwnNameDiscoveringDescriptor, find_clear_place_on_circle,
    general_sum, general_product, is_legal_email_address, is_type, NonInstatiable,
    repeat_getattr, add_extension_if_plain
)
from . import name_mangling
from .proxy_property import ProxyProperty