# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

class ObsoleteCruncherError(Exception):
    """
    An error to raise when a cruncher is trying to do work, but in the meantime
    the main program decided that work should be stopped.
    """
    pass