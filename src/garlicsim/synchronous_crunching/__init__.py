# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
The synchronous_crunching package defines functions for conducting simulations
with the crunching being done synchronously, i.e. in the main thread, without
recruiting any worker threads or worker processes.
"""

from simulate import simulate
from list_simulate import list_simulate

__all__ = ["simulate", "list_simulate"]