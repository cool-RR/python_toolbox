# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
GarlicSim is a platform for writing, running and analyzing simulations. It can
handle any kind of simulation: Physics, game theory, epidemic spread,
electronics, etc.

Visit http://garlicsim.com for more info.

This package, called `garlicsim`, is the business logic. It is copyrighted to
Ram Rachum, 2009, and is distributed under the LGPL v2.1 License. The license
is included with this package as the file `lgpl2.1_license.txt`.

This licensing does not apply to `garlicsim_wx`, which is the associated GUI
package.

todo: fix documentation everywhere to reflect that `touched` is now a node attribute.
"""

from asynchronous_crunching import Project
from synchronous_crunching import simulate, path_simulate

__all__ = ["Project", "simulate", "path_simulate"]