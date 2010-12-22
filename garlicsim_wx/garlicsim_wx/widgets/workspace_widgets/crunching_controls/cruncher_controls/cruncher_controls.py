# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

import pkg_resources
import wx

from garlicsim_wx.general_misc import wx_tools

import garlicsim, garlicsim_wx

from .cruncher_selection_dialog import CruncherSelectionDialog

    
class CruncherControls(wx.Panel):
    '''Widget for viewing/changing the active cruncher type.'''
    
    def __init__(self, parent, frame):
        
        assert isinstance(frame, garlicsim_wx.Frame)
        self.frame = frame
        self.gui_project = frame.gui_project
        
        wx.Panel.__init__(self, parent)
        
        self.SetBackgroundColour(wx_tools.get_background_color())
        
        self.SetToolTipString('Observe or change the cruncher type that is '
                              'used when crunching the simulation.')
        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.SetSizer(self.main_v_sizer)
        
        self.title_text = wx.StaticText(self, -1, 'Cruncher in use:')
        
        self.main_v_sizer.Add(self.title_text, 0)
        
        self.cruncher_in_use_static_text = wx.StaticText(self, -1, '')
        self.cruncher_in_use_static_text.SetFont(
            wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL)
        )
        
        self.main_v_sizer.Add(self.cruncher_in_use_static_text, 0,
                              wx.EXPAND | wx.ALL, 5)
        
        
        self.change_cruncher_button = wx.Button(self, -1, 'Change...')
        self.Bind(wx.EVT_BUTTON, self.on_change_cruncher_button,
                  self.change_cruncher_button)
        
        self.main_v_sizer.Add(self.change_cruncher_button, 0,
                              wx.ALIGN_RIGHT | wx.BOTTOM, 5)
        
        self.gui_project.cruncher_type_changed_emitter.add_output(
            self._recalculate
        )
        
        
    def on_change_cruncher_button(self, event):
        cruncher_selection_dialog = CruncherSelectionDialog(self)
        cruncher_selection_dialog.ShowModal()
        cruncher_selection_dialog.Destroy()
        
    
    def _recalculate(self):
        '''Ensure we display the correct current cruncher type.'''
        self.cruncher_in_use_static_text.SetLabel(
            self.gui_project.project.crunching_manager.cruncher_type.__name__
        )
        

