# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
A collection of crunchers, which are workers that crunch the simulation.

See also `garlicsim.asynchronous_crunching.base_cruncher.BaseCruncher` and its
documentation. It is the abstract base class for all of the crunchers here.

A cruncher receives a state from the main program, and then it repeatedly
applies the step function of the simulation to produce more states. Those states
are then put in the cruncher's `work_queue`. They are then taken by the main
program when `Project.sync_crunchers` is called, and put into the tree.

The cruncher also receives a crunching profile from the main program. The
crunching profile specifes how far the cruncher should crunch the simulation,
and which arguments it should pass to the step function.

This package may define different crunchers which work in different ways, but
are to a certain extent interchangable. Different kinds of crunchers have
different advantages and disadvantges relatively to each other, and which
cruncher you should use for your project depends on the situation.

See the documentation for the different crunchers for more info.
'''

from thread_cruncher import ThreadCruncher
try:
    from process_cruncher import ProcessCruncher
except ImportError:
    try:
        import multiprocessing
    except ImportError:
        import warnings
        warnings.warn("You don't have the multiprocessing package installed. "
                      "GarlicSim will run, but it won't be able to use "
                      "ProcessCruncher in order to take advantage of multiple "
                      "processor cores for crunching.")
    else:
        raise
