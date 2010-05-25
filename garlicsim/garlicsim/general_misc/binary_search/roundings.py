# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines different rounding options for binary search.'''

# Confirm that *_IF_BOTH options are used are used in all places that currently
# ~use them.

class Rounding(object):
    '''Base class for rounding options for binary search.'''


    
class BOTH(Rounding):
    '''
    Get a tuple (low, high) of the two items that surround the specified value.
    
    If there's an exact match, gives it twice in the tuple, i.e. (match, match).
    '''
    
class EXACT(Rounding):
    '''Get the item which has exactly the same value has the specified value.'''
    
class CLOSEST(Rounding):
    '''Get the item which has a value closest to the specified value.'''
    
class LOW(Rounding):
    '''
    Get the item with a value that is just below the specified value.
    
    i.e. the highest item which has a value lower or equal to the specified
    value.
    '''
    
class HIGH(Rounding):
    '''
    Get the item with a value that is just above the specified value.
    
    i.e. the lowest item which has a value higher or equal to the specified
    value.
    '''

class LOW_IF_BOTH(Rounding):
    '''
    Get the item with a value that is just below the specified value.
    
    i.e. the highest item which has a value lower or equal to the specified
    value.
    
    Before it returns the item, it checks if there also exists an item with a
    value *higher* than the specified value. If there isn't, it returns None.
    '''
    
class HIGH_IF_BOTH(Rounding):
    '''
    Get the item with a value that is just above the specified value.
    
    i.e. the lowest item which has a value higher or equal to the specified
    value.
    
    Before it returns the item, it checks if there also exists an item with a
    value *lower* than the specified value. If there isn't, it returns None.
    '''
    
class CLOSEST_IF_BOTH(Rounding):
    '''
    Get the item which has a value closest to the specified value.
    
    Before it returns the item, it checks if there also exists an item which is
    "on the other side" of the specified value. e.g. if the closest item is
    higher than the specified item, it will confirm that there exists an item
    *below* the specified value. (And vice versa.) If there isn't it returns
    None.
    '''
    
class LOW_OTHERWISE_HIGH(Rounding):
    '''
    Get the item with a value that is just below the specified value.
    
    i.e. the highest item which has a value lower or equal to the specified
    value.
    
    If there is no item below, give the one just above.
    '''
    
class HIGH_OTHERWISE_LOW(Rounding):
    '''
    Get the item with a value that is just above the specified value.
    
    i.e. the lowest item which has a value higher or equal to the specified
    value.
    
    If there is no item above, give the one just below.
    '''

roundings = (LOW, LOW_IF_BOTH, LOW_OTHERWISE_HIGH, HIGH, HIGH_IF_BOTH,
             HIGH_OTHERWISE_LOW, EXACT, CLOSEST, CLOSEST_IF_BOTH, BOTH)
