# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `Placeholder` class.

See its documentation for more details.
'''

import wx

from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.general_misc import color_tools


class Placeholder(wx.StaticText):
    '''Placeholder for functions that don't have extraneous arguments.'''
    def __init__(self, argument_control, argument_kind):
        self.argument_control = argument_control
        self.argument_kind = argument_kind
        
        wx.StaticText.__init__(
            self,
            argument_control,
            label='(No %s )' % argument_kind,
            size=argument_control.box_size,
            style=wx.ALIGN_CENTER_HORIZONTAL
        )
        self.HelpText = ("The currently selected step function doesn't take "
                         "any %s." % argument_kind)
        old_foreground_color = self.GetForegroundColour()        
        
        faint_color = wx_tools.colors.mix_wx_color(
            0.5,
            old_foreground_color,
            wx_tools.colors.get_background_color()
        )
        self.SetForegroundColour(faint_color)
        
        self.SetMinSize(argument_control.box_size)
        self.SetMaxSize(argument_control.box_size)
            