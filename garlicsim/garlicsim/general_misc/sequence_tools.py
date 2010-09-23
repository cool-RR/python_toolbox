
def heads(sequence, include_empty=False, include_full=True):    
    for i in range(0 if include_empty else 1, len(sequence)):
        yield sequence[:i]
    if include_full:
        yield sequence[:]
        
        