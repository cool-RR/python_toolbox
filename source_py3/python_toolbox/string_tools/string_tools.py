# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines string-related tools.'''

import sys
import re


def docstring_trim(docstring):
    '''Trim a docstring, removing redundant tabs.'''
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxsize
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxsize:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
        
    return '\n'.join(trimmed)


def get_n_identical_edge_characters(string, character=None, head=True):
    '''
    Get the number of identical characters at `string`'s head.
    
    For example, the result for 'qqqwe' would be `3`, while the result for
    'meow' will be `1`.
    
    Specify `character` to only consider that character; if a different
    character is found at the head, `0` will be returned.
    
    Specify `head=False` to search the tail instead of the head.
    '''
    if not string:
        return 0
    index = 0 if head is True else -1
    direction = 1 if head is True else -1
    if character is None:
        character = string[index]
    else:
        assert isinstance(character, str) and len(character) == 1
    for i, c in enumerate(string[::direction]):
        if c != character:
            return i
    else:
        return len(string)