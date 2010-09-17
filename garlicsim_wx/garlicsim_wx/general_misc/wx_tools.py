# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''Defines various tools for wxPython.'''

from __future__ import division

import warnings
import colorsys

import wx

from garlicsim.general_misc import caching


@caching.cache
def get_background_color():
    '''Get the default garlicsim_wx background color'''
    
    if wx.Platform == '__WXMSW__':
        # return wx.Color(212, 208, 200)
        return wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENUBAR)
    elif wx.Platform == '__WXMAC__':
        return wx.Color(232, 232, 232)
    elif wx.Platform == '__WXGTK__':
        # Until SYS_COLOUR_* get their act togother, we're using Windows colors
        # for Linux.
        return wx.Color(212, 208, 200)
    
    else:
        warnings.warn("Unidentified platform! It's neither '__WXGTK__', "
                      "'__WXMAC__' nor '__WXMSW__'. Things might not work "
                      "properly.")
        return wx.Color(212, 208, 200)


@caching.cache
def get_background_brush():
    '''Get the default garlicsim_wx background brush.'''
    return wx.Brush(get_background_color())


def wx_color_to_html_color(color):
    rgb = color.GetRGB()
    (green_blue, red) = divmod(rgb, 256)
    (blue, green) = divmod(green_blue, 256)
    return '#%02x%02x%02x' % (red, green, blue)


def hls_to_wx_color(hls):
    return wx.Color(*colorsys.hls_to_rgb(*hls))


def wx_color_to_hls(color):
    return colorsys.rgb_to_hls(color.red, color.blue, color.green)


def post_event(evt_handler, event_binder, source=None):
    '''Post an event to an evt_handler.'''
    # todo: Use wherever I post events
    event = wx.PyEvent(source.GetId() if source else 0)
    event.SetEventType(event_binder.evtType[0])
    wx.PostEvent(evt_handler, event)
    
    
class Key(object):    
    '''A key combination.'''

    def __init__(self, key_code, cmd=False, alt=False, shift=False):

        self.key_code = key_code        
        '''The numerical code of the pressed key.'''
        
        self.cmd = cmd
        '''Flag saying whether the ctrl/cmd key was pressed.'''
        
        self.alt = alt
        '''Flag saying whether the alt key was pressed.'''
        
        self.shift = shift
        '''Flag saying whether the shift key was pressed.'''
        
        
    @staticmethod
    def get_from_key_event(event):
        '''Construct a Key from a wx.EVT_KEY_DOWN event.'''
        return Key(event.GetKeyCode(), event.CmdDown(),
                   event.AltDown(), event.ShiftDown())
    
    def __hash__(self):
        return hash(tuple(sorted(tuple(vars(self)))))
    
    def __eq__(self, other):
        if not isinstance(other, Key):
            return NotImplemented
        return self.key_code == other.key_code and \
               self.cmd == other.cmd and \
               self.shift == other.shift and \
               self.alt == other.alt
        
    
def iter_rects_of_region(region):
    '''Iterate over the rects of a region.'''
    i = wx.RegionIterator(region)
    while i.HaveRects():
        yield i.GetRect()
        i.Next()
        


