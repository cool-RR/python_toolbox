class ObsoleteCruncherError(Exception):
    """
    An error to raise when a cruncher is trying to do work, but in the meantime
    the main program decided that work should be stopped.
    """
    pass