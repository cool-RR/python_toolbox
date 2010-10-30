# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the CuteDialog class.

See its documentation for more info.
'''

import wx

from garlicsim_wx.general_misc import wx_tools


class CuteDialog(wx.Dialog):
    '''
    Dialog.
    
    Differences from wx.Dialog:
    1. Works around a Mac bug by centering itself on the screen.
    2. Uses garlicsim_wx's default background color.
    '''
    def __init__(self, *args, **kwargs):
        if not kwargs.pop('skip_dialog_init', False):
            wx.Dialog.__init__(self, *args, **kwargs)
        self.SetBackgroundColour(wx_tools.get_background_color())
        
    def ShowModal(self):
        #if True: #wx.Platform == '__WXMAC__':
            #self.Centre(wx.BOTH)
            #def try_center():
                #try:
                    #wx_tools.center_on_top_level_parent(self)
                #except Exception:
                    ## Solve problem, fuck `try` and lambdize.
                    ## Problem:
                    ## http://groups.google.com/group/wxpython-users/
                    ## browse_thread/thread/63a30859da024c9e
                    #pass
                
            ##wx.CallAfter(try_center)
            #try_center()
                
        self.Centre(wx.BOTH)
        return super(CuteDialog, self).ShowModal()
    
