# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
This is a bootstrap module for garlicsim_wx.

It checks all prerequisites are installed.
'''

import warnings

def __check_prerequisites():
    '''
    Check that all modules required for garlicsim_wx are installed.
    
    Returns a list of some imported modules: A reference to this list should be
    kept alive so to prevent the imported modules from being garbage-collected,
    which would cause Python to load them twice, which would needlessly increase
    startup time.
    '''
    
    modules = []
    
    class MissingModule(Exception):
        '''An error to raise when a required module is not found.'''
        pass
    
    def check_garlicsim():
        try:
            import garlicsim
            return [garlicsim]
        except ImportError:
            raise MissingModule('''garlicsim is \
required, but it's not currently installed on your system. Please find it \
online and install it, then try again.''')
        
    
    def check_wx():
        try:
            import wx
            if wx.__version__ < '2.8.10.1':
                warnings.warn('''You have wxPython version %s installed, \
while version 2.8.10.1 is needed. This program will try to run now, and if \
you're lucky it will work alright, but if any problem comes up, try upgrading \
wxPython. To do that, download and install the latest version from \
http://wxpython.org''' % wx.__version__)
            return [wx]
        except ImportError:
            raise MissingModule('''wxPython (version 2.8.10.1 and upwards) is \
required, but it's not currently installed on your system. Please find it \
online and install it, then try again.''')
    

    checkers = [check_garlicsim, check_wx]
    
    for checker in checkers:
        modules += checker()
    
    return modules

__modules_list = __check_prerequisites()
