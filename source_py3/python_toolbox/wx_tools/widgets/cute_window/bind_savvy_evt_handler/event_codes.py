# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Module for obtaining event codes.'''

import wx
import wx.lib.buttons

from python_toolbox import caching
from python_toolbox import sequence_tools
from python_toolbox import address_tools
from python_toolbox import string_tools


def monkeypatch_wx():
    '''Give event code attributes to several built-in wxPython widgets.'''
    
    # Using `wx.EVT_MENU` for buttons (in addition to `wx.EVT_BUTTON`)
    # because that's the event created by invoking a button's accelerator on
    # Mac:
    wx.Button._EventHandlerGrokker__event_code = \
      wx.lib.buttons.GenButton._EventHandlerGrokker__event_code = \
      (wx.EVT_BUTTON, wx.EVT_MENU)
    
    wx.Menu._EventHandlerGrokker__event_code = wx.EVT_MENU
    wx.MenuItem._EventHandlerGrokker__event_code = wx.EVT_MENU
    
    wx.Timer._EventHandlerGrokker__event_code = wx.EVT_TIMER

monkeypatch_wx()


def get_event_codes_of_component(component):
    '''Get the event codes that should be bound to `component`.'''
    return sequence_tools.to_tuple(component._EventHandlerGrokker__event_code)
           
    
@caching.cache()
def get_event_code_from_name(name, evt_handler_type):
    '''
    Get an event code given a `name` and an `evt_handler_type`.
    
    For example, given a `name` of `left_down` this function will return the
    event code `wx.EVT_LEFT_DOWN`.
    
    If `evt_handler_type` has an `.event_modules` attribute, these modules will
    be searched for event codes in precedence to `wx` and the event handler
    type's own module.
    '''
    processed_name = 'EVT_%s' % string_tools.case_conversions. \
                                camel_case_to_lower_case(name).upper()
    raw_event_modules = sequence_tools.to_tuple(evt_handler_type.event_modules)
    event_modules = raw_event_modules + (
        address_tools.resolve(evt_handler_type.__module__),
        wx
    )
    for event_module in event_modules:
        try:
            return getattr(event_module, processed_name)
        except AttributeError:
            pass
    else:
        raise LookupError("Couldn't find event by the name of '%s'." %
                          processed_name)
    