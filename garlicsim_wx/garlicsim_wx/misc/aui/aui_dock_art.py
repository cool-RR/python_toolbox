# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
This module defines the AuiDockArt class.

See its documentation for more info.
'''

import wx

from garlicsim_wx.general_misc.third_party import aui
from garlicsim_wx.general_misc import wx_tools

# Imports for my copy-paste-modify overriding of some methods:
# # # #
import types
from garlicsim_wx.general_misc.third_party.aui.aui_utilities import (
    BitmapFromBits, StepColour, ChopText, GetBaseColour, DrawGradientRectangle,
    DrawMACCloseButton, DarkenBitmap, LightContrastColour)
from garlicsim_wx.general_misc.third_party.aui.aui_constants import *

optionActive = 2**14
# # # #



class AuiDockArt(aui.AuiDefaultDockArt):
    '''A dock art provider.'''
    def __init__(self):
        aui.AuiDefaultDockArt.__init__(self)
 
        self.SetColor(
            aui.AUI_DOCKART_BACKGROUND_GRADIENT_COLOUR,
            self.GetColor(
                aui.AUI_DOCKART_BACKGROUND_COLOUR
            )
        )
        
        self.SetMetric(aui.AUI_DOCKART_SASH_SIZE, 2)
        
        font_size = 9 if wx.Platform == '__WXMAC__' else 7
        
        self.SetMetric(aui.AUI_DOCKART_CAPTION_SIZE, 11)
        self.SetFont(
            aui.AUI_DOCKART_CAPTION_FONT,
            wx.Font(font_size, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL, False)
        )
        
        #self.SetMetric(aui.AUI_DOCKART_GRADIENT_TYPE,
        #               aui.AUI_GRADIENT_NONE)
        
        self.SetColor(aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR,
                      wx_tools.get_background_color())

        
    def DrawCaption(self, dc, window, text, rect, pane):
        # A copy-paste-modify override. Changes not marked, you can diff.
        """
        Draws the text in the pane caption.

        :param `dc`: a `wx.DC` device context;
        :param `window`: an instance of `wx.Window`;
        :param `text`: the text to be displayed;
        :param `rect`: the pane caption rectangle;
        :param `pane`: the pane for which the text is drawn.
        """

        dc.SetPen(wx.TRANSPARENT_PEN)
        dc.SetFont(self._caption_font)
        
        self.DrawCaptionBackground(dc, rect, pane)

        if pane.state & optionActive:
            dc.SetTextForeground(self._active_caption_text_colour)
        else:
            dc.SetTextForeground(self._inactive_caption_text_colour)

        w, h = dc.GetTextExtent("ABCDEFHXfgkj")

        clip_rect = wx.Rect(*rect)
        btns = pane.CountButtons()

        captionLeft = pane.HasCaptionLeft()
        variable = (captionLeft and [rect.height] or [rect.width])[0]

        variable -= 3      # text offset
        variable -= 2      # button padding

        caption_offset = 0
        if pane.icon:
            if captionLeft:
                caption_offset += pane.icon.GetHeight() + 3
            else:
                caption_offset += pane.icon.GetWidth() + 3
                
            self.DrawIcon(dc, rect, pane)

        variable -= caption_offset
        variable -= btns*(self._button_size + self._border_size)
        draw_text = ChopText(dc, text, variable)

        if captionLeft:
            dc.DrawRotatedText(draw_text, rect.x+(rect.width/2)-(h/2)-1, rect.y+rect.height-3-caption_offset, 90)
        else:
            dc.DrawText(draw_text, rect.x+3+caption_offset, rect.y+(rect.height/2)-(h/2))
            
    


    def SetColor(self, id, colour):
        # A copy-paste-modify override. Changes marked with "# IS A CHANGE"
        """
        Sets the colour of a certain setting.

        :param `id`: can be one of the colour values in `Metric Ordinals`;
        :param `colour`: the new value of the setting.
        """

        if isinstance(colour, basestring):
            colour = wx.NamedColour(colour)
        elif isinstance(colour, types.TupleType):
            colour = wx.Colour(*colour)
        elif isinstance(colour, types.IntType):
            colour = wx.ColourRGB(colour)
        
        if id == AUI_DOCKART_BACKGROUND_COLOUR:
            self._background_brush.SetColour(colour)
        elif id == AUI_DOCKART_BACKGROUND_GRADIENT_COLOUR:
            self._background_gradient_colour = colour
        elif id == AUI_DOCKART_SASH_COLOUR:
            self._sash_brush.SetColour(colour)
        elif id == AUI_DOCKART_INACTIVE_CAPTION_COLOUR:
            self._inactive_caption_colour = colour
            if not self._custom_pane_bitmaps and wx.Platform == "__WXMAC__":
                # No custom bitmaps for the pane close button
                # Change the MAC close bitmap colour
                pass # # self._inactive_close_bitmap = DrawMACCloseButton(wx.WHITE, colour)
                # IS A CHANGE

        elif id == AUI_DOCKART_INACTIVE_CAPTION_GRADIENT_COLOUR:
            self._inactive_caption_gradient_colour = colour
        elif id == AUI_DOCKART_INACTIVE_CAPTION_TEXT_COLOUR:
            self._inactive_caption_text_colour = colour
        elif id == AUI_DOCKART_ACTIVE_CAPTION_COLOUR:
            self._active_caption_colour = colour
            if not self._custom_pane_bitmaps and wx.Platform == "__WXMAC__":
                # No custom bitmaps for the pane close button
                # Change the MAC close bitmap colour
                pass # self._active_close_bitmap = DrawMACCloseButton(wx.WHITE, colour)
                # IS A CHANGE
                
        elif id == AUI_DOCKART_ACTIVE_CAPTION_GRADIENT_COLOUR:
            self._active_caption_gradient_colour = colour
        elif id == AUI_DOCKART_ACTIVE_CAPTION_TEXT_COLOUR:
            self._active_caption_text_colour = colour
        elif id == AUI_DOCKART_BORDER_COLOUR:
            self._border_pen.SetColour(colour)
        elif id == AUI_DOCKART_GRIPPER_COLOUR:
            self._gripper_brush.SetColour(colour)
            self._gripper_pen1.SetColour(StepColour(colour, 40))
            self._gripper_pen2.SetColour(StepColour(colour, 60))
        else:
            raise Exception("Invalid Colour Ordinal.")
