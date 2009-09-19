# Copyright 2009 Ram Rachum.
# This program is not licensed for distribution and may not be distributed.

import wx

class GenericInitialDialog(wx.Dialog):
    def __init__(self, parent, id):
        wx.Dialog.__init__(self, parent, id, title="Creating a root state")


        hbox1=wx.BoxSizer(wx.HORIZONTAL)
        self.plain=empty=wx.RadioButton(self, -1, 'Plain', style=wx.RB_GROUP)
        self.random=random=wx.RadioButton(self, -1, 'Random')
        random.SetValue(True)
        hbox1.Add(empty,0,wx.ALIGN_CENTER | wx.ALL,5)
        hbox1.Add(random,0,wx.ALIGN_CENTER | wx.ALL,5)

        vbox = wx.BoxSizer(wx.VERTICAL)

        last_hbox = wx.StdDialogButtonSizer()
        ok=wx.Button(self, wx.ID_OK, 'Ok', size=(70, 30))
        ok.SetDefault()
        last_hbox.SetAffirmativeButton(ok)
        self.Bind(wx.EVT_BUTTON, self.on_ok, id=ok.GetId())
        cancel=wx.Button(self, wx.ID_CANCEL, 'Cancel', size=(70, 30))
        self.Bind(wx.EVT_BUTTON, self.on_cancel, id=cancel.GetId())
        last_hbox.AddButton(ok)
        last_hbox.AddButton(cancel)
        last_hbox.Realize()


        vbox.Add(hbox1,0,wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        vbox.Add(last_hbox, 1, wx.ALIGN_CENTER |  wx.BOTTOM, 10)

        self.SetSizer(vbox)
        vbox.Fit(self)
        ok.SetFocus()

    def on_ok(self,e=None):

        def complain(message):
            dialog=wx.MessageDialog(self,message,"Error",wx.ICON_ERROR | wx.OK)
            dialog.ShowModal(); dialog.Destroy()

        self.info={}


        self.info["random"]=True if self.random.GetValue() else False


        self.EndModal(wx.ID_OK)

    def on_cancel(self,e=None):
        self.EndModal(wx.ID_CANCEL)
