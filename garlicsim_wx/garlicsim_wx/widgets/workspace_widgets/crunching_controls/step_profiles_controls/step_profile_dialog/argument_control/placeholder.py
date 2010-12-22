# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the `Placeholder` class.

See its documentation for more details.
'''

import wx

from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.general_misc import color_tools


class Placeholder(wx.StaticText):
    '''Placeholder for functions that don't have extraneous arguments.'''
    def __init__(self, argument_control, label):
        self.argument_control = argument_control
        
        wx.StaticText.__init__(self, argument_control, label=label,
                               size=argument_control.box_size,
                               style=wx.ALIGN_CENTER_HORIZONTAL)
        
        old_foreground_color = self.GetForegroundColour()        
        
        faint_color = wx_tools.mix_wx_color(0.5,
                                            old_foreground_color,
                                            wx_tools.get_background_color())
        self.SetForegroundColour(faint_color)
        
        self.SetMinSize(argument_control.box_size)
        self.SetMaxSize(argument_control.box_size)
            