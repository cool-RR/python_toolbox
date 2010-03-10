# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
This module defines the get_lines function. See its documentation for more
info.
'''

def get_lines(start, end, thing):
    '''
    Get a list of all "round" numbers between start and end.
    
    with thing=0, round numbers = 1, 2, 3...
    with thing=1, round numbers = 10, 20, 30...
    with thing=-1, round numbers = 0.1, 0.2, 0.3...
    etc.
    '''
    mything = int(round(thing))
    mystart = round(start,mything)
    if mystart < start:
        mystart += 10 ** mything
    '''
    myend=round(end,-thing)
    if myend>end:
        myend-=10**thing
    '''

    result = []
    current = mystart
    while current < end:
        result.append(round(current, -mything))
        current += 10 ** mything
    return result
