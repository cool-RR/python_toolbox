


def heads(sequence, include_empty=False, include_full=True):    
    for i in range(0 if include_empty else 1, len(sequence)):
        yield sequence[:i]
    if include_full:
        yield sequence[:]
        
def are_equal_regardless_of_order(seq1, seq2):
    # Will fail for items that have problems with comparing
    return sorted(seq1) == sorted(seq2)
        

def flatten(iterable):
    iterator = iter(iterable)
    try:
        first_item = iterator.next()
    except StopIteration:
        return []
    type_ = type(first_item)
    return sum(iterator, first_item)