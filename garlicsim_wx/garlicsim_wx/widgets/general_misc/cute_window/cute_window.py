# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `` class.

See its documentation for more information.
'''

import wx

from garlicsim_wx.general_misc import wx_tools
from garlicsim.general_misc import caching
from garlicsim.general_misc import freezers
from garlicsim.general_misc.context_managers import ContextManager

from .accelerator_savvy_window import AcceleratorSavvyWindow
from .bind_savvy_window import BindSavvyWindow


class CuteWindow(AcceleratorSavvyWindow, BindSavvyWindow, wx.Window):
    '''
    An improved `wx.Window`.
    
    The advantages of this class over `wx.Window`:
    
      - A `.freezer` property for freezing the window.  
      - A `.create_cursor_changer` method which creates a `CursorChanger`
       context manager for temporarily changing the cursor.
      - A `set_good_background_color` for setting a good background color.
      # blocktododoc
     
    This class doesn't require calling its `__init__` when subclassing. (i.e.,
    you *may* call its `__init__` if you want, but it will do the same as
    calling `wx.Window.__init__`.) # blocktododoc: remove notice?
    '''
    
    freezer = freezers.FreezerProperty(
        freezer_type=wx_tools.window_tools.WindowFreezer,
        doc='''Freezer for freezing the window while the suite executes.'''
    )
    
    def create_cursor_changer(self, cursor):
        '''
        Create a `CursorChanger` context manager for ...blocktotodoc
        
        `cursor` may be either a `wx.Cursor` object or a constant like
        `wx.CURSOR_BULLSEYE`.
        '''
        return wx_tools.cursors.CursorChanger(self, cursor)
    
    def set_good_background_color(self):
        '''Set a good background color to the window.'''
        self.SetBackgroundColour(wx_tools.colors.get_background_color())
        

    def has_focus(self):
        return wx.Window.FindFocus() == self
    
    
    def bind_event_handers(self, cls): #blocktodo: move to base class?
        if not isinstance(self, cls):
            raise Exception('blocktododoc')
        event_handler_grokkers = \
            cls._BindSavvyWindowType__event_handler_grokkers
        for event_handler_grokker in event_handler_grokkers:
            event_handler_grokker.bind(self)
        
        