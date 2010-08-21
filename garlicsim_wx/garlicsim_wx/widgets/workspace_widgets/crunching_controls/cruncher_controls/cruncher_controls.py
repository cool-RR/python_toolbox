# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

import pkg_resources
import wx

import garlicsim, garlicsim_wx

    
class CruncherControls(wx.Panel):
    '''tododoc'''
    
    def __init__(self, parent, frame, *args, **kwargs):
        
        assert isinstance(frame, garlicsim_wx.Frame)
        self.frame = frame
        
        wx.Panel.__init__(self, parent, *args, **kwargs)

        
        self.main_v_sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.SetSizer(self.main_v_sizer)
        
        self.title_text = wx.StaticText(self, -1, 'Cruncher in use:')
        
        self.main_v_sizer.Add(self.title_text, 0)
        
        self.cruncher_in_use_static_text = \
            wx.StaticText(self, -1, 'CookieMonsterCruncher')
        self.cruncher_in_use_static_text.SetFont(
            wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL)
        )
        
        self.main_v_sizer.Add(self.cruncher_in_use_static_text, 0,
                              wx.EXPAND | wx.ALL, 5)
        
        
        self.change_cruncher_button = wx.Button(self, -1, 'Change...')
        
        self.main_v_sizer.Add(self.change_cruncher_button, 0,
                              wx.ALIGN_RIGHT, 0)
        

