# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''This module defines string-related tools.'''

import sys
import re


def camelcase_to_underscore(s):
    '''
    Convert a string from camelcase to underscore.
    
    Example: camelcase_to_underscore('HelloWorld') == 'hello_world'
    '''
    return re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', s).\
           lower().strip('_')


def camelcase_to_spacecase(s):
    '''
    Convert a string from camelcase to spacecase.
    
    Example: camelcase_to_underscore('HelloWorld') == 'Hello world'
    '''
    if s == '': return s
    character_process = lambda c: (' ' + c.lower()) if c.isupper() else c
    return s[0] + ''.join(character_process(c) for c in s[1:])


def docstring_trim(docstring):
    '''Trim a docstring, removing redundant tabs.'''
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
        
    return '\n'.join(trimmed)
    