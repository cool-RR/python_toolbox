# Copyright 2009 Ram Rachum.
# This program is not licensed for distribution and may not be distributed.

def get_lines(start,end,thing):
    """
    returns a list of all "round" numbers between start and end
    with thing=0, round numbers = 1, 2, 3...
    with thing=1, round numbers = 10, 20, 30...
    with thing=-1, round numbers = 0.1, 0.2, 0.3...
    etc.
    """
    mything=int(round(thing))
    mystart=round(start,mything)
    if mystart<start:
        mystart+=10**mything
    """
    myend=round(end,-thing)
    if myend>end:
        myend-=10**thing
    """

    result=[]
    current=mystart
    while current<end:
        result+=[round(current,-mything)]
        current+=10**mything
    return result
