# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Module for obtaining event codes.'''

import wx
import wx.lib.buttons

from garlicsim.general_misc import caching
from garlicsim.general_misc import sequence_tools
from garlicsim.general_misc import address_tools
from garlicsim.general_misc import string_tools


def monkeypatch_wx():
    '''Give event code attributes to several built-in wxPython widgets.'''
    
    # Using `wx.EVT_MENU` for buttons (in addition to `wx.EVT_BUTTON`)
    # because that's the event created by invoking a button's accelerator on
    # Mac:
    wx.Button._EventHandlerGrokker__event_code = \
      wx.lib.buttons.GenButton._EventHandlerGrokker__event_code = \
      (wx.EVT_BUTTON, wx.EVT_MENU)
    
    wx.Menu._EventHandlerGrokker__event_code = wx.EVT_MENU
    
    wx.Timer._EventHandlerGrokker__event_code = wx.EVT_TIMER

monkeypatch_wx()


def get_event_codes_of_component(component):
    '''Get the event codes that should be bound to `component`.'''
    return sequence_tools.to_tuple(component._EventHandlerGrokker__event_code)
           
    
@caching.cache()
def get_event_code_from_name(name, window_type):
    '''
    Get an event code given a `name` and a `window_type`.
    
    For example, given a `name` of `left_down` this function will return the
    event code `wx.EVT_LEFT_DOWN`.
    
    If `window_type` has an `.event_modules` attribute, these modules will be
    searched for event codes in precedence to `wx` and the window type's own
    module.
    '''
    processed_name = 'EVT_%s' % string_tools.conversions.\
                                camelcase_to_underscore(name).upper()
    raw_event_modules = \
        (window_type.event_modules if
         sequence_tools.is_sequence(window_type.event_modules) else 
         [window_type.event_modules])
    event_modules = raw_event_modules + [
        address_tools.resolve(window_type.__module__),
        wx
    ]
    for event_module in event_modules:
        try:
            return getattr(event_module, processed_name)
        except AttributeError:
            pass
    else:
        raise LookupError("Couldn't find event by the name of '%s'." %
                          processed_name)
    