# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the WorkspaceMenu class.

See its documentation for more info.
'''

import wx

from garlicsim_wx.general_misc.cute_menu import CuteMenu

class WorkspaceMenu(CuteMenu):
    '''Menu for manipulating the workspace.'''
    def __init__(self, frame):
        super(WorkspaceMenu, self).__init__()
        self.frame = frame
        self._build()
        
        
    def _build(self):

        frame = self.frame
        
        self.save_workspace_button = self.Append(
            -1,
            '&Save workspace...',
            ''' Save the current workspace configuration, so that it may be \
recalled in the future'''
        )
        self.save_workspace_button.Enable(False)
        
        
        self.delete_workspace_button = self.Append(
            -1,
            '&Delete workspace...',
            ' Delete one of the saved workspace configurations'
        )
        self.delete_workspace_button.Enable(False)
        
        
        self.AppendSeparator()
        
                
        self.delete_workspace_button = self.Append(
            -1,
            'De&fault workspace',
            ' Use the factory-default workspace configuration'
        )
        self.delete_workspace_button.Enable(False)
                
