# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the NodeMenu class.

See its documentation for more info.
'''

import wx

from garlicsim_wx.general_misc.cute_menu import CuteMenu


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
            'Fork by &editing',
            ''' Fork the simulation by making a copy of the active node and \
editing it'''
        )
        
        frame.Bind(
            wx.EVT_MENU,
            lambda event: frame.gui_project.fork_by_editing(),
            self.fork_by_editing_button
        )

        
        self.fork_by_crunching_button = self.Append(
            -1,
            'Fork by &crunching',
            ' Fork the simulation by crunching from the active node'
        )
        frame.Bind(
            wx.EVT_MENU,
            lambda event: frame.gui_project.fork_by_crunching(),
            self.fork_by_crunching_button
        )

        
        self.AppendSeparator()
        
        
        self.properties_button = self.Append(
            -1,
            'Node &properties...',
            " See the active node's properties"
        )
        self.properties_button.Enable(False)        
        
        
        self.AppendSeparator()
        
        
        self.delete_button = self.Append(
            -1,
            '&Delete active node...',
            ' Delete the active node'
        )
        self.delete_button.Enable(False)
                
