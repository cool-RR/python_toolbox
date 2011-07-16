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
'''The different acceptable names for simpack's preview images.'''


@caching.cache()
def get_simpack_bitmap(simpack_metadata):
    '''
    Get a simpack's preview image as bitmap, or `None` if there isn't one.
    '''
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
    '''Panel that shows a preview image of the selected simpack.'''

    def __init__(self, simpack_info_panel):
        '''
        Construct the `ImageDisplay`, using `simpack_info_panel` as parent.
        '''
        self.simpack_info_panel = simpack_info_panel
        CutePanel.__init__(self, simpack_info_panel)
        self.HelpText = 'A preview image of the currently-selected simpack.'
        if wx_tools.is_gtk:
            self.set_good_background_color()
        self._bitmap = wx.EmptyBitmap(1, 1)
        self.bind_event_handlers(ImageDisplay)
        self.Hide()
        
        
    def refresh(self):
        '''Show the image of the currently-selected simpack.'''
        simpack_metadata = \
            self.simpack_info_panel.simpack_selection_dialog.simpack_metadata
        if simpack_metadata is not None:
            self._bitmap = get_simpack_bitmap(simpack_metadata)
            self.Show()
        else: # simpack_metadata is None
            self.Hide()

        
    def _on_set_focus(self, event):
        event.Skip()
        self.Navigate()
        
        
    def _on_paint(self, event):
        dc = wx.PaintDC(self)
        
        if self._bitmap:
            client_width, client_height = self.ClientSize
            client_origin_x, client_origin_y = self.ClientAreaOrigin
            
            bitmap_width, bitmap_height = self._bitmap.Size
            bitmap_origin_x = (client_width - bitmap_width) / 2
            bitmap_origin_y = (client_height- bitmap_height) / 2
            dc.DrawBitmap(self._bitmap, bitmap_origin_x, bitmap_origin_y)
            
            dc.SetPen(wx.Pen(wx.NamedColour('black')))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.DrawRectangle(client_origin_x, client_origin_y,
                             client_width, client_height)
