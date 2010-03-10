# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
This module defines the GenericInitialDialog class. See its documentation for
more info.
'''

import wx

class GenericInitialDialog(wx.Dialog):
    '''
    An initial dialog to show when creating a root state.
    
    This is a generic one, used if the simpack doesn't define its own.
    '''
    def __init__(self, parent, id):
   
        wx.Dialog.__init__(self, parent, id, title="Creating a root state")

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.plain = empty = wx.RadioButton(self, -1, 'Plain', style=wx.RB_GROUP)
        self.random = random = wx.RadioButton(self, -1, 'Random')
        random.SetValue(True)
        hbox1.Add(empty, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        hbox1.Add(random, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        vbox = wx.BoxSizer(wx.VERTICAL)

        last_hbox = wx.StdDialogButtonSizer()
        ok = wx.Button(self, wx.ID_OK, 'Ok', size=(70, 30))
        ok.SetDefault()
        last_hbox.SetAffirmativeButton(ok)
        self.Bind(wx.EVT_BUTTON, self.on_ok, id=ok.GetId())
        cancel = wx.Button(self, wx.ID_CANCEL, 'Cancel', size=(70, 30))
        self.Bind(wx.EVT_BUTTON, self.on_cancel, id=cancel.GetId())
        last_hbox.AddButton(ok)
        last_hbox.AddButton(cancel)
        last_hbox.Realize()

        vbox.Add(hbox1, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        vbox.Add(last_hbox, 1, wx.ALIGN_CENTER | wx.BOTTOM, 10)

        self.SetSizer(vbox)
        vbox.Fit(self)
        ok.SetFocus()

    def on_ok(self,e=None):
        '''Do 'Okay' on the dialog.'''

        '''
        def complain(message):
            dialog = wx.MessageDialog(self, message, "Error",
                                      wx.ICON_ERROR | wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
        '''

        self.info = {}

        self.info["random"] = self.random.GetValue() # It's a bool

        self.EndModal(wx.ID_OK)

        
    def on_cancel(self,e=None):
        '''Do 'cancel' on the dialog'''
        
        self.EndModal(wx.ID_CANCEL)

        
        