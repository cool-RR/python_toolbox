# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Bootstrap module for `garlicsim_wx`.

It checks all prerequisites are installed.
'''

import warnings
import sys


### Confirming correct Python version: ########################################
#                                                                             #
if sys.version_info[0] >= 3:
    raise Exception('This package is not compatible with Python 3.x.')
if sys.version_info[1] <= 4:
    raise Exception('This package requires Python 2.5 and upwards. (Not '
                    'including 3.x).')
#                                                                             #
### Finished confirming correct Python version. ###############################


def __check_prerequisites():
    '''
    Check that all modules required for `garlicsim_wx` are installed.
    
    Returns a list of some imported modules: A reference to this list should be
    kept alive so to prevent the imported modules from being garbage-collected,
    which would cause Python to load them twice, which would needlessly
    increase startup time.
    '''
    
    modules = []
    
    class MissingModule(Exception):
        '''A required module is not found.'''
    
    def check_garlicsim():
        try:
            import garlicsim
        except ImportError:
            raise MissingModule("`garlicsim` is required, but it's not "
                                "currently installed on your system. Go to "
                                "http://garlicsim.org and follow the "
                                "instructions for installation.")
        else:
            if garlicsim.__version_info__ < (0, 6, 3):
                raise MissingModule("You have `garlicsim` version %s, while "
                                    "version 0.6.3 is required. Go to "
                                    "http://garlicsim.org and follow the "
                                    "instructions for installation." %
                                    (garlicsim.__version_info__,))
            return [garlicsim]
    
    def check_wx():
        try:
            import wx
            
        except ImportError:
            raise MissingModule("wxPython (version 2.8.10.1 and upwards, but "
                                "lower than 2.9) is required, but it's not "
                                "currently installed on your system. Please "
                                "go download it at http://wxpython.org, "
                                "install it, then try again.")
        
        else:
            wx_version = tuple(int(x) for x in wx.__version__.split('.'))
            if not ((2, 8, 10, 1) <= wx_version < (2, 9, 1, 1)):
                warnings.warn("You have wxPython version %s installed, while "
                              "version 2.8.10.1 or higher (but lower than "
                              "2.9) is needed. This program will try to run "
                              "now, and if you're lucky it will work alright, "
                              "but if any problem comes up, try upgrading "
                              "wxPython. To do that, download and install the "
                              "latest version from "
                              "http://wxpython.org" % (wx.__version__,))
            return [wx]
    

    checkers = [check_garlicsim, check_wx]
    
    for checker in checkers:
        modules += checker()
    
    return modules

__modules_list = __check_prerequisites()