# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `ImageDisplay` class.

See its documentation for more information.
'''

from __future__ import division

import wx

from garlicsim.general_misc import caching
from garlicsim.general_misc import module_tasting
from garlicsim_wx.widgets.general_misc.cute_panel import CutePanel
from garlicsim_wx.general_misc import wx_tools


possible_image_names = [
    'preview.png',
    'preview.jpg',
    'preview.gif'
]


@caching.cache()
def get_simpack_bitmap(simpack_metadata):
    for possible_image_name in possible_image_names:
        if module_tasting.tasted_resources.resource_exists(
            simpack_metadata._tasted_simpack,
            possible_image_name
        ):
            stream = module_tasting.tasted_resources.resource_stream(
                simpack_metadata._tasted_simpack,
                possible_image_name
            )
            return wx.BitmapFromImage(wx.ImageFromStream(stream))
            
    else:
        return None


class ImageDisplay(CutePanel):

    def __init__(self, simpack_info_panel):
        self.simpack_info_panel = simpack_info_panel
        CutePanel.__init__(self, simpack_info_panel)
        if wx_tools.is_gtk:
            self.set_good_background_color()
        self._bitmap = wx.EmptyBitmap(1, 1)
        #self.BackgroundColour = wx.NamedColour('red')
        self.bind_event_handlers(ImageDisplay)
        self.Hide()
        
        
    def refresh(self):
        simpack_metadata = \
            self.simpack_info_panel.simpack_selection_dialog.simpack_metadata
        if simpack_metadata is not None:
            self._bitmap = get_simpack_bitmap(simpack_metadata)
            self.Show()
            self.Layout()
            self.Refresh()
        else: # simpack_metadata is None
            self.Hide()

        
    def _on_set_focus(self, event):
        event.Skip()
        self.Navigate()

        
    def _on_paint(self, event):
        dc = wx.PaintDC(self)
        
        if self._bitmap:
            width, height = self.ClientSize
            bitmap_width, bitmap_height = self._bitmap.Size
            origin_x = (width - bitmap_width) / 2
            origin_y = (height- bitmap_height) / 2
            dc.DrawBitmap(self._bitmap, origin_x, origin_y)
