# Copyright 2009 Ram Rachum. No part of this program may be used, copied or
# distributed without explicit written permission from Ram Rachum.

'''
A little module for cataloging strings.
'''

stringsaver_catalog=[]

def s2i(string):
    '''
    If the string isn't cataloged already, catalogs it.
    In any case, returns the number associated with the string
    '''
    global stringsaver_catalog
    if string in stringsaver_catalog:
        return stringsaver_catalog.index(string) + 1
    else:
        stringsaver_catalog+=[string]
        return stringsaver_catalog.index(string) + 1


def i2s(integer):
    '''
    Returns the string cataloged under the given integer
    '''
    return stringsaver_catalog[integer - 1]
