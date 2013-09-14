# Copyright 2009-2013 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various tools for comparisons.'''

import sys


def underscore_hating_key(string):
    '''Key function for sorting that treats `_` as last character.'''
    assert isinstance(string, basestring)
    return unicode(string).replace('_', unichr(sys.maxunicode))


def total_ordering(cls): 
    '''
    Add full arsenal of ordering methods to a class based on existing subset.
    '''
    convert = {
        '__lt__': [('__gt__', lambda self, other:
                                  not (self < other or self == other)),
                   ('__le__', lambda self, other:
                                  self < other or self == other),
                   ('__ge__', lambda self, other:
                                  not self < other)],
        '__le__': [('__ge__', lambda self, other: 
                                  not self <= other or self == other),
                   ('__lt__', lambda self, other: 
                                  self <= other and not self == other),
                   ('__gt__', lambda self, other: 
                                  not self <= other)],
        '__gt__': [('__lt__', lambda self, other: 
                                  not (self > other or self == other)),
                   ('__ge__', lambda self, other: 
                                  self > other or self == other),
                   ('__le__', lambda self, other: 
                                  not self > other)],
        '__ge__': [('__le__', lambda self, other: 
                                  (not self >= other) or self == other),
                   ('__gt__', lambda self, other: 
                                  self >= other and not self == other),
                   ('__lt__', lambda self, other: 
                                  not self >= other)]
    }
    roots = set(dir(cls)) & set(convert)
    if not roots:
        raise ValueError('Must define at least one ordering operation: `<`, '
                         '`>`, `<=`, or `>=`.')
    root = max(roots) # We prefer __lt__ to __le__ to __gt__ to __ge__
    for opname, opfunc in convert[root]:
        if opname not in roots:
            opfunc.__name__ = opname
            opfunc.__doc__ = getattr(float, opname).__doc__
            setattr(cls, opname, opfunc)
    return cls


def process_key_function_or_attribute_name(key_function_or_attribute_name):
    '''
    Make a key function given either a key function or an attribute name.
    
    Some functions let you sort stuff by entering a key function or an
    attribute name by which the elements will be sorted. This function tells
    whether we were given a key function or an attribute name, and generates a
    key function out of it if needed.
    '''
    if key_function_or_attribute_name is None:
        return None
    elif callable(key_function_or_attribute_name):
        return key_function_or_attribute_name
    else:
        assert isinstance(key_function_or_attribute_name, basestring)
        return lambda key: getattr(key, key_function_or_attribute_name)



