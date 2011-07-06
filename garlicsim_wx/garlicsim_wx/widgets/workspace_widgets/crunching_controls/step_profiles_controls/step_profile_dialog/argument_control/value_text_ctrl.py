# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `ValueTextCtrl` class.

See its documentation for more details.
'''

import wx

from garlicsim_wx.widgets.general_misc.cute_window import CuteWindow

from . import colors


class ValueTextCtrl(wx.TextCtrl, CuteWindow):
    '''Widget for inputting a Python expression for an argument value.'''
    
    def __init__(self, parent, value='', root=None):
        
        wx.TextCtrl.__init__(self, parent, value=value)
        
        self._original_background_color = self.GetBackgroundColour()
        
        self.root = root
        
        self.SetMinSize((10, -1))
        
        self.bind_event_handlers(ValueTextCtrl)
        
        self.error_mode = False
        
    
    def _check_validity_and_color(self):
        '''
        Check whether the expression is valid, if it isn't show error color.
        '''
        try:
            self.Parent.argument_control.step_profile_dialog.resolve(
                str(self.GetValue())
            )
        except Exception:
            is_valid = False
        else:
            is_valid = True
            
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