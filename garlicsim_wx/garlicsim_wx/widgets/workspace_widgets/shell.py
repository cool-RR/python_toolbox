# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.


import wx.py.shell
from garlicsim_wx.widgets import WorkspaceWidget
import garlicsim
import garlicsim_wx

__all__ = ["Shell"]

class Shell(wx.py.shell.Shell, WorkspaceWidget):#tododoc
    # todo: After every command in shell, must make the top emitter emit
    def __init__(self, frame):
        locals_for_shell = {
            'f': frame,
            'gp': frame.gui_project,
            'p': frame.gui_project.project,
            't': frame.gui_project.project.tree,
            'garlicsim': garlicsim,
            'garlicsim_wx': garlicsim_wx,
        }
        wx.py.shell.Shell.__init__(self, frame, size=(100, 100),
                                   locals=locals_for_shell)
        WorkspaceWidget.__init__(self, frame)
        
    
