# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines various tools for manipulating sequences.'''

import itertools

from garlicsim.general_misc.nifty_collections import Counter

        
def are_equal_regardless_of_order(seq1, seq2):
    '''
    Return whether the two sequences are equal in the elements they contain,
    regardless of the order of the elements.
    
    Currently will fail for items that have problems with comparing.
    '''
    return Counter(seq1) == Counter(seq2)
        

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


def combinations(sequence, n=None, start=0):
    '''
    Iterate over combinations of items from the sequence.

    `n` specifies the number of items. (Use `None` for all possible sizes
    together.) `start` specifies the index number of the member from which to
    start giving combinations. (Keep the default of `start=0` for doing the
    whole sequence.)
    
    Example:
    
    `combinations([1, 2, 3, 4], n=2)` would be, in list form: `[[1, 2], [1, 3],
    [1, 4], [2, 3], [2, 4], [3, 4]]`.
    '''
    
    if n is None:
        length = len(sequence) - start
        iterators = (combinations(sequence, n=i, start=start) for i
                     in xrange(1, length + 1))
        for item in itertools.chain(*iterators):
            yield item
        
    elif n == 1:
        for thing in itertools.islice(sequence, start, None):
            yield [thing]
    else:
        assert n > 1
        for (i, thing) in itertools.islice(enumerate(sequence), start, None):
            for sub_result in combinations(sequence, n - 1, start=(i + 1)):
                yield [thing] + sub_result


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