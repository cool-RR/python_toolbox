# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the simpack_name_cmp function.

See its documentation for more info.
'''



__all__ = ['simpack_name_cmp']

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

def simpack_name_cmp(a, b):
    '''Compare which simpack has a "higher" name.'''
    assert isinstance(a, basestring) and isinstance(b, basestring)
    first_result = _leading_underscore_cmp(a, b)
    if first_result != 0:
        return first_result
    return cmp(a, b)