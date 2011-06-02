# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

import wx


class EventHandlerGrokker(object):
    @classmethod
    def create_from_name(cls, name, event_handler):
        assert name.startswith('_on_')
        
        