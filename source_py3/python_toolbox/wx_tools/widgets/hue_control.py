# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `HueControl` class.

See its documentation for more details.
'''


import colorsys

import wx

from python_toolbox.wx_tools.widgets.hue_selection_dialog \
     import HueSelectionDialog
from python_toolbox import wx_tools
from python_toolbox.wx_tools.widgets.cute_window import CuteWindow
from python_toolbox.emitting import Emitter


class HueControl(CuteWindow):
    '''
    Widget for displaying (and possibly modifying) a hue.
    
    Clicking on the hue will open a dialog for changing it.
    '''
    def __init__(self, parent, getter, setter, emitter=None, lightness=1,
                 saturation=1, dialog_title='Select hue',
                 help_text='Shows the current hue. Click to change.',
                 size=(25, 10)):
        
        CuteWindow.__init__(self, parent, size=size, style=wx.SIMPLE_BORDER)
        
        self.getter = getter
        
        self.setter = setter                
        
        self.lightness = lightness
        
        self.saturation = saturation
        
        self.dialog_title = dialog_title
        
        self.SetHelpText(help_text)
        
        self._pen = wx.Pen(wx.Colour(0, 0, 0), width=0, style=wx.TRANSPARENT)
        
        self.bind_event_handlers(HueControl)
        
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
            
    
    @property
    def extreme_negative_wx_color(self):
        return wx.NamedColour('Black') if self.lightness > 0.5 else \
               wx.NamedColour('White')
    
    
    def open_editing_dialog(self):
        '''Open a dialog to edit the hue.'''
        old_hue = self.getter()
        
        hue_selection_dialog = HueSelectionDialog.create_and_show_modal(
            self.TopLevelParent, self.getter, self.setter, self.emitter,
            lightness=self.lightness, saturation=self.saturation,
            title=self.dialog_title
        )

            
    def update(self):
        if self: # Protecting from dead object
            self.Refresh()

        
    def Destroy(self):
        self.emitter.remove_output(self.update)
        super().Destroy()

        
    ### Event handlers: #######################################################
    #                                                                         #        
    def _on_paint(self, event):
        dc = wx.BufferedPaintDC(self)
        color = wx_tools.colors.hls_to_wx_color(
            (
                self.getter(),
                self.lightness,
                self.saturation
            )
        )
        dc.SetBrush(wx.Brush(color))
        dc.SetPen(self._pen)
        width, height = self.ClientSize
        dc.DrawRectangle(-5, -5, width+10, height+10)

        if self.has_focus():
            graphics_context = wx.GraphicsContext.Create(dc)
            assert isinstance(graphics_context, wx.GraphicsContext)
            graphics_context.SetPen(
                wx_tools.drawing_tools.pens.get_focus_pen(
                    color=self.extreme_negative_wx_color
                )
            )
            graphics_context.SetBrush(wx.TRANSPARENT_BRUSH)
            graphics_context.DrawRectangle(2, 2,
                                           width - 5, height - 5)
        
    
    def _on_left_down(self, event):
        self.open_editing_dialog()
    
        
    def _on_char(self, event):
        char = unichr(event.GetUniChar())
        if char == ' ':
            self.open_editing_dialog()
        else:
            event.Skip()
            
            
    def _on_set_focus(self, event):
        event.Skip()
        self.Refresh()
        

    def _on_kill_focus(self, event):
        event.Skip()
        self.Refresh()   
    #                                                                         #
    ### Finished event handlers. ##############################################
