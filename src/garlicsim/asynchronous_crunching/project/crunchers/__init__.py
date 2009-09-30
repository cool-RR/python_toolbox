# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
This package defines two crunchers, CruncherThread and CruncherProcess.
They work in a similar way, but they are based on threading.Thread
and multiprocessing.Process respectively.

A cruncher is a dumb little drone. It receives a state from the main program,
and then it repeatedly applies the step funcion of the simulation to produce
more states. Those states are then put in the cruncher's work_queue. They
are then taken by the main program when Project.sync_crunchers is called,
and put into the tree.

The main reason there are two kinds of crunchers is that some simulations,
albeit a small minority of them, are history-dependent: They require access
to the history of the world in order to calculate the next step. This is very
hard to implement using Process, because information transfer between processes
is complicated. This is why CruncherThread was born, as threads share memory
trivially between them.

Another reason for CruncherThread is that on single-core computer it might
be faster than CruncherProcess because of the memory-sharing.
"""

from cruncher_thread import CruncherThread
from cruncher_process import CruncherProcess
from exceptions import ObsoleteCruncherError

__all__ = ["CruncherProcess", "CruncherThread", "ObsoleteCruncherError"]