# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various tools for comparisons.'''

import sys


def underscore_hating_key(string):
    '''Key function for sorting that treats `_` as last character.'''
    assert isinstance(string, str)
    return str(string).replace('_', chr(sys.maxunicode))


def process_key_function_or_attribute_name(key_function_or_attribute_name):
    '''
    Make a key function given either a key function or an attribute name.
    
    Some functions let you sort stuff by entering a key function or an
    attribute name by which the elements will be sorted. This function tells
    whether we were given a key function or an attribute name, and generates a
    key function out of it if needed.
    '''
    if key_function_or_attribute_name is None:
        return None
    elif callable(key_function_or_attribute_name):
        return key_function_or_attribute_name
    else:
        assert isinstance(key_function_or_attribute_name, basestring)
        return lambda key: getattr(key, key_function_or_attribute_name)



