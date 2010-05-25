# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines a collection of exceptions.'''

from garlicsim.general_misc.exceptions import CuteException

class GarlicSimException(CuteException):
    '''GarlicSim-related exception.'''

class GarlicSimWarning(Warning):
    '''GarlicSim-related warning.'''
    

class InvalidSimpack(GarlicSimException):
    '''Trying to load an invalid simpack.'''

class SimpackError(GarlicSimException):
    '''A simpack behaved unexpectedly.'''
    
class WorldEnd(GarlicSimException):
    '''The simulation has ended.'''

    
    