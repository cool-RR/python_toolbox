# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
GarlicSim is a platform for writing, running and analyzing simulations. It can
handle any kind of simulation: Physics, game theory, epidemic spread,
electronics, etc.

Visit http://garlicsim.org for more info.

This package, called `garlicsim`, is the business logic. It is copyrighted to
Ram Rachum, 2009, and is distributed under the LGPL v2.1 License. The license
is included with this package as the file `lgpl2.1_license.txt.py`.

This licensing does not apply to `garlicsim_wx`, which is the associated GUI
package.
'''



###############################################################################
###  Checking for prerequisites:
###############################################################################

def __check_prerequisites():
    '''
    Check that all modules required for garlicsim are installed.
    
    Returns a list of some imported modules: A reference to this list should be
    kept alive so to prevent the imported modules from being garbage-collected,
    which would cause Python to load them twice, which would needlessly increase
    startup time.
    '''
    
    modules = []
    
    class MissingModule(Exception):
        '''An error to raise when a required module is not found.'''
        pass
    
    def check_distribute():
        try:
            import pkg_resources
            modules.append(pkg_resources)
            assert pkg_resources.require('Distribute >= 0.6')
        except (ImportError, pkg_resources.DistributionNotFound, AssertionError):
            raise MissingModule('''Distribute (version 0.6 and upwards) is \
required, but it's not currently installed on your system. Please find it \
online and install it, then try again.''')
        return [pkg_resources]
    
    modules += check_distribute()
    
    return modules

__modules_list = __check_prerequisites()




###############################################################################
###  Importing:
###############################################################################

import general_misc
import misc
from asynchronous_crunching import Project
from synchronous_crunching import simulate, list_simulate

__all__ = ["Project", "simulate", "list_simulate"]

__version__ = '0.1'

