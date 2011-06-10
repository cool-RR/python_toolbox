# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

import wx

from garlicsim.general_misc import caching

# blocktododoc: in a monkeypatch function?
wx.Button._EventHandlerGrokker__event_code = wx.EVT_BUTTON
wx.Menu._EventHandlerGrokker__event_code = wx.EVT_MENU
wx.Timer._EventHandlerGrokker__event_code = wx.EVT_TIMER


def get_event_code_of_component(component):
    return component._EventHandlerGrokker__event_code
           
    
@caching.cache()
def get_event_code_from_name(name):
    processed_name = 'EVT_%s' % name.upper()
    return getattr(wx, processed_name)