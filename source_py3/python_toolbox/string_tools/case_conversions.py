# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines functions for converting between different string conventions.'''

import sys
import re


def camel_case_to_space_case(s):
    '''
    Convert a string from camelcase to spacecase.
    
    Example: camelcase_to_underscore('HelloWorld') == 'Hello world'
    '''
    if s == '': return s
    process_character = lambda c: (' ' + c.lower()) if c.isupper() else c
    return s[0] + ''.join(process_character(c) for c in s[1:])


def camel_case_to_lower_case(s):
    '''
    Convert a string from camel-case to lower-case.
    
    Example: 
    
        camel_case_to_lower_case('HelloWorld') == 'hello_world'
        
    '''
    return re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', s). \
           lower().strip('_')


def lower_case_to_camel_case(s):
    '''
    Convert a string from lower-case to camel-case.
    
    Example: 
    
        camel_case_to_lower_case('hello_world') == 'HelloWorld'
        
    '''
    s = s.capitalize()
    while '_' in s:
        head, tail = s.split('_', 1)
        s = head + tail.capitalize()
    return s


def camel_case_to_upper_case(s):
    '''
    Convert a string from camel-case to upper-case.
    
    Example: 
    
        camel_case_to_lower_case('HelloWorld') == 'HELLO_WORLD'
        
    '''
    return camel_case_to_lower_case(s).upper()


def upper_case_to_camel_case(s):
    '''
    Convert a string from upper-case to camel-case.
    
    Example: 
    
        camel_case_to_lower_case('HELLO_WORLD') == 'HelloWorld'
        
    '''
    return lower_case_to_camel_case(s.lower())
