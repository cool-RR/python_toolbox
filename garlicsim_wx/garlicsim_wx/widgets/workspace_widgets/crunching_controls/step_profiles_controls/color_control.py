import colorsys

import wx

from garlicsim_wx.widgets.general_misc.hue_selection_dialog \
     import HueSelectionDialog
from garlicsim_wx.general_misc import wx_tools

import garlicsim_wx


class ColorControl(wx.Window):
    def __init__(self, step_profiles_list, color=None):
        wx.Window.__init__(self, step_profiles_list.GetMainWindow(),
                           size=(25, 10), style=wx.SIMPLE_BORDER)

        self.color = color or wx.Color(0, 0, 0)
        
        self._pen = wx.Pen(wx.Color(0, 0, 0), width=0, style=wx.TRANSPARENT)
        
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_mouse_left_down)
        
        
    
    def on_paint(self, event):
        dc = wx.PaintDC(self)
        dc.SetBrush(wx.Brush(self.color))
        dc.SetPen(self._pen)
        dc.DrawRectangle(0, 0, *self.GetSize())
        dc.Destroy()
        
    
    def on_mouse_left_down(self, event):
        old_hls = wx_tools.wx_color_to_hls(self.color)
        hue_selection_dialog = \
            HueSelectionDialog(self, setter=lambda color: None,
                               old_hls=old_hls, lightness=0.3,
                               title='Select hue for step profile')
        hue_selection_dialog.ShowModal()
        hue_selection_dialog.Destroy()
        
        
    def set_color(self, color):
        if self.color != color:
            self.color = color
            self.Refresh()