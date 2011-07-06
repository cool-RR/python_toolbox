# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `StarKwarg` class.

See its documentation for more details.
'''

import wx

from garlicsim.general_misc import misc_tools
from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.widgets.general_misc.cute_panel import CutePanel

from .name_text_ctrl import NameTextCtrl
from .value_text_ctrl import ValueTextCtrl
from .close_button import CloseButton


class StarKwarg(CutePanel):
    '''
    Widget for specifying an extraneous keyword argument (for `**kwargs`).
    
    Allows used to type both a keyword name and a value to be assigned to it.
    '''
    def __init__(self, argument_control, star_kwarg_box, name='', value=''):
        wx.Panel.__init__(self, argument_control)
        if wx_tools.is_gtk:
            self.set_good_background_color()
        
        self.argument_control = argument_control
        
        self.star_kwarg_box = star_kwarg_box
        
        self.main_h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.name_text_ctrl = NameTextCtrl(self, value=name)
        self.main_h_sizer.Add(self.name_text_ctrl, 4,
                              wx.ALIGN_CENTER_VERTICAL)
                
        self.static_text = wx.StaticText(self, label=('='))
        
        self.main_h_sizer.Add(self.static_text, 0,
                              wx.ALIGN_CENTER_VERTICAL)
        
        self.value_text_ctrl = ValueTextCtrl(
            self,
            value=value
        )
        self.main_h_sizer.Add(self.value_text_ctrl, 6,
                              wx.ALIGN_CENTER_VERTICAL)
        
        self.close_button = CloseButton(self)
        
        self.main_h_sizer.Add(self.close_button, 0,
                              wx.ALIGN_CENTER_VERTICAL)
        
        self.SetSizer(self.main_h_sizer)
        
        self.bind_event_handlers(StarKwarg)

        
    def remove(self):
        '''Remove this `StarKwarg` from the containing `StarKwargBox`.'''
        self.star_kwarg_box.remove(self)
        
        
    def get_name_string(self):
        '''Get the name of the kwarg as a string.'''
        return str(self.name_text_ctrl.GetValue())
    
    
    def get_value_string(self):
        '''Get the value of the kwarg as a string.'''
        return self.value_text_ctrl.GetValue()
        
    
    def _on_close_button(self, event):
        self.remove()