# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

import wx

from garlicsim.general_misc import caching


map = {
    wx.Button: wx.EVT_BUTTON,
    wx.Menu: wx.EVT_MENU,
}

def get_event_code_of_component(component):
    if hasattr(component, '_EventHandlerGrokker__event_code'):
        return component._EventHandlerGrokker__event_code
    else:
        return _get_event_code_of_component_type(type(component))
    
@caching.cache()
def _get_event_code_of_component_type(component_type):    
    if hasattr(component_type, '_EventHandlerGrokker__event_code'):
        return component_type._EventHandlerGrokker__event_code
    else:
        return map[component_type]
           
    
@caching.cache()
def get_event_code_from_name(name):
    processed_name = 'EVT_%s' % name.upper()
    return getattr(wx, processed_name)