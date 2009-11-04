# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This package is a warehouse. For an explanation of what a warehouse is and how
it works, see documentation of garlicsim.general_mise.warehouse.create.

This is a warehouse of crunchers. What is a cruncher?

A cruncher is a worker which crunches the simulation. It receives a state from
the main program, and then it repeatedly applies the step function of the
simulation to produce more states. Those states are then put in the cruncher's
work_queue. They are then taken by the main program when Project.sync_crunchers
is called, and put into the tree.

The cruncher also receives a crunching profile from the main program. The
crunching profile specifes how far the cruncher should crunch the simulation,
and which arguments it should pass to the step function.

This warehouse may define different crunchers which work in different ways,
but are to a certain extent interchangable. Different kinds of crunchers have
different advantages and disadvantges relatively to each other, and which
cruncher you should use for your project depends on the situation. See the
documentation for the different crunchers for more info.
'''

import sys
from ...general_misc import warehouse

this_module = sys.modules[__name__]
crunchers = warehouse.create(this_module)




