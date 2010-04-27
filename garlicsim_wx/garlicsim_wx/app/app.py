# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the class.

See its documentation for more information.
'''

import wx

import garlicsim_wx


class App(wx.PySimpleApp):
    def __init__(self, *args, **keywords):
        wx.PySimpleApp.__init__(self, *args, **keywords)
        self.frames = []
        
    def add_frame(self):
        frame = garlicsim_wx.Frame(
            parent=None,
            title="GarlicSim",
            size=(1140, 850)
        )
        self.frames.append(frame)
        return frame
    
    def OnInit(self):
        
        frame = self.add_frame()
        self.SetTopWindow(frame)
        
        return True