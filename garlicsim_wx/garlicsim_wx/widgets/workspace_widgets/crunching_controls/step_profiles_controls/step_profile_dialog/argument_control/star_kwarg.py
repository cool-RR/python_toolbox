# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the `StarKwarg` class.

See its documentation for more details.
'''

import wx

from garlicsim.general_misc import misc_tools
from garlicsim_wx.general_misc import wx_tools

from .name_text_ctrl import NameTextCtrl
from .value_text_ctrl import ValueTextCtrl
from .close_button import CloseButton


class StarKwarg(wx.Panel):
    '''
    Widget for specifying an extraneous keyword argument (for `**kwargs`).
    
    Allows used to type both a keyword name and a value to be assigned to it.
    '''
    def __init__(self, argument_control, star_kwarg_box, name='', value=''):
        wx.Panel.__init__(self, argument_control)
        if wx.Platform == '__WXGTK__':
            self.SetBackgroundColour(wx_tools.get_background_color())
        
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
        
        self.Bind(wx.EVT_BUTTON, lambda event: self.remove(),
                  source=self.close_button)
        

        
    def remove(self):
        '''Remove this `StarKwarg` from the containing `StarKwargBox`.'''
        self.star_kwarg_box.remove(self)
        
        
    def get_name_string(self):
        '''Get the name of the kwarg as a string.'''
        return str(self.name_text_ctrl.GetValue())
    
    
    def get_value_string(self):
        '''Get the value of the kwarg as a string.'''
        return self.value_text_ctrl.GetValue()
        