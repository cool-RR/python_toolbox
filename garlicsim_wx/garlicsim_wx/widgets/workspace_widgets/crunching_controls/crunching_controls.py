# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `CrunchingControls` class.

See its documentation for more details.
'''

import wx.lib.scrolledpanel

from garlicsim_wx.general_misc import wx_tools

import garlicsim, garlicsim_wx
from garlicsim_wx.widgets import WorkspaceWidget

from .step_profiles_controls import StepProfilesControls
from .cruncher_controls import CruncherControls
from .autocrunch_controls import AutocrunchControls


class CrunchingControls(wx.lib.scrolledpanel.ScrolledPanel, WorkspaceWidget):
    '''
    Widget for controlling the crunching of the simulations.
    
    Contains three parts:
    
     1. `AutocrunchControls` for setting how far we should automatically
        crunch.
        
     2. `StepProfilesControls` for manipulating step profiles that are used 
        (or will be used) in the tree.
        
     3. `CruncherControls` for displaying which cruncher type is active and 
        switching to a different cruncher type.
    
    '''
    
    _WorkspaceWidget__name = 'Crunching'

    def __init__(self, frame):
        wx.lib.scrolledpanel.ScrolledPanel.__init__(self, frame, -1,
                                                    style=wx.SUNKEN_BORDER)
        WorkspaceWidget.__init__(self, frame)
        
        self.set_good_background_color()
        
        self.SetupScrolling()
        
        
        assert isinstance(self.gui_project, garlicsim_wx.GuiProject)
        # I put this assert mainly for better source assistance in Wing.
        # It may be removed.
        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.SetSizer(self.main_v_sizer)
        
        self.autocrunch_controls = AutocrunchControls(self, frame)
    
        self.main_v_sizer.Add(self.autocrunch_controls, 0, wx.ALL, border=10)
        
        self.step_profiles_controls = StepProfilesControls(self, frame)
        
        self.main_v_sizer.Add(self.step_profiles_controls, 1,
                              wx.EXPAND | wx.ALL, border=10)
        
        self.horizontal_line = wx.StaticLine(self, -1)
        
        self.main_v_sizer.Add(self.horizontal_line, 0,
                              wx.EXPAND | wx.LEFT | wx.RIGHT, border=30)
        
        self.main_v_sizer.AddSpacer((1, 20))
        
        self.cruncher_controls = CruncherControls(self, frame)
        
        self.main_v_sizer.Add(self.cruncher_controls, 0,
                              wx.EXPAND | wx.LEFT | wx.TOP | wx.RIGHT, 10)
        
        self.bind_event_handlers(CrunchingControls)
        
        self.autocrunch_controls.SetFocus()
        # We do this so when the user switches to this widget for the first
        # time, the focus will be on the autocrunch controls. I'm not sure this
        # is the wisest way to do this, since this sets the global focus and
        # not just the local.

        
    def _on_size(self, event):
        self.Refresh()
        event.Skip()
        