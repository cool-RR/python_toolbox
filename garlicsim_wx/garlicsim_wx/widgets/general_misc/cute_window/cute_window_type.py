# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

import wx

from garlicsim.general_misc import dict_tools




class CuteWindowType(type):
    def __new__(mcls, name, bases, namespace):
        cls = super(CuteWindowType, mcls).__new__(mcls, name, bases, namespace)
        event_handlers = dict_tools.filter_items(
            namespace,
            lambda name, value: name.startswith('_on_') and callable(value)
        )
            
        # blocktodo: implement
            
        cls.___event_handlers = 1/0
        
        return cls

