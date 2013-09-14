# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines functions for converting between different string conventions.'''

import sys
import re


def camelcase_to_underscore(string):
    '''
    Convert a string from camelcase to underscore.
    
    Example: camelcase_to_underscore('HelloWorld') == 'hello_world'
    '''
    return re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', string).\
           lower().strip('_')


def camelcase_to_spacecase(string):
    '''
    Convert a string from camelcase to spacecase.
    
    Example: camelcase_to_underscore('HelloWorld') == 'Hello world'
    '''
    if string == '': return string
    process_character = lambda c: (' ' + c.lower()) if c.isupper() else c
    return string[0] + ''.join(process_character(c) for c in string[1:])