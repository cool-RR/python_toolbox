# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines the `WindowMenu` class.

See its documentation for more info.
'''

import wx

from garlicsim_wx.general_misc.cute_menu import CuteMenu
from garlicsim_wx.general_misc import wx_tools

from garlicsim_wx.widgets.workspace_widget import \
     EVT_WORKSPACE_WIDGET_MENU_SELECT
from .workspace_menu import WorkspaceMenu


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
            ' Manipulate the workspace, i.e. the arrangement of widgets on '
            'the screen'
        )
        self.workspace_menu_button.Enable(False)
        
        
        self.AppendSeparator()
        
        
        self.crunching_controls_button = self.Append(
            -1,
            '&Crunching',
            ' Go to the crunching tool, which lets you control how your '
            'simulation is crunched'
        )       
        
        frame.Bind(
            wx.EVT_MENU,
            lambda event: wx_tools.event_tools.post_event(
                frame.crunching_controls,
                EVT_WORKSPACE_WIDGET_MENU_SELECT
            ),
            source=self.crunching_controls_button
        )
        
        
        self.local_nodes_examiner_button = self.Append(
            -1,
            '&Local Nodes Examiner',
            ' Go to the local nodes examiner, which lets you manipulate '
            'tree nodes one-by-one'
        )       
        self.local_nodes_examiner_button.Enable(False)
        
        #frame.Bind(
            #wx.EVT_MENU,
            #lambda event: wx_tools.event_tools.post_event(
                #frame.local_nodes_examiner,
                #EVT_WORKSPACE_WIDGET_MENU_SELECT
            #),
            #source=self.local_nodes_examiner_button
        #)
        
        
        self.playback_controls_button = self.Append(
            -1,
            '&Playback',
            ' Go to the playback controls, which let you control the onscreen '
            'playback of the simulation'
        )       
        
        frame.Bind(
            wx.EVT_MENU,
            lambda event: wx_tools.event_tools.post_event(
                frame.playback_controls,
                EVT_WORKSPACE_WIDGET_MENU_SELECT
            ),
            source=self.playback_controls_button
        )
        
        
        self.seek_bar_button = self.Append(
            -1,
            'Seek &Bar',
            ' Go to the seek-bar, which lets you navigate the active timeline'
        )       
        
        frame.Bind(
            wx.EVT_MENU,
            lambda event: wx_tools.event_tools.post_event(
                frame.seek_bar,
                EVT_WORKSPACE_WIDGET_MENU_SELECT
            ),
            source=self.seek_bar_button
        )
        
        
        self.shell_button = self.Append(
            -1,
            '&Shell',
            ' Go to the shell, which lets you analyze your simulation using '
            'arbitrary Python code'
        )               
        
        frame.Bind(
            wx.EVT_MENU,
            lambda event: wx_tools.event_tools.post_event(
                frame.shell,
                EVT_WORKSPACE_WIDGET_MENU_SELECT
            ),
            source=self.shell_button
        )
        
        
        self.toolbox_button = self.Append(
            -1,
            'Toolbo&x',
            ' Go to the toolbox, in which you can choose between '
            'different tools to use in the other widgets'
        )       
        self.toolbox_button.Enable(False)
        
        #frame.Bind(
            #wx.EVT_MENU,
            #lambda event: wx_tools.event_tools.post_event(
                #frame.toolbox,
                #EVT_WORKSPACE_WIDGET_MENU_SELECT
            #),
            #source=self.toolbox_button
        #)
        
        
        self.tree_browser_button = self.Append(
            -1,
            '&Tree Browser',
            ' Go to the tree browser, which lets you navigate the time tree'
        )       
        
        frame.Bind(
            wx.EVT_MENU,
            lambda event: wx_tools.event_tools.post_event(
                frame.tree_browser,
                EVT_WORKSPACE_WIDGET_MENU_SELECT
            ),
            source=self.tree_browser_button
        )
        
        
        self.workspace_widgets_buttons = [
            self.crunching_controls_button,
            #self.local_nodes_examiner_button,
            self.playback_controls_button,
            self.seek_bar_button,
            self.shell_button,
            #self.toolbox_button
            self.tree_browser_button
        ]
        
    def _recalculate(self):
        gui_project = self.frame.gui_project
        for workspace_widget_button in self.workspace_widgets_buttons:
            workspace_widget_button.Enable(gui_project is not None)
        