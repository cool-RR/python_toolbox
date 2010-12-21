# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines `WorkspaceWidget` class and `EVT_WORKSPACE_WIDGET_MENU_SELECT` event.

See their documentation for more info.
'''

import wx

import garlicsim_wx
from garlicsim_wx.general_misc import wx_tools
from garlicsim_wx.general_misc.third_party import aui
from garlicsim.general_misc.third_party import abc
from garlicsim.general_misc import string_tools


wxEVT_WORKSPACE_WIDGET_MENU_SELECT = wx.NewEventType()
EVT_WORKSPACE_WIDGET_MENU_SELECT = wx.PyEventBinder(
    wxEVT_WORKSPACE_WIDGET_MENU_SELECT,
    1
)
'''Event for when a workspace widget gets activated from the menu.'''


class WorkspaceWidget(object):
    '''
    Abstract base class for workspace widgets.
    
    A workspace widget is a widget displayed on the `Frame` of `garlicsim_wx`,
    and is connected to a specific gui project.
    '''

    # todo: How do I make it so all subclasses must inherit from `Window`?
    
    __metaclass__ = abc.ABCMeta
    

    _WorkspaceWidget__name = None
    '''The display name of the widget. Default is class name.'''

    
    def __init__(self, frame):
        
        
        self.Hide()
        
        self.frame = frame
        assert isinstance(self.frame, garlicsim_wx.Frame)
        
        self.gui_project = frame.gui_project
        assert isinstance(self.gui_project, garlicsim_wx.GuiProject)
        
        self.aui_manager = frame.aui_manager
        assert isinstance(self.aui_manager, aui.AuiManager)
        
        
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        self.__escape_key = wx_tools.Key(wx.WXK_ESCAPE)
        
        self.Bind(EVT_WORKSPACE_WIDGET_MENU_SELECT,
                  self.on_workspace_widget_menu_select)
        
        
    @classmethod
    def get_uppercase_name(cls):
        '''Get the name of the widget's class in uppercase. Used for title.'''
        name = cls._WorkspaceWidget__name or cls.__name__
        return string_tools.camelcase_to_spacecase(name).upper()

    
    def get_aui_pane_info(self):
        '''Get the AuiPaneInfo of this widget in the aui manager.'''
        return self.aui_manager.GetPane(self)
        
    
    def on_key_down(self, event):
        '''Handler for key down event.'''
        
        if wx_tools.Key.get_from_key_event(event) == self.__escape_key and \
           self.frame.FindFocus() is not self.frame:
                
                self.frame.SetFocus()
                
        else:
            event.Skip()


    def show(self):
        '''Show the workspace widget, making sure `aui` doesn't hide it.'''
        aui_pane_info = self.get_aui_pane_info()
        if aui_pane_info.IsShown() is False:
            aui_pane_info.Show()
            self.aui_manager.Update()
        if isinstance(self.Parent, aui.AuiNotebook):
            self.Parent.SetSelectionToWindow(self)
        self.SetFocus()
            
            
    def on_workspace_widget_menu_select(self, event):
        '''Handle the event of a workspace widget being selected in menu.'''
        self.show()
    