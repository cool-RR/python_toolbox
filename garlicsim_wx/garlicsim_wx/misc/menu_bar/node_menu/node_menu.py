# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `NodeMenu` class.

See its documentation for more info.
'''

import wx

from garlicsim_wx.general_misc.cute_menu import CuteMenu

from .fork_by_crunching_using_menu import ForkByCrunchingUsingMenu


class NodeMenu(CuteMenu):
    '''Menu for manipulating the active node.'''
    def __init__(self, frame):
        super(NodeMenu, self).__init__()
        self.frame = frame
        self._build()
    
    def _build(self):
        
        frame = self.frame
       
        self.fork_by_editing_button = self.Append(
            -1,
            'Fork by &Editing',
            " Fork the simulation by making a copy of the active node and "
            "editing it"
        )
        
        frame.Bind(
            wx.EVT_MENU,
            lambda event: frame.gui_project.fork_by_editing(),
            self.fork_by_editing_button
        )

        
        self.fork_by_crunching_button = self.Append(
            -1,
            'Fork by &Crunching',
            ' Fork the simulation by crunching from the active node'
        )
        frame.Bind(
            wx.EVT_MENU,
            lambda event: frame.gui_project.fork_by_crunching(),
            self.fork_by_crunching_button
        )

        self.fork_by_crunching_using_menu = ForkByCrunchingUsingMenu(frame)
        self.fork_by_crunching_using_menu_button = self.AppendMenu(
            -1,
            'Fork by Crunching &Using',
            self.fork_by_crunching_using_menu,
            ' Fork by crunching from the active node using specified step '
            'profile'
        )

        
        self.AppendSeparator()
        
        
        self.properties_button = self.Append(
            -1,
            'Node &Properties',
            " See the active node's properties"
        )
        self.properties_button.Enable(False)        
        
        
        self.AppendSeparator()
        
        
        self.delete_button = self.Append(
            -1,
            '&Delete Active Node...',
            ' Delete the active node'
        )
        self.delete_button.Enable(False)
                
        
    def _recalculate(self):
        self.enable_in_menu_bar(
            self.frame.gui_project is not None and \
            self.frame.gui_project.active_node is not None
        )