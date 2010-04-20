# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.


import wx
from garlicsim_wx.widgets import WorkspaceWidget
import garlicsim.general_misc.dict_tools as dict_tools
from garlicsim_wx.general_misc.flag_raiser import FlagRaiser

__all__ = ["StateReprViewer"]

class StateReprViewer(wx.Panel, WorkspaceWidget):#tododoc
    def __init__(self, frame):
        wx.Panel.__init__(self, frame, size=(300, 300))
        WorkspaceWidget.__init__(self, frame)

        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        
        self.Bind(wx.EVT_PAINT, self.on_paint)        
        
        self.text_ctrl = wx.TextCtrl(
            self,
            style=wx.TE_MULTILINE | wx.NO_BORDER
        )
        font = wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.BOLD, False,
                       u'Courier New')
        self.text_ctrl.SetFont(font)
        
        self.sizer_v = wx.BoxSizer(wx.VERTICAL)
        self.sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_v.Add(self.sizer_h, 1, wx.EXPAND)
        self.sizer_h.Add(self.text_ctrl, 1, wx.EXPAND)
        
        self.SetSizer(self.sizer_v)
        self.sizer_v.Layout()
        
        self.state = None
        
        self.needs_update_flag = True
        
        self.needs_update_emitter = \
            self.gui_project.emitter_system.make_emitter(
                inputs=(
                    self.gui_project.active_node_changed_emitter,
                    # todo: put the active_state_changed whatever here
                    ),
                outputs=(FlagRaiser(self, 'needs_update_flag'),),
                name='needs_update_emitter',
            )
    

    def on_paint(self, event):
        event.Skip()
        if self.needs_update_flag:
            if self.gui_project:
                active_state = self.gui_project.get_active_state()        
                if active_state:
                    if active_state is not self.state:
                        self.state = active_state
                        state_repr = dict_tools.fancy_string(vars(active_state))
                        self.text_ctrl.SetValue(state_repr)
            self.needs_update_flag = False
         
        
    
