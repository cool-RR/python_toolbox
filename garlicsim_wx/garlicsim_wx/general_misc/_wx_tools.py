# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

# blocktodo: delete this file

import wx

from garlicsim.general_misc import caching
from garlicsim.general_misc.context_manager import ContextManager



def post_event(evt_handler, event_binder, source=None, **kwargs):
    '''Post an event to an evt_handler.'''
    # todo: Use wherever I post events    
    # todo: possibly it's a problem that I'm using PyEvent here for any type of
    # event, because every event has its own type. but i don't know how to get
    # the event type from `event_binder`. problem.
    event = wx.PyCommandEvent(event_binder.evtType[0],
                              source.GetId() if source else 0)
    for key, value in kwargs.iteritems():
        setattr(event, key, value)
    event.SetEventType(event_binder.evtType[0])
    wx.PostEvent(evt_handler, event)
    
    

        
    


def navigate_from_key_event(key_event):
    '''
    Figure out if `key_event` is a navigation button press, if so navigate.
    
    Returns whether there was navigation action or not.
    '''
    key = Key.get_from_key_event(key_event)
    
    if key in [Key(wx.WXK_TAB), Key(wx.WXK_TAB, shift=True),
               Key(wx.WXK_TAB, cmd=True),
               Key(wx.WXK_TAB, cmd=True, shift=True)]:
        
        window = key_event.GetEventObject()
        
        flags = 0
        
        if key.shift:
            flags |= wx.NavigationKeyEvent.IsBackward
        else: # not key.shift
            flags |= wx.NavigationKeyEvent.IsForward
        
        if key.cmd:
            flags |= wx.NavigationKeyEvent.WinChange
        
        
        current_window = window
        while not current_window.Parent.HasFlag(wx.TAB_TRAVERSAL):
            current_window = current_window.Parent
        current_window.Navigate(flags)
        return True
    
    else:
        return False
            

    
def iter_rects_of_region(region):
    '''Iterate over the rects of a region.'''
    i = wx.RegionIterator(region)
    while i.HaveRects():
        yield i.GetRect()
        i.Next()
        


def color_replaced_bitmap(bitmap, old_rgb, new_rgb):
    '''Replace all appearances of `old_rgb` with `new_rgb` in `bitmap`.'''
    old_r, old_g, old_b = old_rgb
    new_r, new_g, new_b = new_rgb
    image = wx.ImageFromBitmap(bitmap)
    assert isinstance(image, wx.Image)
    image.Replace(old_r, old_g, old_b, new_r, new_g, new_b)
    return wx.BitmapFromImage(image)
    

        
        
class CursorChanger(ContextManager):
    '''Context manager for showing specified cursor while suite executes.'''
    def __init__(self, window, cursor):
        '''
        Construct the `CursorChanger`.
        
        `cursor` may be either a `wx.Cursor` object or a constant like
        `wx.CURSOR_BULLSEYE`.
        '''
        assert isinstance(window, wx.Window)
        self.window = window
        self.cursor = cursor if isinstance(cursor, wx.Cursor) \
            else wx.StockCursor(cursor)
        self.old_cursor = window.GetCursor()
    def __enter__(self):
        self.window.SetCursor(self.cursor)
    def __exit__(self, *args, **kwargs):
        self.window.SetCursor(self.old_cursor)
        

    
