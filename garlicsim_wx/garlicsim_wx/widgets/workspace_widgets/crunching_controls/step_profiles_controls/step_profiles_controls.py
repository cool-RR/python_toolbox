# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

import pkg_resources
import wx

from garlicsim_wx.general_misc.third_party import aui
from garlicsim_wx.general_misc.flag_raiser import FlagRaiser
from garlicsim_wx.general_misc import emitters

import garlicsim, garlicsim_wx

    
class StepProfilesControls(wx.PaintEvent):
    '''tododoc'''
    
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.static_text = wx.StaticText(self, -1, 'Step profiles:')
        
        self.main_v_sizer.Add(self.static_text)
        
        #       self.s
        

