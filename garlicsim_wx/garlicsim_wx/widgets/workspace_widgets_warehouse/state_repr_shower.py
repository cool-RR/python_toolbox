# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied or
# distributed without explicit written permission from Ram Rachum.


import wx
from garlicsim_wx.widgets import WorkspaceWidget
import garlicsim.general_misc.dict_tools as dict_tools


__all__ = ["StateReprShower"]

class StateReprShower(wx.TextCtrl, WorkspaceWidget):#tododoc
    def __init__(self, frame):
        wx.TextCtrl.__init__(self, frame, style=wx.TE_MULTILINE)
        WorkspaceWidget.__init__(self, frame)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, False,
                       u'Courier New')
        self.SetFont(font)

    def on_paint(self, event):
        if self.frame.gui_project:
            active_state = self.frame.gui_project.get_active_state()
            if active_state:
                self.SetValue(dict_tools.fancy_string(vars(active_state)))
         
        event.Skip()
    
