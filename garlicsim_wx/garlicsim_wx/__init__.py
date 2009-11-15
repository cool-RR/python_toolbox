# Copyright 2009 Ram Rachum. No part of this program may be used, copied or
# distributed without explicit written permission from Ram Rachum.

'''
This is garlicsim_wx, a wxPython GUI for GarlicSim.

The final goal of this project is to become a fully-fledged application for
working with simulations, friendly enough that it may be used by
non-programmers.
'''

###############################################################################
###  Checking for prerequisites:
###############################################################################

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
    
    def check_wx():
        try:
            import wx
            return [wx]
        except ImportError:
            raise MissingModule('''wxPython is \
required, but it's not currently installed on your system. Please find it \
online and install it, then try again.''')
    

    checkers = [check_distribute, check_garlicsim, check_wx]
    
    for checker in checkers:
        modules += checker()
    
    return modules

__modules_list = __check_prerequisites()

########################## Done checking for prerequisites





import wx

from application_window import ApplicationWindow
from gui_project import GuiProject

def start():
    '''
    Start the gui.
    '''
    app = wx.PySimpleApp()
    my_app_win = ApplicationWindow(None, -1, "GarlicSim", size=(600, 600))

    '''
    import cProfile
    cProfile.run("app.MainLoop()")
    '''
    app.MainLoop()
    
if __name__ == "__main__":
    start()