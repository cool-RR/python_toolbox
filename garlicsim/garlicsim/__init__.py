# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
GarlicSim is a platform for writing, running and analyzing simulations.

It can handle any kind of simulation: Physics, game theory, epidemic spread,
electronics, etc.

Visit http://garlicsim.org for more info.

This package, called `garlicsim`, is the business logic. It is copyrighted to
Ram Rachum, 2009-2011, and is distributed under the LGPL v2.1 License. The
license is included with this package as the file `lgpl2.1_license.txt`.

This licensing does not apply to `garlicsim_wx`, which is the associated GUI
package.

This program is intended for Python versions 2.5, 2.6 and 2.7.
'''

import garlicsim.bootstrap
import garlicsim.general_misc
import garlicsim.general_misc.version_info
import garlicsim.general_misc.monkeypatch_copy_reg
import garlicsim.misc
from garlicsim.asynchronous_crunching import Project
from garlicsim.synchronous_crunching import (simulate, list_simulate,
                                             iter_simulate)


__all__ = ['Project', 'simulate', 'list_simulate', 'iter_simulate']


__version_info__ = garlicsim.general_misc.version_info.VersionInfo(0, 6, 2)
__version__ = '0.6.2'

