# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines event-related tools.'''

import wx

from python_toolbox import caching
from python_toolbox.wx_tools.keyboard import Key


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
            

class ObjectWithId(object):
    Id = caching.CachedProperty(lambda object: wx.NewId())