# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied or
# distributed without explicit written permission from Ram Rachum.


import wx
from garlicsim_wx.widgets import WorkspaceWidget
import garlicsim.general_misc.dict_tools as dict_tools


__all__ = ["StateReprShower"]

class StateReprShower(wx.TextCtrl, WorkspaceWidget):#tododoc
    def __init__(self, gui_project):
        
        wx.TextCtrl.__init__(self, gui_project.frame, style=wx.TE_MULTILINE)
        
        self.gui_project = gui_project

    def OnPaint(self, *args, **kwargs):
        active_state = self.gui_project.get_active_state()
        if active_state:
            self.SetValue(dict_tools.fancy_string(state.__dict__))
            
        wx.TextCtrl.OnPaint(self, *args, **kwargs)
    
