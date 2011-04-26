# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines various tools for comparisons.'''
# blocktodo: rename to `comparison_tools`
import sys


def underscore_hating_cmp(a, b):
    '''Compare two strings, counting the "_" character as highest.'''
    assert isinstance(a, basestring) and isinstance(b, basestring)
    return cmp(
        unicode(a).replace('_', unichr(sys.maxunicode)),
        unicode(b).replace('_', unichr(sys.maxunicode))
    )



# Commented out until I make a version that doesn't suck:

#def total_ordering(cls): 
    #'''
    #Add full arsenal of ordering methods to a class based on existing subset.
    #'''
    #convert = {
        #'__lt__': [('__gt__', lambda self, other: other < self),
                   #('__le__', lambda self, other: not other < self),
                   #('__ge__', lambda self, other: not self < other)],
        #'__le__': [('__ge__', lambda self, other: other <= self),
                   #('__lt__', lambda self, other: not other <= self),
                   #('__gt__', lambda self, other: not self <= other)],
        #'__gt__': [('__lt__', lambda self, other: other > self),
                   #('__ge__', lambda self, other: not other > self),
                   #('__le__', lambda self, other: not self > other)],
        #'__ge__': [('__le__', lambda self, other: other >= self),
                   #('__gt__', lambda self, other: not other >= self),
                   #('__lt__', lambda self, other: not self >= other)]
    #}
    #roots = set(dir(cls)) & set(convert)
    #if not roots:
        #raise ValueError('Must define at least one ordering operation: `<`, '
                         #'`>`, `<=`, or `>=`.')
    #root = max(roots) # We prefer __lt__ to __le__ to __gt__ to __ge__
    #for opname, opfunc in convert[root]:
        #if opname not in roots:
            #opfunc.__name__ = opname
            #opfunc.__doc__ = getattr(float, opname).__doc__
            #setattr(cls, opname, opfunc)
    #return cls
