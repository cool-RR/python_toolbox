# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

__all__ = ['simpack_name_cmp']

def leading_underscore_count(string):
    result = 0
    for char in string:
        if char == '_':
            result += 1
        else:
            break
    return result

def leading_underscore_cmp(a, b):
    return cmp(
        leading_underscore_count(a),
        leading_underscore_count(b)
    )

def simpack_name_cmp(a, b):
    assert isinstance(a, basestring) and isinstance(b, basestring)
    first_result = leading_underscore_cmp(a, b)
    if first_result != 0:
        return first_result
    return cmp(a, b)