# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

import wx

from garlicsim_wx.widgets.general_misc.cute_dialog import CuteDialog

import garlicsim
import garlicsim_wx
    

class CruncherSelectionDialog(CuteDialog):
    # tododoc: make it respect Esc. (SetEscapeId)
    def __init__(self, cruncher_controls):
        CuteDialog.__init__(
            self,
            cruncher_controls.GetTopLevelParent(),
            title='Choose a cruncher type'
        )
        
        self.frame = cruncher_controls.frame
        self.gui_project = cruncher_controls.gui_project
        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.general_text = wx.StaticText(
            self,
            label=("Choose a cruncher type to be used when crunching the "
                   "simulation. Your simulation will use the same algorithm "
                   "regardless of which cruncher you'll choose; the choice of "
                   "cruncher will affect how and where that algorithm will be "
                   "run.")
        )
        
        self.main_v_sizer.Add(self.general_text, 0, wx.EXPAND)
        
        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.cruncher_list_box = wx.ListBox(
            self,
            choices=[
                'ThreadCruncher',
                'ProcessCruncher',
                'NanoThreadCruncher (Not available)',
                'PiCloudCruncher (Not available)'
            ]
        )
        
        self.h_sizer.Add(self.cruncher_list_box, 1, wx.EXPAND)
        
        self.cruncher_text = wx.StaticText(
            self,
            label=help(garlicsim.asynchronous_crunching.crunchers.ThreadCruncher)
        )
        
        self.h_sizer.Add(self.cruncher_text, 1, wx.EXPAND)
        
        
        
        
        self.SetSizer(self.main_v_sizer)
    