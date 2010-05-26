# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''Defines various tools for wxPython.'''

from __future__ import division
import wx


# employ generic caching decorator here to make shorter

_background_color = None
def get_background_color():
    '''Get the default garlicsim_wx background color'''
    global _background_color
    if _background_color is not None:
        return _background_color
    
    result = wx.Color(212, 208, 200)
    '''
    NOTE I'M ACTUALLY USING A CONSTANT COLOR NOW. THIS COMMENT IS NOT RELEVANT
    RIGHT NOW:    
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
    '''Get the default garlicsim_wx background brush.'''
    global _background_brush
    if _background_brush is not None:
        return _background_brush
    result = wx.Brush(get_background_color())
    _background_brush = result
    return result


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
        


