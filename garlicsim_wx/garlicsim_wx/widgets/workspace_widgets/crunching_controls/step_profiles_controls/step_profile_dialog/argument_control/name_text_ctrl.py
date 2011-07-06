# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `` class.

See its documentation for more details.
'''

import wx

from garlicsim.general_misc import misc_tools
from garlicsim_wx.widgets.general_misc.cute_window import CuteWindow

from . import colors


class NameTextCtrl(wx.TextCtrl, CuteWindow):
    '''Widget for entering an argument name.'''
    def __init__(self, parent, value=''):
        
        wx.TextCtrl.__init__(self, parent, value=value)
        self._original_background_color = self.GetBackgroundColour()
        
        self.SetMinSize((10, -1))
        
        self.bind_event_handlers(NameTextCtrl)
        
        self.error_mode = False
        
    
    def _check_validity_and_color(self):
        '''
        Check whether the value is a valid name, if it isn't show error color.
        '''
        is_valid = misc_tools.is_legal_ascii_variable_name(self.GetValue())
        if is_valid:
            self.SetBackgroundColour(self._original_background_color)
        else: # not is_valid
            self.SetBackgroundColour(colors.get_error_background_color())
        self.Refresh()
        return is_valid
            
        
    def _on_text(self, event):
        if self.error_mode:
            self._check_validity_and_color()
            
            
    def _on_kill_focus(self, event):
        event.Skip()
        if self.FindFocus() != self:
            if not self._check_validity_and_color() and not self.error_mode:
                self.error_mode = True