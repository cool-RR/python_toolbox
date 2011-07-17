# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `ObsoleteCruncherException` exception.

See its documentation for more info.
'''

from garlicsim.general_misc.exceptions import CuteBaseException


class ObsoleteCruncherException(CuteBaseException):
    '''
    The cruncher became obsolete; we don't need it do no any more crunching.
    
    The cruncher is trying to do work, but in the meantime the main program
    decided that the work assigned to this cruncher is no longer wanted, and
    should therefore be stopped.
    '''
    # Inherits from `CuteBaseException` rather than `CuteException` because it
    # is an exit exception.
