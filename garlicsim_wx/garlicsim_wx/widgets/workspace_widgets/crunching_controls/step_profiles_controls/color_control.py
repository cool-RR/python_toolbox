import colorsys

import wx

from garlicsim_wx.widgets.general_misc.hue_selection_dialog \
     import HueSelectionDialog
from garlicsim_wx.general_misc import wx_tools

import garlicsim_wx


class ColorControl(wx.Window):
    def __init__(self, step_profiles_list, step_profile, color):
        wx.Window.__init__(self, step_profiles_list.GetMainWindow(),
                           size=(25, 10), style=wx.SIMPLE_BORDER)
                
        self.step_profiles_list = step_profiles_list
        self.frame = self.step_profiles_list.frame
        self.step_profile = step_profile
        self.color = color
        
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
        gui_project = self.step_profiles_list.frame.gui_project
        step_profiles_to_hues = gui_project.step_profiles_to_hues
        
        getter = lambda: \
                 step_profiles_to_hues.__getitem__(self.step_profile)
        setter = lambda color: \
                 step_profiles_to_hues.__setitem__(self.step_profile, color)
        
        hue_selection_dialog = \
            HueSelectionDialog(self.frame, getter, setter, lightness=0.3,
                               title='Select hue for step profile')
        
        gui_project.step_profiles_to_hues_modified_emitter.add_output(
            hue_selection_dialog.update
        )
        try:
            hue_selection_dialog.ShowModal()
        finally:
            hue_selection_dialog.Destroy()
            gui_project.step_profiles_to_hues_modified_emitter.remove_output(
                hue_selection_dialog.update
            )
        
        
    def set_color(self, color):
        if self.color != color:
            self.color = color
            self.Refresh()
