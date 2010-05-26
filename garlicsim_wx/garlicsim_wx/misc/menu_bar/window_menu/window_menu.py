# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the WindowMenu class.

See its documentation for more info.
'''

import wx

from garlicsim_wx.general_misc.cute_menu import CuteMenu

from workspace_menu import WorkspaceMenu


class WindowMenu(CuteMenu):
    '''Menu for controlling workspace widgets.'''
    def __init__(self, frame):
        super(WindowMenu, self).__init__()
        self.frame = frame
        self._build()
    
    def _build(self):
        
        frame = self.frame


        self.workspace_menu = WorkspaceMenu(frame)
        self.workspace_menu_button = self.AppendMenu(
            -1,
            '&Workspace',
            self.workspace_menu,
            ''' Manipulate the workspace, i.e. the arrangement of widgets \
on the screen'''
        )
        self.workspace_menu_button.Enable(False)
        
        
        self.AppendSeparator()
        
        
        self.crunching_button = self.Append(
            -1,
            '&Crunching',
            ''' Show/hide the crunching tool, which lets you control how your \
simulation is crunched''',
             wx.ITEM_CHECK
        )       
        self.crunching_button.Enable(False)
        
        
        self.local_nodes_examiner_button = self.Append(
            -1,
            '&Local nodes examiner',
            ''' Show/hide the local nodes examiner, which lets you manipulate \
tree nodes one-by-one''',
            wx.ITEM_CHECK
        )       
        self.local_nodes_examiner_button.Enable(False)
        
        
        self.playback_controls_button = self.Append(
            -1,
            '&Playback Controls',
            ''' Show/hide the playback controls, which let you control the \
onscreen playback of the simulation''',
            wx.ITEM_CHECK
        )       
        self.playback_controls_button.Enable(False)
        
        
        self.seek_bar_button = self.Append(
            -1,
            'Seek-&bar',
            ''' Show/hide the seek-bar, which lets you navigate the active \
timeline''',
            wx.ITEM_CHECK
        )       
        self.seek_bar_button.Enable(False)
        
        
        self.shell_button = self.Append(
            -1,
            '&Shell',
            ''' Show/hide the shell, which lets you analyze your simulation \
using arbitrary Python code''',
            wx.ITEM_CHECK
        )       
        self.shell_button.Enable(False)
        
        
        self.toolbox_button = self.Append(
            -1,
            'Toolbo&x',
            ''' Show/hide the toolbox, in which you can choose between \
different tools to use in the other widgets''',
            wx.ITEM_CHECK
        )       
        self.toolbox_button.Enable(False)
        
        
        self.tree_browser_button = self.Append(
            -1,
            '&Tree browser',
            ''' Show/hide the tree browser, which lets you navigate the time \
tree''',
            wx.ITEM_CHECK
        )       
        self.tree_browser_button.Enable(False)
        