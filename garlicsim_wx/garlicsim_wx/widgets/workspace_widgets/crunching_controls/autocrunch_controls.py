# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

import wx

import garlicsim, garlicsim_wx


class AutocrunchControls(wx.Panel):

    def __init__(self, parent, frame):
        wx.Panel.__init__(self, parent, -1)
        
        self.main_h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.SetSizer(self.main_h_sizer)
        
        self.main_h_sizer.Add(self.autocrunch_h_sizer, 0, wx.ALL, border=10)
        
        self.check_box = wx.CheckBox(self, -1, 'Autocrunch: ')
        
        self.main_h_sizer.Add(
            self.check_box,
            0,
            wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT,
            border=10
        )
        
        self.spin_ctrl = wx.SpinCtrl(self, -1, max=10000000)
        
        self.main_h_sizer.Add(self.spin_ctrl, 0,
                              wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        
        self.Bind(wx.EVT_CHECKBOX, self.on_autocrunch_check_box,
                  source=self.autocrunch_check_box)
        
        self.autocrunch_check_box.SetValue(
            bool(self.gui_project.default_buffer)
        )
        
        self.autocrunch_spin_ctrl.Enable(
            bool(self.gui_project.default_buffer)
        )
        
        self.autocrunch_spin_ctrl.SetValue(
            self.gui_project.default_buffer or \
            self.gui_project._default_buffer_before_cancellation or \
            0
        )
        
        


    def on_check_box(self, event):
        if event.IsChecked(): # Checkbox got checked
            new_autocrunch = \
                self.gui_project._default_buffer_before_cancellation or 100
            self.gui_project.default_buffer = new_autocrunch
            self.gui_project._default_buffer_before_cancellation = None
            self.autocrunch_spin_ctrl.SetValue(new_autocrunch)
            self.autocrunch_spin_ctrl.Enable()
            self.gui_project.project.ensure_buffer(
                self.gui_project.active_node,
                clock_buffer=new_autocrunch
            )
        else: # Checkbox got unchecked
            autocrunch_to_store = self.autocrunch_spin_ctrl.GetValue() or 100
            self.gui_project._default_buffer_before_cancellation = \
                autocrunch_to_store
            self.gui_project.default_buffer = 0
            self.autocrunch_spin_ctrl.Disable()
        
        
    def on_size(self, event):
        '''EVT_SIZE handler.'''
        self.Refresh()
        event.Skip()
    
        
    def on_paint(self, event):
        '''EVT_PAINT handler.'''
        event.Skip()
        

    