# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the App class.

See its documentation for more information.
'''

import wx

import garlicsim_wx


class App(wx.PySimpleApp):
    # todo: need to think if i allow frames with no app. on one hand good idea,
    # to allow people to start a garlicsim_wx frame in their own app. on other
    # hand frames will need to know how to start another frame.
    def __init__(self, *args, **keywords):
        self.frames = []
        super(App, self).__init__(*args, **keywords)
        
        
    def add_frame(self):
        frame = garlicsim_wx.Frame(
            app=self,
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