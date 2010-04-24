# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines functions for conducting simulations with synchronous crunching.

This means that the crunching is done in the main thread, without recruiting any
worker threads or worker processes.
'''

from simulate import simulate
from list_simulate import list_simulate
from history_browser import HistoryBrowser

__all__ = ["simulate", "list_simulate", "HistoryBrowser"]