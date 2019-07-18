# Copyright 2009-2017 Ram Rachum.
# This program is distributed under the MIT license.

'''Testing package for `exceptions.CuteException`.'''

from python_toolbox import cute_testing

from python_toolbox.exceptions import CuteBaseException, CuteException


def test():

    try:
        raise CuteException
    except Exception as exception:
        assert exception.message == ''
    else:
        raise cute_testing.Failure

    try:
        raise CuteException()
    except Exception as exception:
        assert exception.message == ''
    else:
        raise cute_testing.Failure


    class MyException(CuteException):
        '''My hovercraft is full of eels.'''


    try:
        raise MyException()
    except Exception as exception:
        assert exception.message == '''My hovercraft is full of eels.'''
    else:
        raise cute_testing.Failure

    try:
        raise MyException
    except Exception as exception:
        assert exception.message == '''My hovercraft is full of eels.'''
    else:
        raise cute_testing.Failure