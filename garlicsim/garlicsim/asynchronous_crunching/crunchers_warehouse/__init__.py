# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''TODOdOC
This package defines two crunchers, CruncherThread and CruncherProcess.
They work in a similar way, but they are based on threading.Thread
and multiprocessing.Process respectively.

A cruncher is a worker which crunches the simulation. It receives a state from
the main program, and then it repeatedly applies the step function of the
simulation to produce more states. Those states are then put in the cruncher's
work_queue. They are then taken by the main program when Project.sync_crunchers
is called, and put into the tree.

The cruncher also receives a crunching profile from the main program. The
crunching profile specifes how far the cruncher should crunch the simulation,
and which arguments it should pass to the step function.

The main reason there are two kinds of crunchers is that some simulations,
albeit a small minority of them, are history-dependent: They require access
to the history of the world in order to calculate the next step. This is very
hard to implement using Process, because information transfer between processes
is complicated. This is why CruncherThread was born, as threads share memory
trivially between them.

These are the advantages of CruncherThread:

    1. CruncherThread is able to handle simulations that are history-dependent.
    2. CruncherThread is based on the threading module, which is stabler and
       more mature than the multiprocessing module.
    3. CruncherThread is much easier to debug than CruncherProcess, since there
       are currently many more tools for debugging Python threads than Python
       processes.
    4. On a single-core computer, CruncherThread may be faster than
       CruncherProcess because of shared memory.

The advantage of CruncherProcess over CruncherThread is that CruncherProcess is
able to run on a different core of the processor in the machine, thus using the
full power of the processor.
'''

from ...general_misc import warehouse
from . import cruncher_process
crunchers = warehouse.create(__file__)




