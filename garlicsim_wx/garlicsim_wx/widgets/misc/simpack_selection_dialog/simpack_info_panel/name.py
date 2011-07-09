# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `Name` class.

See its documentation for more information.
'''

from garlicsim_wx.widgets.general_misc.cute_static_text import CuteStaticText



class Name(CuteStaticText):
    def __init__(self, simpack_info_panel):
        ''' '''
        self.simpack_info_panel = simpack_info_panel
        CuteStaticText.__init__(self, simpack_info_panel)
        