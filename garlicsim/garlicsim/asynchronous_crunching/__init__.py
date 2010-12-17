# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines objects for working with simulations that crunch asynchronically.

(Asynchronously means in a separate thread/process/computer.)

The most important class defined here is `Project`, and it is the only class
that the user needs to interact with. It employs all the other classes.
'''

from .obsolete_cruncher_error import ObsoleteCruncherError
from .history_browser import HistoryBrowser
from .crunching_profile import CrunchingProfile
from .base_cruncher import BaseCruncher
from . import crunchers
from .project import Project
from .job import Job
from .crunching_manager import CrunchingManager

