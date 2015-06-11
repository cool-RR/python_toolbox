# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''A little module for cataloging strings.'''


_catalog = []


def string_to_integer(string):
    '''
    If the string isn't cataloged already, catalog it.
    
    In any case, returns the number associated with the string.
    '''
    global _catalog
    if string in _catalog:
        return _catalog.index(string) + 1
    else:
        _catalog.append(string)
        return _catalog.index(string) + 1


def integer_to_string(integer):
    '''Get the string cataloged under the given integer.'''
    return _catalog[integer - 1]
