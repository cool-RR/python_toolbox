# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''Defines various tools for wxPython.'''

from __future__ import division
import wx

# maybe employ generic caching decorator here to make shorter

_background_color = None
def get_background_color():
    '''Get the background color on this platform.tododoc'''
    global _background_color
    if _background_color is not None:
        return _background_color
    
    result = wx.Color(212, 208, 200)
    '''
    todo: Not sure it's the right system color. Find the right one by comparing
    on different platforms. The right one is probably one of these:
    
    ['SYS_COLOUR_MENUBAR', 'SYS_COLOUR_SCROLLBAR', 'SYS_COLOUR_3DFACE',
    'SYS_COLOUR_INACTIVECAPTIONTEXT', 'SYS_COLOUR_3DLIGHT', 'SYS_COLOUR_MENU',
    'SYS_COLOUR_INACTIVEBORDER', 'SYS_COLOUR_BTNFACE',
    'SYS_COLOUR_ACTIVEBORDER']
    '''
    
    _background_color = result
    return result


_background_brush = None
def get_background_brush():
    '''Get the background brush for this platform.'''
    global _background_brush
    if _background_brush is not None:
        return _background_brush
    result = wx.Brush(get_background_color())
    _background_brush = result
    return result


def post_event(evt_handler, event_binder, source=None):
    # todo: Use wherever I post events
    event = wx.PyEvent(source.GetId() if source else 0)
    event.SetEventType(event_binder.evtType[0])
    wx.PostEvent(evt_handler, event)
    
    
class Key(object):    
    
    def __init__(self, key_code, cmd=False, alt=False, shift=False):
        self.key_code = key_code
        self.cmd = cmd
        self.alt = alt
        self.shift = shift
        
    @staticmethod
    def get_from_key_event(event):
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
    i = wx.RegionIterator(region)
    while i.HaveRects():
        yield i.GetRect()
        i.Next()
        


