# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines different rounding options for binary search.'''


class Rounding(object):
    '''Base class for rounding options for binary search.'''
    
class LOW(Rounding):
    '''
    Get the highest item which has a value lower or equal to the specified value.
    '''
    
class HIGH(Rounding):
    '''
    Get the lowest item which has a value higher or equal to the specified value.
    '''
    
class EXACT(Rounding):
    '''Get the item which has exactly the same value has the specified value.'''
    
class CLOSEST(Rounding):
    '''Get the item which has a value closest to the specified value.'''

class BOTH(Rounding):
    '''
    Get a tuple (low, high) of the two items that surround the specified value.
    
    If there's an exact match, gives it twice in the tuple, i.e. (match, match).
    '''
    
