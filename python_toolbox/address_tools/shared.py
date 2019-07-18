# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Various objects and tools for `address_tools`.'''

import re


_address_pattern = re.compile(
    r"^(?P<address>([a-zA-Z_][0-9a-zA-Z_]*)(\.[a-zA-Z_][0-9a-zA-Z_]*)*)$"
)
'''Pattern for Python addresses, like 'email.encoders'.'''


_contained_address_pattern = re.compile(
    r"(?P<address>([a-zA-Z_][0-9a-zA-Z_]*)(\.[a-zA-Z_][0-9a-zA-Z_]*)*)"
)
'''
Pattern for strings containing Python addresses, like '{email.encoders: 1}'.
'''


def _get_parent_and_dict_from_namespace(namespace):
    '''
    Extract the parent object and `dict` from `namespace`.

    For the `namespace`, the user can give either a parent object
    (`getattr(namespace, address) is obj`) or a `dict`-like namespace
    (`namespace[address] is obj`).

    Returns `(parent_object, namespace_dict)`.
    '''

    if hasattr(namespace, '__getitem__') and hasattr(namespace, 'keys'):
        parent_object = None
        namespace_dict = namespace

    else:
        parent_object = namespace
        namespace_dict = vars(parent_object)

    return (parent_object, namespace_dict)


def is_address(string):
    return bool(_address_pattern.match(string))