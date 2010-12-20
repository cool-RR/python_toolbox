# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines various tools for manipulating sequences.'''

        
def are_equal_regardless_of_order(seq1, seq2):
    '''
    Return whether the two sequences are equal in the elements they contain,
    regardless of the order of the elements.
    
    Currently will fail for items that have problems with comparing.
    '''
    return sorted(seq1) == sorted(seq2)
        

def flatten(iterable):
    '''
    Flatten a sequence, returning a sequence of all its items' items.
    
    For example, `flatten([[1, 2], [3], [4, 'meow']]) == [1, 2, 3, 4, 'meow']`.
    '''
    
    iterator = iter(iterable)
    try:
        first_item = iterator.next()
    except StopIteration:
        return []
    return sum(iterator, first_item)


### Not using now, might want in future:

#def is_sequence(thing):
    #return hasattr(thing, '__len__') and hasattr(thing, '__getitem__') and\
    #hasattr(thing, '__iter__') and 
    #pass

#def heads(sequence, include_empty=False, include_full=True):    
    #for i in range(0 if include_empty else 1, len(sequence)):
        #yield sequence[:i]
    #if include_full:
        #yield sequence[:]