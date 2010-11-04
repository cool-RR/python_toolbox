# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

import wx

from garlicsim_wx.widgets.general_misc.cute_dialog import CuteDialog
from garlicsim.general_misc import string_tools

import garlicsim
import garlicsim_wx
    

class CruncherSelectionDialog(CuteDialog):
    # tododoc: make it respect Esc. (SetEscapeId or ID_CANCEL)
    def __init__(self, cruncher_controls):
        CuteDialog.__init__(
            self,
            cruncher_controls.GetTopLevelParent(),
            title='Choose a cruncher type',
            size=(500, 300)
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
        
        self.main_v_sizer.Add(self.general_text, 0, wx.EXPAND | wx.ALL,
                              border=10)
        
        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.main_v_sizer.Add(self.h_sizer, 1, wx.EXPAND)
        
        self.cruncher_list_box = wx.ListBox(
            self,
            choices=[
                'ThreadCruncher',
                'ProcessCruncher',
                'PiCloudCruncher (Not available)'
            ]
        )
        
        self.h_sizer.Add(self.cruncher_list_box, 1, wx.EXPAND | wx.ALL,
                              border=10)
        
        self.cruncher_text = wx.StaticText(
            self,
            label=string_tools.docstring_trim(
                garlicsim.asynchronous_crunching.crunchers.ThreadCruncher.\
                __doc__
            )
        )
        
        self.h_sizer.Add(self.cruncher_text, 1, wx.EXPAND | wx.ALL,
                              border=10)
        
        self.dialog_button_sizer = wx.StdDialogButtonSizer()
        
        self.main_v_sizer.Add(self.dialog_button_sizer, 0,
                              wx.ALIGN_CENTER | wx.ALL, border=10)
        
        self.ok_button = wx.Button(self, wx.ID_OK, 'Okay')
        self.dialog_button_sizer.AddButton(self.ok_button)
        self.ok_button.SetDefault()
        self.dialog_button_sizer.SetAffirmativeButton(self.ok_button)
        self.Bind(wx.EVT_BUTTON, self.on_ok, source=self.ok_button)
        
        self.cancel_button = wx.Button(self, wx.ID_CANCEL, 'Cancel')
        self.dialog_button_sizer.AddButton(self.cancel_button)
        self.Bind(wx.EVT_BUTTON, self.on_cancel, source=self.cancel_button)
        self.dialog_button_sizer.Realize()
        
        self.SetSizer(self.main_v_sizer)
        self.Layout()

        
    def on_ok(self, event):
        1/0
    
        
    def on_cancel(self, event):
        1/0