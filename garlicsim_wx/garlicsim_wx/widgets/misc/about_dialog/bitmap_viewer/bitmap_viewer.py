# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `BitmapViewer` class.

See its documentation for more info.
'''

import wx

from garlicsim_wx.widgets.general_misc.cute_panel import CutePanel


class BitmapViewer(CutePanel):
    '''Widget for viewing a bitmap. Similar to `StaticBitmap`.'''
    
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        #self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self._bitmap = wx.EmptyBitmap(1, 1)
        self.bind_event_handlers(BitmapViewer)

        
    def set_bitmap(self, bitmap):
        '''Set the bitmap that the viewer will display.'''
        self._bitmap = bitmap
        self.Refresh()

        
    ### Event handlers: #######################################################
    #                                                                         #
    def _on_set_focus(self, event):
        event.Skip()
        self.Navigate()
        
    def _on_paint(self, event):
        dc = wx.PaintDC(self)
        dc.DrawBitmap(self._bitmap, 0, 0)   
    #                                                                         #
    ### Finished event handlers. ##############################################
