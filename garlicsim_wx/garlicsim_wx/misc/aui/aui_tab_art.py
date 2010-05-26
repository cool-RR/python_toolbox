# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
This module defines the AuiTabArt class.

See its documentation for more info.
'''

import wx
from garlicsim_wx.general_misc.third_party import aui

# Imports for my copy-paste-modify overriding of some methods:
# # # #
from garlicsim_wx.general_misc.third_party.aui.aui_utilities import (
    BitmapFromBits, StepColour, IndentPressedBitmap, ChopText, GetBaseColour,
    DrawMACCloseButton, LightColour, TakeScreenShot, CopyAttributes)
from garlicsim_wx.general_misc.third_party.aui.aui_constants import *
# # # #


class AuiTabArt(aui.AuiDefaultTabArt):
    '''A tab art provider.'''
    def __init__(self):
        aui.AuiDefaultTabArt.__init__(self)
        
        font_size = 9 if wx.Platform == '__WXMAC__' else 7
        
        self.SetNormalFont(wx.Font(font_size, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL))
        self.SetSelectedFont(wx.Font(font_size, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL))
        self.SetMeasuringFont(wx.Font(font_size, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL))
 
        
    def Clone(self):

        art = type(self)()
        art.SetNormalFont(self.GetNormalFont())
        art.SetSelectedFont(self.GetSelectedFont())
        art.SetMeasuringFont(self.GetMeasuringFont())

        art = aui.aui_utilities.CopyAttributes(art, self)
        return art

    
    def DrawTab(self, dc, wnd, page, in_rect, close_button_state, paint_control=False):
        # A copy-paste-modify override. Changes marked with "# IS A CHANGE"
        """
        Draws a single tab.

        :param `dc`: a `wx.DC` device context;
        :param `wnd`: a `wx.Window` instance object;
        :param `page`: the tab control page associated with the tab;
        :param `in_rect`: rectangle the tab should be confined to;
        :param `close_button_state`: the state of the close button on the tab;
        :param `paint_control`: whether to draw the control inside a tab (if any) on a `wx.MemoryDC`.
        """

        # if the caption is empty, measure some temporary text
        caption = page.caption
        if not caption:
            caption = "Xj"

        dc.SetFont(self._selected_font)
        selected_textx, selected_texty, dummy = dc.GetMultiLineTextExtent(caption)

        dc.SetFont(self._normal_font)
        normal_textx, normal_texty, dummy = dc.GetMultiLineTextExtent(caption)

        control = page.control

        # figure out the size of the tab
        tab_size, x_extent = self.GetTabSize(dc, wnd, page.caption, page.bitmap,
                                             page.active, close_button_state, control)

        tab_height = self._tab_ctrl_height - 3
        tab_width = tab_size[0]
        tab_x = in_rect.x
        tab_y = in_rect.y + in_rect.height - tab_height

        caption = page.caption

        # select pen, brush and font for the tab to be drawn

        if page.active:
        
            dc.SetFont(self._selected_font)
            textx, texty = selected_textx, selected_texty
        
        else:
        
            dc.SetFont(self._normal_font)
            textx, texty = normal_textx, normal_texty

        if not page.enabled:
            dc.SetTextForeground(wx.SystemSettings.GetColour(wx.SYS_COLOUR_GRAYTEXT))
            pagebitmap = page.dis_bitmap
        else:
            dc.SetTextForeground(page.text_colour)
            pagebitmap = page.bitmap
            
        # create points that will make the tab outline

        clip_width = tab_width
        if tab_x + clip_width > in_rect.x + in_rect.width:
            clip_width = in_rect.x + in_rect.width - tab_x

        # since the above code above doesn't play well with WXDFB or WXCOCOA,
        # we'll just use a rectangle for the clipping region for now --
        dc.SetClippingRegion(tab_x, tab_y, clip_width+1, tab_height-3)

        border_points = [wx.Point() for i in xrange(6)]
        agwFlags = self.GetAGWFlags()
        
        if agwFlags & AUI_NB_BOTTOM:
        
            border_points[0] = wx.Point(tab_x,             tab_y)
            border_points[1] = wx.Point(tab_x,             tab_y+tab_height-6)
            border_points[2] = wx.Point(tab_x+2,           tab_y+tab_height-4)
            border_points[3] = wx.Point(tab_x+tab_width-2, tab_y+tab_height-4)
            border_points[4] = wx.Point(tab_x+tab_width,   tab_y+tab_height-6)
            border_points[5] = wx.Point(tab_x+tab_width,   tab_y)
        
        else: #if (agwFlags & AUI_NB_TOP) 
        
            border_points[0] = wx.Point(tab_x,             tab_y+tab_height-4)
            border_points[1] = wx.Point(tab_x,             tab_y+2)
            border_points[2] = wx.Point(tab_x+2,           tab_y)
            border_points[3] = wx.Point(tab_x+tab_width-2, tab_y)
            border_points[4] = wx.Point(tab_x+tab_width,   tab_y+2)
            border_points[5] = wx.Point(tab_x+tab_width,   tab_y+tab_height-4)
        
        # TODO: else if (agwFlags & AUI_NB_LEFT) 
        # TODO: else if (agwFlags & AUI_NB_RIGHT) 

        drawn_tab_yoff = border_points[1].y
        drawn_tab_height = border_points[0].y - border_points[1].y

        if page.active:
        
            # draw active tab

            # draw base background colour
            r = wx.Rect(tab_x, tab_y, tab_width, tab_height)
            dc.SetPen(self._base_colour_pen)
            dc.SetBrush(self._base_colour_brush)
            dc.DrawRectangle(r.x+1, r.y+1, r.width-1, r.height-4)

            # this white helps fill out the gradient at the top of the tab
            dc.SetPen(wx.WHITE_PEN)
            dc.SetBrush(wx.WHITE_BRUSH)
            dc.DrawRectangle(r.x+2, r.y+1, r.width-3, r.height-4)

            # these two points help the rounded corners appear more antialiased
            dc.SetPen(self._base_colour_pen)
            dc.DrawPoint(r.x+2, r.y+1)
            dc.DrawPoint(r.x+r.width-2, r.y+1)

            # set rectangle down a bit for gradient drawing
            r.SetHeight(r.GetHeight()/2)
            r.x += 2
            r.width -= 2
            r.y += r.height
            r.y -= 2

            # draw gradient background
            top_colour = wx.WHITE
            bottom_colour = self._base_colour
            dc.GradientFillLinear(r, bottom_colour, top_colour, wx.NORTH)
        
        else:
        
            # draw inactive tab

            r = wx.Rect(tab_x, tab_y+1, tab_width, tab_height-3)

            # start the gradent up a bit and leave the inside border inset
            # by a pixel for a 3D look.  Only the top half of the inactive
            # tab will have a slight gradient
            r.x += 3
            r.y += 1
            r.width -= 4
            r.height /= 2
            r.height -= 1

            # -- draw top gradient fill for glossy look
            top_colour = self._base_colour
            bottom_colour = StepColour(top_colour, 160)
            dc.GradientFillLinear(r, bottom_colour, top_colour, wx.NORTH)

            r.y += r.height
            r.y -= 1

            # -- draw bottom fill for glossy look
            top_colour = self._base_colour
            bottom_colour = self._base_colour
            dc.GradientFillLinear(r, top_colour, bottom_colour, wx.SOUTH)
        
        # draw tab outline
        dc.SetPen(self._border_pen)
        dc.SetBrush(wx.TRANSPARENT_BRUSH)
        dc.DrawPolygon(border_points)

        # there are two horizontal grey lines at the bottom of the tab control,
        # this gets rid of the top one of those lines in the tab control
        if page.active:
        
            if agwFlags & AUI_NB_BOTTOM:
                dc.SetPen(wx.Pen(StepColour(self._base_colour, 170)))
                
            # TODO: else if (agwFlags & AUI_NB_LEFT) 
            # TODO: else if (agwFlags & AUI_NB_RIGHT) 
            else: # for AUI_NB_TOP
                dc.SetPen(self._base_colour_pen)
                
            dc.DrawLine(border_points[0].x+1,
                        border_points[0].y,
                        border_points[5].x,
                        border_points[5].y)
        
        text_offset = tab_x + 8
        close_button_width = 0

        if close_button_state != AUI_BUTTON_STATE_HIDDEN:
            close_button_width = self._active_close_bmp.GetWidth()

            if agwFlags & AUI_NB_CLOSE_ON_TAB_LEFT:
                text_offset += close_button_width - 5
                
        bitmap_offset = 0
        
        if pagebitmap.IsOk():
        
            bitmap_offset = tab_x + 8
            if agwFlags & AUI_NB_CLOSE_ON_TAB_LEFT and close_button_width:
                bitmap_offset += close_button_width - 5

            # draw bitmap
            dc.DrawBitmap(pagebitmap,
                          bitmap_offset,
                          drawn_tab_yoff + (drawn_tab_height/2) - (pagebitmap.GetHeight()/2),
                          True)

            text_offset = bitmap_offset + pagebitmap.GetWidth()
            text_offset += 3 # bitmap padding

        else:

            if agwFlags & AUI_NB_CLOSE_ON_TAB_LEFT == 0 or not close_button_width:
                text_offset = tab_x + 8
        
        draw_text = ChopText(dc, caption, tab_width - (text_offset-tab_x) - close_button_width)

        ypos = drawn_tab_yoff + (drawn_tab_height)/2 - (texty/2) + 1 # IS A CHANGE

        offset_focus = text_offset     
        if control is not None:
            if control.GetPosition() != wx.Point(text_offset+1, ypos):
                control.SetPosition(wx.Point(text_offset+1, ypos))

            if not control.IsShown():
                control.Show()

            if paint_control:
                bmp = TakeScreenShot(control.GetScreenRect())
                dc.DrawBitmap(bmp, text_offset+1, ypos, True)
                
            controlW, controlH = control.GetSize()
            text_offset += controlW + 4
            textx += controlW + 4
            
        # draw tab text
        rectx, recty, dummy = dc.GetMultiLineTextExtent(draw_text)
        dc.DrawLabel(draw_text, wx.Rect(text_offset, ypos, rectx, recty))

        # draw focus rectangle
        self.DrawFocusRectangle(dc, page, wnd, draw_text, offset_focus, bitmap_offset, drawn_tab_yoff, drawn_tab_height, textx, texty)
        
        out_button_rect = wx.Rect()
        
        # draw close button if necessary
        if close_button_state != AUI_BUTTON_STATE_HIDDEN:
        
            bmp = self._disabled_close_bmp

            if close_button_state == AUI_BUTTON_STATE_HOVER:
                bmp = self._hover_close_bmp
            elif close_button_state == AUI_BUTTON_STATE_PRESSED:
                bmp = self._pressed_close_bmp

            shift = (agwFlags & AUI_NB_BOTTOM and [1] or [0])[0]

            if agwFlags & AUI_NB_CLOSE_ON_TAB_LEFT:
                rect = wx.Rect(tab_x + 4, tab_y + (tab_height - bmp.GetHeight())/2 - shift,
                               close_button_width, tab_height)
            else:
                rect = wx.Rect(tab_x + tab_width - close_button_width - 1,
                               tab_y + (tab_height - bmp.GetHeight())/2 - shift,
                               close_button_width, tab_height)

            rect = IndentPressedBitmap(rect, close_button_state)
            dc.DrawBitmap(bmp, rect.x, rect.y, True)

            out_button_rect = rect
        
        out_tab_rect = wx.Rect(tab_x, tab_y, tab_width, tab_height)

        dc.DestroyClippingRegion()

        return out_tab_rect, out_button_rect, x_extent