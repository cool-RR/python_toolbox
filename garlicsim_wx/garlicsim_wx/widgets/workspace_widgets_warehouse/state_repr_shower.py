# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.


import wx
from garlicsim_wx.widgets import WorkspaceWidget
import garlicsim.general_misc.dict_tools as dict_tools


__all__ = ["StateReprShower"]

class StateReprShower(wx.TextCtrl, WorkspaceWidget):#tododoc
    def __init__(self, frame):
        wx.TextCtrl.__init__(self, frame, size=(100, 100),
                             style=wx.TE_MULTILINE)
        WorkspaceWidget.__init__(self, frame)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        font = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD, False,
                       u'Courier New')
        self.SetFont(font)
        self.state = None

    def on_paint(self, event):
        if self.frame.gui_project:
            active_state = self.frame.gui_project.get_active_state()        
            if active_state:
                if active_state is not self.state:
                    self.state = active_state
                    state_repr = dict_tools.fancy_string(vars(active_state))
                    self.SetValue(state_repr)
         
        event.Skip()
    
