# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines tools for name-mangling.'''

from python_toolbox import string_tools

MANGLE_LEN = 256


def mangle_attribute_name_if_needed(attribute_name, class_name):

    # Ruling out four cases in which we do not mangle:
    if ((not attribute_name.startswith('__')) or
        (len(attribute_name) + 2 >= MANGLE_LEN) or
        (attribute_name.endswith('__')) or
        set(class_name) == set(('_',))):
        
        return attribute_name
    
    
    cleaned_class_name = class_name.lstrip('_')

    total_length = len(cleaned_class_name) + len(attribute_name)
    if total_length > MANGLE_LEN:
        cleaned_class_name = cleaned_class_name[:(MANGLE_LEN - total_length)]

    return '_%s%s' % (cleaned_class_name, attribute_name)


def will_attribute_name_be_mangled(attribute_name, class_name):
    
    return mangle_attribute_name_if_needed(attribute_name, class_name) != \
                                                                 attribute_name

def unmangle_attribute_name_if_needed(attribute_name, class_name):
    
    # Ruling out four cases in which mangling wouldn't have happened:
    if ((string_tools.get_n_identical_edge_characters(attribute_name,
                                                      '_') != 1) or
        (len(attribute_name) >= MANGLE_LEN) or
        (attribute_name.endswith('__')) or
        set(class_name) == set('_')):
        
        return attribute_name
    
    cleaned_class_name = class_name.lstrip('_')
    if not attribute_name[1:].startswith(cleaned_class_name + '__'):
        return attribute_name
    
    return attribute_name[(len(cleaned_class_name) + 1):]
