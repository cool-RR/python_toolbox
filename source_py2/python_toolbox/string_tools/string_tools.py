# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines string-related tools.'''

import sys
import re
import itertools


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


def get_n_identical_edge_characters(string, character=None, head=True):
    '''
    Get the number of identical characters at `string`'s head.
    
    For example, the result for 'qqqwe' would be `3`, while the result for
    'meow' will be `1`.
    
    Specify `character` to only consider that character; if a different
    character is found at the head, `0` will be returned.
    
    Specify `head=False` to search the tail instead of the head.
    '''
    from python_toolbox import cute_iter_tools
    
    if not string:
        return 0
    found_character, character_iterator = next(
        itertools.groupby(string if head else reversed(string))
    )
    if (character is not None) and found_character != character:
        assert isinstance(character, str) and len(character) == 1
        return 0
    return cute_iter_tools.get_length(character_iterator)
    

def rreplace(s, old, new, count=None):
    '''
    Replace instances of `old` in `s` with `new`, starting from the right.
    
    This function is to `str.replace` what `str.rsplit` is to `str.split`.
    '''
    return new.join(s.rsplit(old, count) if count is not None
                    else s.rsplit(old))
    