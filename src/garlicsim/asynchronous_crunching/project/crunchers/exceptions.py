# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
This module defines the ObsoleteCruncherError exception. See its documentation
for more information.
"""

class ObsoleteCruncherError(Exception):
    """
    An error to raise when a cruncher is trying to do work, but in the meantime
    the main program decided that the work assigned to this cruncher is no
    longer wanted, and should therefore be stopped.
    """
    pass