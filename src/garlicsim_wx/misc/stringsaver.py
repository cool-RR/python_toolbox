# Copyright 2009 Ram Rachum.
# This program is not licensed for distribution and may not be distributed.

"""
A little module for cataloging strings.
"""

stringsaver_catalog=[]

def s2i(string):
    """
    If the string isn't cataloged already, catalogs it.
    In any case, returns the number associated with the string
    """
    global stringsaver_catalog
    if string in stringsaver_catalog:
        return stringsaver_catalog.index(string) + 1
    else:
        stringsaver_catalog+=[string]
        return stringsaver_catalog.index(string) + 1


def i2s(integer):
    """
    Returns the string cataloged under the given integer
    """
    return stringsaver_catalog[integer - 1]
