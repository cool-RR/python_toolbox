# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines various tools for comparisons.'''


__all__ = ['underscore_hating_cmp']


def underscore_hating_cmp(a, b):
    '''Compare two strings, counting the "_" character as highest.'''
    assert isinstance(a, basestring) and isinstance(b, basestring)
    first_result = _leading_underscore_cmp(a, b)
    if first_result != 0:
        return first_result
    return cmp(a, b)


def _leading_underscore_count(string):
    '''Count the number of leading underscores that a string has.'''
    result = 0
    for char in string:
        if char == '_':
            result += 1
        else:
            break
    return result


def _leading_underscore_cmp(a, b):
    '''Compare which string has more leading underscores.'''
    return cmp(
        _leading_underscore_count(a),
        _leading_underscore_count(b)
    )

