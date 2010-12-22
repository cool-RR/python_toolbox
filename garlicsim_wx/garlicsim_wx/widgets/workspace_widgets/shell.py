# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the `Shell` class.

See its documentation for more info.
'''

import wx.py.shell

from garlicsim_wx.widgets import WorkspaceWidget
import garlicsim
import garlicsim_wx


class Shell(wx.py.shell.Shell, WorkspaceWidget):
    '''
    A shell widget, allowing to execute arbitrary Python code.
    
    This is useful for examining the simulation.
    '''
    # todo: After every command in shell, must make the top emitter emit
    def __init__(self, frame):
        wx.py.shell.Shell.__init__(self, frame, size=(100, 100),
                                   locals=frame.gui_project.namespace,
                                   style=wx.SUNKEN_BORDER)
        WorkspaceWidget.__init__(self, frame)
        
        # Obscure:
        import site; del site
        # This causes the `site` module to add `help` and a few others
        # to `__builtin__`. For some reason `site` isn't imported when frozen
        # with py2exe, so here we make sure to import it.
        
    
    def setLocalShell(self):
        # Making it a no-op to avoid reference to retarded `ShellFacade`.
        pass