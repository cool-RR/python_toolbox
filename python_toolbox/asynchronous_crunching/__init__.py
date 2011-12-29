# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines objects for working with simulations that crunch asynchronically.

(Asynchronously means in a separate thread/process/computer.)

The most important class defined here is `Project`, and it is the only class
that the user needs to interact with. It employs all the other classes.
'''

from .obsolete_cruncher_error import ObsoleteCruncherException
from .history_browser import HistoryBrowser
from .crunching_profile import CrunchingProfile
from .base_cruncher import BaseCruncher
from . import crunchers
from .project import Project
from .job import Job
from .crunching_manager import CrunchingManager


CRUNCHER_QUEUE_SIZE = 100
'''
The `max_size` given to the crunchers' work queues.

This is needed for simpacks with very fast step functions, because without a
`max_size` the cruncher might work so fast that the GUI will never catch up
with it.
'''