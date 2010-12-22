# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the `HueControl` class.

See its documentation for more details.
'''

from __future__ import with_statement

import colorsys

import wx

from garlicsim_wx.widgets.general_misc.hue_selection_dialog \
     import HueSelectionDialog
from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.general_misc.emitters import Emitter


class HueControl(wx.Window):
    '''
    Widget for displaying (and possibly modifying) a hue.
    
    Clicking on the hue will open a dialog for changing it.
    '''
    def __init__(self, parent, getter, setter, emitter=None, lightness=1,
                 saturation=1, dialog_title='Select hue', size=(25, 10)):
        
        wx.Window.__init__(self, parent, size=size, style=wx.SIMPLE_BORDER)
        
        self.getter = getter
        
        self.setter = setter
                
        
        
        self.lightness = lightness
        
        self.saturation = saturation
        
        self.dialog_title = dialog_title
        
        
        self._pen = wx.Pen(wx.Colour(0, 0, 0), width=0, style=wx.TRANSPARENT)
        
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_mouse_left_down)
        
        if emitter:
            assert isinstance(emitter, Emitter)
            self.emitter = emitter
            self.emitter.add_output(self.update)
        else:
            assert emitter is None
            self.emitter = Emitter(
                outputs=(self.update,),
                name='hue_modified'
            )
            old_setter = self.setter
            def new_setter(value):
                old_setter(value)
                self.emitter.emit()
            self.setter = new_setter
            
        
    
    def on_paint(self, event):
        dc = wx.PaintDC(self)
        color = wx_tools.hls_to_wx_color(
            (
                self.getter(),
                self.lightness,
                self.saturation
            )
        )
        dc.SetBrush(wx.Brush(color))
        dc.SetPen(self._pen)
        width, height = self.GetSize()
        dc.DrawRectangle(-5, -5, width+10, height+10)
                
    
    def on_mouse_left_down(self, event):
        self.open_editing_dialog()
      
        
    def open_editing_dialog(self):
        '''Open a dialog to edit the hue.'''
        old_hue = self.getter()
        
        with wx_tools.CursorChanger(self, wx.CURSOR_WAIT):
            hue_selection_dialog = HueSelectionDialog(
                self.GetTopLevelParent(), self.getter, self.setter,
                self.emitter,
                lightness=self.lightness, saturation=self.saturation,
                title=self.dialog_title
            )
        
        try:
            hue_selection_dialog.ShowModal()
        finally:
            hue_selection_dialog.Destroy()

            
    def update(self):
        if self: # Protecting from dead object
            self.Refresh()

        
    def Destroy(self):
        self.emitter.remove_output(self.update)
        super(HueControl, self).Destroy()