# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the `` class.

See its documentation for more details.
'''

from __future__ import with_statement

import wx

import garlicsim, garlicsim_wx

from garlicsim.general_misc.context_manager import ContextManager
from garlicsim_wx.general_misc import wx_tools


class Freezer(ContextManager):
    '''
    Freezer for not changing the `SpinCtrl`'s text value.

    Used as a context manager. Anything that happens inside the `with` suite
    will not cause the `SpinCtrl` to update its text value.
    
    This is useful because when the `SpinCtrl`'s value changes, some platforms
    automatically select all the text in the `SpinCtrl`, which is really
    annoying if you're just typing in it.
    '''
    
    def __init__(self, autocrunch_controls):
        self.autocrunch_controls = autocrunch_controls
        
    def __enter__(self):
        self.autocrunch_controls.frozen += 1
        
    def __exit__(self, *args, **kwargs):
        self.autocrunch_controls.frozen -= 1
        

class AutocrunchControls(wx.Panel):

    def __init__(self, parent, frame):

        assert isinstance(frame, garlicsim_wx.Frame)
        self.frame = frame
        self.gui_project = frame.gui_project
        assert isinstance(self.gui_project, garlicsim_wx.GuiProject)
        
        wx.Panel.__init__(self, parent, -1)
        
        self.SetBackgroundColour(wx_tools.get_background_color())
        
        tooltip_text = ('Set the clock buffer that will be crunched '
                        'automatically from the active node.')
        
        self.SetToolTipString(tooltip_text)
                
        self.frozen = 0
        self.freezer = Freezer(self)
        
        self.main_h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.SetSizer(self.main_h_sizer)
        
        self.check_box = wx.CheckBox(self, -1, 'Autocrunch: ')
        
        self.check_box.SetToolTipString(tooltip_text)
        
        self.main_h_sizer.Add(
            self.check_box,
            0,
            wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT,
            border=10
        )
        
        self.spin_ctrl = wx.SpinCtrl(self, -1, max=10000000)
        
        self.spin_ctrl.SetToolTipString(tooltip_text)
        
        
        self.main_h_sizer.Add(self.spin_ctrl, 0,
                              wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        
        self.check_box.SetValue(
            bool(self.gui_project.default_buffer)
        )
        
        self.spin_ctrl.Enable(
            bool(self.gui_project.default_buffer)
        )
        
        self.spin_ctrl.SetValue(
            self.gui_project.default_buffer or \
            self.gui_project._default_buffer_before_cancellation or \
            0
        )
        
        ### Setting up event handling and emitter connections: ################
        #                                                                     #
        
        self.gui_project.default_buffer_modified_emitter.add_output(
            self.update_check_box
        )
        
        self.Bind(wx.EVT_CHECKBOX, self.on_check_box,
                  source=self.check_box)
        
        self.Bind(wx.EVT_SPINCTRL, self.on_spin, self.spin_ctrl)
        self.Bind(wx.EVT_TEXT, self.on_text, self.spin_ctrl)
        
        self.gui_project.default_buffer_modified_emitter.add_output(
            self.update_spin_ctrl
        )
        
        #                                                                     #
        ### Finished setting up event handling and emitter connections. #######
        
        
    def on_check_box(self, event):
        if event.IsChecked(): # Checkbox got checked
            new_autocrunch = \
                self.gui_project._default_buffer_before_cancellation or 100
            self.gui_project.default_buffer = new_autocrunch
            self.gui_project._default_buffer_before_cancellation = None
            self.spin_ctrl.SetValue(new_autocrunch)
            self.spin_ctrl.Enable()
            if self.gui_project.active_node:
                self.gui_project.project.ensure_buffer(
                    self.gui_project.active_node,
                    clock_buffer=new_autocrunch
                )
        else: # Checkbox got unchecked
            autocrunch_to_store = self.spin_ctrl.GetValue() or 100
            self.gui_project._default_buffer_before_cancellation = \
                autocrunch_to_store
            self.gui_project.default_buffer = 0
            self.spin_ctrl.Disable()
        
    def _update_gui_project(self):
        '''Update the gui project with the autocrunch value that we have.'''
        self.gui_project.set_default_buffer(self.spin_ctrl.GetValue())
        
            
    def on_spin(self, event):
        self._update_gui_project()
        event.Skip()
            
        
    def on_text(self, event):
        with self.freezer:
            self._update_gui_project()
        event.Skip()
        
        
    def update_spin_ctrl(self):
        '''Update the `SpinCtrl` with the gui project's autocrunch value.'''
        if not self.frozen:
            value = self.gui_project.default_buffer or \
                    self.gui_project._default_buffer_before_cancellation or \
                    0
            self.spin_ctrl.SetValue(value)
            self.spin_ctrl.Enable(bool(value))
        
        
    def update_check_box(self):
        '''
        Update the `CheckBox` on whether autocrunch is on in the gui project.
        '''
        self.check_box.SetValue(
            bool(self.gui_project.default_buffer)
        )
        
        
    def on_size(self, event):
        '''EVT_SIZE handler.'''
        self.Refresh()
        event.Skip()
    
        
    def on_paint(self, event):
        '''EVT_PAINT handler.'''
        event.Skip()
        

    