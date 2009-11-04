# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This package defines objects for working with simulations that crunch
asynchronically, i.e. in a separate thread/process.

The most important class defined here is Project, and it is the only class
that the user needs to interact with. It employs all the other classes.
'''

from obsolete_cruncher_error import ObsoleteCruncherError
from history_browser import HistoryBrowser
from crunching_profile import CrunchingProfile
import crunchers_warehouse
from project import Project
from job import Job
from crunching_manager import CrunchingManager

__all__ = ["Project", "HistoryBrowser", "CrunchingManager", "Job",
           "crunchers_warehouse", "CrunchingProfile", "ObsoleteCruncherError"]

