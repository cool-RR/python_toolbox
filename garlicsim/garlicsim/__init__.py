# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
GarlicSim is a platform for writing, running and analyzing simulations.

It can handle any kind of simulation: Physics, game theory, epidemic spread,
electronics, etc.

Visit http://garlicsim.org for more info.

This package, called `garlicsim`, is the business logic. It is copyrighted to
Ram Rachum, 2009, and is distributed under the LGPL v2.1 License. The license
is included with this package as the file `lgpl2.1_license.txt`.

This licensing does not apply to `garlicsim_wx`, which is the associated GUI
package.

This program is intended for Python versions 2.5 and 2.6.
'''

from . import bootstrap
import general_misc
import general_misc.monkeypatch_copy_reg
import misc
from asynchronous_crunching import Project
from synchronous_crunching import simulate, list_simulate

__all__ = ["Project", "simulate", "list_simulate"]

__version__ = '0.5'

