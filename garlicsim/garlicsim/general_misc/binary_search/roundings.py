# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
A module for doing a binary search in a sequence.

Todo: wrap all things in tuples?

todo: add option to specify cmp.

todo: possibly change 'low' to class Low(RoundingOption).

todo: i think `binary_search_by_index` should have the core logic, and the other
one will use it. I think this will save many sequence accesses, and some
sequences can be expensive.
'''

class Rounding(object):
    #tododoc
    pass
    
class LOW(Rounding):
    pass
    
class HIGH(Rounding):
    pass
    
class EXACT(Rounding):
    pass
    
class CLOSEST(Rounding):
    pass

class BOTH(Rounding):
    pass
    
