# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing package for `exceptions.CuteException`.'''

from garlicsim.general_misc import cute_testing

from garlicsim.general_misc.exceptions import CuteBaseException, CuteException


def test():
        
    try:
        raise CuteException
    except Exception, exception:
        assert exception.message == ''
    else:
        raise cute_testing.Failure
        
    try:
        raise CuteException()
    except Exception, exception:
        assert exception.message == ''
    else:
        raise cute_testing.Failure
        
        
    class MyException(CuteException):
        '''My hovercraft is full of eels.'''
        
        
    try:
        raise MyException()
    except Exception, exception:
        assert exception.message == '''My hovercraft is full of eels.'''
    else:
        raise cute_testing.Failure
        
    try:
        raise MyException
    except Exception, exception:
        assert exception.message == '''My hovercraft is full of eels.'''
    else:
        raise cute_testing.Failure