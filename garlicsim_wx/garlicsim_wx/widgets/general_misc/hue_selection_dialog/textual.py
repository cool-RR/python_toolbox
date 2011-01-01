# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the `Textual` class.

See its documentation for more details.
'''

from __future__ import division
from __future__ import with_statement

import wx

from garlicsim_wx.general_misc import wx_tools
from garlicsim.general_misc.context_manager import ContextManager


def ratio_to_round_degrees(ratio):
    return int(ratio * 360)


def degrees_to_ratio(degrees):
    return degrees / 360


class Freezer(ContextManager):
    '''
    Freezer for not changing the `Textual`'s text value.

    Used as a context manager. Anything that happens inside the `with` suite
    will not cause the `Textual` to update its text value.
    
    This is useful because when the `Textual`'s value changes, some platforms
    automatically select all the text in the `Textual`, which is really
    annoying if you're just typing in it.
    '''
    def __init__(self, textual):
        self.textual = textual
    def __enter__(self):
        self.textual.frozen += 1
    def __exit__(self, *args, **kwargs):
        self.textual.frozen -= 1


class Textual(wx.Panel):
    '''Display (and allow modifying) the hue as a number 0-359.'''
    def __init__(self, hue_selection_dialog):
        wx.Panel.__init__(self, parent=hue_selection_dialog, size=(75, 100))
        self.SetBackgroundColour(wx_tools.get_background_color())
        
        self.hue_selection_dialog = hue_selection_dialog
        self.hue = hue_selection_dialog.hue
        
        self.frozen = 0
        self.freezer = Freezer(self)
        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.hue_static_text = wx.StaticText(self, label='Hue:')
        
        self.main_v_sizer.Add(self.hue_static_text, 0,
                              wx.ALIGN_LEFT | wx.BOTTOM, border=5)
        
        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.main_v_sizer.Add(self.h_sizer, 0)
        
        self.spin_ctrl = wx.SpinCtrl(self, min=0, max=359,
                                     initial=ratio_to_round_degrees(self.hue),
                                     size=(70, -1), style=wx.SP_WRAP)
        if wx.Platform == '__WXMAC__':
            self.spin_ctrl.SetValue(ratio_to_round_degrees(self.hue))
        
        self.h_sizer.Add(self.spin_ctrl, 0)
        
        self.degree_static_text = wx.StaticText(self, label=unichr(176))
        
        self.h_sizer.Add(self.degree_static_text, 0)
        
        self.SetSizerAndFit(self.main_v_sizer)
        
        self.Bind(wx.EVT_SPINCTRL, self.on_spin, source=self.spin_ctrl)
        self.Bind(wx.EVT_TEXT, self.on_text, source=self.spin_ctrl)
                    
        
    def update(self):
        '''Update to show the new hue.'''
        if not self.frozen and self.hue != self.hue_selection_dialog.hue:
            self.hue = self.hue_selection_dialog.hue
            self.spin_ctrl.SetValue(ratio_to_round_degrees(self.hue))
    
            
    def on_spin(self, event):
        self.hue_selection_dialog.setter(
            degrees_to_ratio(
                self.spin_ctrl.GetValue()
            )
        )
            
    def on_text(self, event):
        with self.freezer:
            self.hue_selection_dialog.setter(
                degrees_to_ratio(
                    self.spin_ctrl.GetValue()
                )
            )
