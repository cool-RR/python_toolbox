# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
A module defining a collection of exceptions.
'''

class InvalidSimpack(Exception):
    '''
    An exception to raise when trying to load an invalid simpack.
    '''
    pass

class SimpackError(Exception):
    '''
    An exception to raise when a simpack behaves unexpectedly.
    '''
    pass

class GarlicSimWarning(Warning):
    '''
    GarlicSim-related warning.
    '''
    
    