# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the `Arg` class.

See its documentation for more details.
'''

import wx

from garlicsim_wx.general_misc import wx_tools

from .value_text_ctrl import ValueTextCtrl


class Arg(wx.Panel):
    '''
    Widget for specifying a named argument to the step function.

    The name is static, only the value can be changed by the user.
    '''
    def __init__(self, argument_control, name, value=''):
        wx.Panel.__init__(self, argument_control)
        if wx.Platform == '__WXGTK__':
            self.SetBackgroundColour(wx_tools.get_background_color())
        
        self.argument_control = argument_control
        self.name = name
        
        self.main_h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.name_static_text = wx.StaticText(self, label=('%s=' % name))
        
        self.main_h_sizer.Add(self.name_static_text, 0,
                              wx.ALIGN_CENTER_VERTICAL)
        
        self.value_text_ctrl = ValueTextCtrl(
            self,
            #size=(100, -1),
            value=value
        )
        
        self.main_h_sizer.Add(self.value_text_ctrl, 1,
                              wx.ALIGN_CENTER_VERTICAL)
        
        self.SetSizer(self.main_h_sizer)
        
        #self.main_h_sizer.Fit(self)
        
        
    def get_value_string(self):
        '''Get the value of the argument, as a string.'''
        return self.value_text_ctrl.GetValue()
    