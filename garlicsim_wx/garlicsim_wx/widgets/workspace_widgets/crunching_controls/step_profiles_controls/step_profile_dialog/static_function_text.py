# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `StaticFunctionText` class.

See its documentation for more details.
'''

import wx

from garlicsim_wx.widgets.general_misc.cute_panel import CutePanel
from garlicsim_wx.general_misc import wx_tools

import garlicsim


class StaticFunctionText(CutePanel):
    '''Static text showing information about the current step function.'''
    
    def __init__(self, step_profile_dialog, step_function=None):
        
        self.step_profile_dialog = step_profile_dialog
        
        self.width = 400 if wx_tools.is_win else 500
        
        self.step_function = None
        
        wx.Panel.__init__(self, step_profile_dialog)
        self.HelpText = ('Information about the currently-selected step '
                         'function.')
        self.set_good_background_color()
        
        self.text = wx.StaticText(self, style=wx.ALIGN_CENTER_HORIZONTAL)
        
        self.SetMinSize((self.width, 25))
        
        #self.set_good_background_color()
        
        self.text.Wrap(self.width - 10)
        
        self.bind_event_handlers(StaticFunctionText)
        
        self.main_h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.main_h_sizer.Add(self.v_sizer, 1, wx.ALIGN_CENTER_VERTICAL)
        
        self.v_sizer.Add(self.text, 0, wx.ALIGN_CENTER_HORIZONTAL)
        
        self.SetSizer(self.main_h_sizer)
        
        self._error_color = wx.Colour(255, 200, 200)
        self._success_color = wx.Colour(200, 255, 200)

        self.valid_step_function = True
        
        
        
        
    def set_error_text(self, error_text):
        '''Set the error text to show.'''
        self.text.SetLabel(error_text)
        self.text.Wrap(self.width - 10)
        self.step_function = None
        
        self.Layout()
        
        
    def set_step_function(self, step_function):
        '''Set the step function to show information about.'''
        if step_function != self.step_function:
            self.step_function = step_function
            step_type = garlicsim.misc.simpack_grokker.step_type.BaseStep.\
                      get_step_type(step_function)
            step_function_address = self.step_profile_dialog.\
                                    describe(step_function)
            label = '`%s` is a %s.' % (
                step_function_address,
                step_type.verbose_name
            )
            self.text.SetLabel(label)
            self.text.Wrap(self.width - 10)
            #self.SetBackgroundColour(self._success_color)
            self.Layout()

    
    def _on_size(self, event):
        pass
    