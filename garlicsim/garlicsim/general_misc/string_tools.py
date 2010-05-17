# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''This module defines string-related tools.'''


import re


def camelcase_to_underscore(s):
    '''
    Convert a string from camelcase to underscore.
    
    Example: camelcase_to_underscore('HelloWorld') == 'hello_world'
    '''
    return re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', s).lower().strip('_')


def camelcase_to_spacecase(s):
    '''
    Convert a string from camelcase to spacecase.
    
    Example: camelcase_to_underscore('HelloWorld') == 'Hello world'
    '''
    if s == '': return s
    character_process = lambda c: (' ' + c.lower()) if c.isupper() else c
    return s[0] + ''.join(character_process(c) for c in s[1:])

"""
def underscore_to_camelcase(s):
    raise NotImplementedError
"""

