# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `MenuBar` class.

See its documentation for more info.
'''

import wx

from garlicsim_wx.general_misc import wx_tools

from .file_menu import FileMenu
from .edit_menu import EditMenu
from .create_menu import CreateMenu
from .node_menu import NodeMenu
from .block_menu import BlockMenu
from .window_menu import WindowMenu
from .help_menu import HelpMenu


class MenuBar(wx.MenuBar):
    '''The main GarlicSim menu bar.'''
    
    def __init__(self, frame):
        super(MenuBar, self).__init__()
        self.frame = frame
        
        self.file_menu = FileMenu(frame)
        self.Append(self.file_menu, '&File')
        
        self.edit_menu = EditMenu(frame)
        self.Append(self.edit_menu, '&Edit')
        # This disables a menu from the bar:
        # self.EnableTop(self.FindMenu('Edit'), False)
        # Logically it makes sense, but it makes it hard to see all the options
        # in the menu, so at least for now I'm not doing it.
        
        self.create_menu = CreateMenu(frame)
        self.Append(self.create_menu, '&Create')
        
        self.node_menu = NodeMenu(frame)
        self.Append(self.node_menu, '&Node')
        
        self.block_menu = BlockMenu(frame)
        self.Append(self.block_menu, '&Block')
        
        self.window_menu = WindowMenu(frame)
        title_of_window_menu = '&Workspace' if wx_tools.is_mac else '&Window'
        self.Append(self.window_menu, title_of_window_menu)
        
        self.help_menu = HelpMenu(frame)
        title_of_help_menu = 'GarlicSim &Help' if wx_tools.is_mac else '&Help'
        self.Append(self.help_menu, title_of_help_menu)