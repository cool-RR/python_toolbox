# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
A little module for cataloging strings.
'''
# blocktodo: go over this and ensure minimal crap

catalog = []

def s2i(string):
    '''
    If the string isn't cataloged already, catalog it.
    
    In any case, returns the number associated with the string.
    '''
    global catalog
    if string in catalog:
        return catalog.index(string) + 1
    else:
        catalog.append(string)
        return catalog.index(string) + 1


def i2s(integer):
    '''Get the string cataloged under the given integer.'''
    return catalog[integer - 1]
