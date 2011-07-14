# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `StarArg` class.

See its documentation for more details.
'''

import wx

from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.widgets.general_misc.cute_panel import CutePanel

from .close_button import CloseButton
from .value_text_ctrl import ValueTextCtrl


class StarArg(CutePanel):
    '''
    Widget for specifying an extraneous positional argument (for `*args`).
    '''
    def __init__(self, argument_control, star_arg_box, value=''):
        wx.Panel.__init__(self, argument_control)
        if wx_tools.is_gtk:
            self.set_good_background_color()
            
        self.HelpText = ('Allows you to set the values of additional '
                         'arguments that the step function accepts. These '
                         'are unnamed arguments.')
        
        self.argument_control = argument_control
        
        self.star_arg_box = star_arg_box
        
        self.main_h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.value_text_ctrl = ValueTextCtrl(
            self,
            value=value
        )
        
        self.main_h_sizer.Add(self.value_text_ctrl, 1,
                              wx.ALIGN_CENTER_VERTICAL)
        
        self.close_button = CloseButton(self)
        
        self.main_h_sizer.Add(self.close_button, 0,
                              wx.ALIGN_CENTER_VERTICAL)
        
        self.SetSizer(self.main_h_sizer)
        
        self.bind_event_handlers(StarArg)
    
        
    def remove(self):
        '''Remove this `StarArg` from the containing `StarArgBox`.'''
        self.star_arg_box.remove(self)
        
        
    def get_value_string(self):
        '''Get the value of the arument as a string.'''
        return self.value_text_ctrl.GetValue()
    
    
    def _on_close_button(self, event):
        self.remove()
    
        
            