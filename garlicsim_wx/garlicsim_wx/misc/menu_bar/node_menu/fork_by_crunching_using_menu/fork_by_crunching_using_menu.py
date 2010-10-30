# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the NodeMenu class.

See its documentation for more info.
'''

import wx

from garlicsim_wx.general_misc.cute_menu import CuteMenu


class ForkByCrunchingUsingMenu(CuteMenu):
    def __init__(self, frame):
        super(NodeMenu, self).__init__()
        self.frame = frame
        self._build()
    
    def _build(self):
        
        frame = self.frame
        
        self.AppendSeparator()
        
        
        self.AppendSeparator()
        
        
        self.new_step_profile_button = self.Append(
            -1,
            '&New step profile...',
            ' Create a new step profile'
        )
        frame.Bind(self.on_new_step_profile_button, wx.EVT_BUTTON,
                   self.new_step_profile_button)
        
        
    def on_new_step_profile_button(self, event):
        raise NotImplementedError#tododoc
    
        
    def _recalculate(self):
        raise NotImplementedError#tododoc
        0
        
    