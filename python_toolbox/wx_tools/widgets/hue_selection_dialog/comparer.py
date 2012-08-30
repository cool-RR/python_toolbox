# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `Comparer` class.

See its documentation for more details.
'''

import wx

from python_toolbox import wx_tools
from python_toolbox.wx_tools.widgets.cute_panel import CutePanel


class Comparer(CutePanel):
    '''Shows the new hue compared to the old hue before dialog was started.'''
    def __init__(self, hue_selection_dialog):
        style = (wx.SIMPLE_BORDER if wx_tools.is_gtk else wx.SUNKEN_BORDER)
        wx.Panel.__init__(self, parent=hue_selection_dialog, size=(75, 90),
                          style=style)
        self.SetDoubleBuffered(True)
        self.SetHelpText('The current hue is shown next to the old hue for '
                         'comparison. To change back to the old hue, click on '
                         'it.')
        self.hue_selection_dialog = hue_selection_dialog
        assert isinstance(self.hue_selection_dialog, HueSelectionDialog)
        self.hue = hue_selection_dialog.hue
        self.old_hls = hue_selection_dialog.old_hls
        self.old_hue = hue_selection_dialog.old_hue
        self.old_color = wx_tools.colors.hls_to_wx_color(self.old_hls)
        self.negative_old_color = wx_tools.colors.invert_wx_color(self.color)
        self.old_brush = wx.Brush(self.old_color)
        self._transparent_pen = \
            wx.Pen(wx.Colour(0, 0, 0), width=0, style=wx.TRANSPARENT)
        self._calculate()
        
        self.SetCursor(wx.StockCursor(wx.CURSOR_BULLSEYE))
        
        self.bind_event_handlers(Comparer)
        
    
    @property
    def color(self):
        return wx_tools.colors.hls_to_wx_color(
            (self.hue,
             self.hue_selection_dialog.lightness,
             self.hue_selection_dialog.saturation)
        )
        
        
    def _calculate(self):
        '''Create a brush for showing the new hue.'''
        self.brush = wx.Brush(self.color)
        
        
    def update(self):
        '''If hue changed, show new hue.'''
        if self.hue != self.hue_selection_dialog.hue:
            self.hue = self.hue_selection_dialog.hue
            self._calculate()
            self.Refresh()
            
    
    def change_to_old_hue(self):
        self.hue_selection_dialog.setter(self.old_hue)

            
    def _on_paint(self, event):
        width, height = self.GetClientSize()
        dc = wx.BufferedPaintDC(self)
        graphics_context = wx.GraphicsContext.Create(dc)
        assert isinstance(graphics_context, wx.GraphicsContext)

        dc.SetPen(self._transparent_pen)
        
        dc.SetBrush(self.brush)
        dc.DrawRectangle(0, 0, width, (height // 2))
                    
        dc.SetBrush(self.old_brush)
        dc.DrawRectangle(0, (height // 2), width, (height // 2) + 1)
        
        if self.has_focus():
            graphics_context.SetPen(
                wx_tools.drawing_tools.pens.get_focus_pen(
                    self.negative_old_color
                )
            )
            graphics_context.SetBrush(self.old_brush)
            graphics_context.DrawRectangle(3, (height // 2) + 3,
                                           width - 6, (height // 2) - 6)
                
    
    def _on_left_down(self, event):
        x, y = event.GetPosition()
        width, height = self.GetClientSize()
        if y >= height // 2:
            self.change_to_old_hue()
            
    def _on_char(self, event):
        char = unichr(event.GetUniChar())
        if char == ' ':
            self.change_to_old_hue()
        else:
            event.Skip()
            
            
    def _on_set_focus(self, event):
        event.Skip()
        self.Refresh()
        

    def _on_kill_focus(self, event):
        event.Skip()
        self.Refresh()
        
        
from .hue_selection_dialog import HueSelectionDialog