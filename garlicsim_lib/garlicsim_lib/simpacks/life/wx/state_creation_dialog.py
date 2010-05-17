# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the StateCreationDialog class.

See its documentation for more info.
'''

import random
import warnings
import functools

import wx

from garlicsim_wx.widgets.general_misc import CuteDialog

import garlicsim.data_structures
import widgets


class StateCreationDialog(CuteDialog):
    '''Initial dialog for creating a root state.'''
    def __init__(self, frame):
        CuteDialog.__init__(self, frame, title="Creating a root state")
        
        self.frame = frame
        self.simpack = frame.gui_project.simpack

        hbox1=wx.BoxSizer(wx.HORIZONTAL)
        self.x_title = x_title = wx.StaticText(self, -1, "Width: ")
        self.x_textctrl = x_textctrl = wx.TextCtrl(self, -1, "45")
        self.y_title = y_title = wx.StaticText(self, -1, "Height: ")
        self.y_textctrl = y_textctrl = wx.TextCtrl(self, -1, "25")
        hbox1.Add(x_title, 0, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL, 5)
        hbox1.Add(x_textctrl, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.RIGHT, 40)
        hbox1.Add(y_title, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.RIGHT, 10)
        hbox1.Add(y_textctrl, 0, wx.EXPAND | wx.ALIGN_CENTER | wx.RIGHT, 5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.empty = empty = wx.RadioButton(self, -1, 'All empty',
                                            style=wx.RB_GROUP)
        self.full = full = wx.RadioButton(self, -1, 'All full')
        self.random = random = wx.RadioButton(self, -1, 'Random')
        random.SetValue(True)
        hbox2.Add(empty, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        hbox2.Add(full, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        hbox2.Add(random, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        
        vbox = wx.BoxSizer(wx.VERTICAL)

        last_hbox = wx.BoxSizer(wx.HORIZONTAL)
        ok = wx.Button(self, -1, 'Ok', size=(70, 30))
        ok.SetDefault()
        self.Bind(wx.EVT_BUTTON, self.on_ok, id=ok.GetId())
        cancel = wx.Button(self, -1, 'Cancel', size=(70, 30))
        self.Bind(wx.EVT_BUTTON, self.on_cancel, id=cancel.GetId())
        last_hbox.Add(ok, 0)
        last_hbox.Add(cancel, 0, wx.LEFT, 5)

        vbox.Add(hbox1, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        vbox.Add(hbox2, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        vbox.Add(last_hbox, 1, wx.ALIGN_CENTER |  wx.BOTTOM, 10)

        self.SetSizer(vbox)
        vbox.Fit(self)
        ok.SetFocus()

    def on_ok(self, e=None):
        '''Do 'okay' on the dialog.'''

        def complain(message):
            dialog = wx.MessageDialog(self, message, "Error",
                                      wx.ICON_ERROR | wx.OK)
            dialog.ShowModal()
            dialog.Destroy()

        self.info = {}

        try:
            self.info["width"] = int(self.x_textctrl.GetValue())
        except ValueError:
            complain("Bad width!")
            return

        try:
            self.info["height"] = int(self.y_textctrl.GetValue())
        except ValueError:
            complain("Bad height!")
            return

        self.info["fill"] = "full" if self.full.GetValue() else \
            "empty" if self.empty.GetValue() else "random"


        self.EndModal(wx.ID_OK)

    def on_cancel(self, e=None):
        '''Do 'cancel' on the dialog.'''
        self.EndModal(wx.ID_CANCEL)
        
    def start(self):
        '''Start the dialog to make a new state.'''
        if self.ShowModal() == wx.ID_OK:
            width, height, fill = (
                self.info["width"],
                self.info["height"],
                self.info["fill"]
            )
            state = self.simpack.State.create_root(width, height, fill)
        else:
            state = None
        self.Destroy()
        return state
        


    
    