# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the `HueSelectionDialog` class.

See its documentation for more details.
'''

import wx

from garlicsim_wx.widgets.general_misc.cute_dialog import CuteDialog
from garlicsim_wx.general_misc.emitters import Emitter

from .wheel import Wheel
from .comparer import Comparer
from .textual import Textual


class HueSelectionDialog(CuteDialog):
    '''Dialog for changing a hue.'''
    
    def __init__(self, parent, getter, setter, emitter, lightness=1,
                 saturation=1, id=-1, title='Select hue',
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_DIALOG_STYLE, name=wx.DialogNameStr):

        
        CuteDialog.__init__(self, parent, id, title, pos, size, style, name)
        
        self.getter = getter
        
        self.setter = setter
        
        assert isinstance(emitter, Emitter)
        self.emitter = emitter
        
        self.lightness = lightness

        self.saturation = saturation
        
        self.hue = getter()
        
        self.old_hue = self.hue
        
        self.old_hls = (self.old_hue, lightness, saturation)
        
        
        
        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.main_v_sizer.Add(self.h_sizer, 0)
        
        self.wheel = Wheel(self)
        
        self.h_sizer.Add(self.wheel, 0)
        
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.h_sizer.Add(self.v_sizer, 0, wx.ALIGN_CENTER)
        
        self.comparer = Comparer(self)
        
        self.v_sizer.Add(self.comparer, 0, wx.RIGHT | wx.TOP | wx.BOTTOM,
                         border=10)
        
        self.textual = Textual(self)
        
        self.v_sizer.Add(self.textual, 0, wx.RIGHT | wx.TOP | wx.BOTTOM,
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
        self.main_v_sizer.Fit(self)
        
        
        self.emitter.add_output(self.update)
        
        
    def on_ok(self, event):
        self.EndModal(wx.ID_OK)
        
    
    def on_cancel(self, event):
        self.setter(self.old_hue)
        self.EndModal(wx.ID_CANCEL)
        
        
    def update(self):
        '''If hue changed, update all widgets to show the new hue.'''
        self.hue = self.getter()
        self.wheel.update()
        self.comparer.update()
        self.textual.update()
        
        
    def Destroy(self):
        self.emitter.remove_output(self.update)
        super(HueSelectionDialog, self).Destroy()