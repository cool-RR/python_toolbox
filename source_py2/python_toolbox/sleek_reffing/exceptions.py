# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines exceptions.'''

from python_toolbox.exceptions import CuteException


class SleekRefDied(CuteException):
    '''You tried to access a sleekref's value but it's already dead.'''