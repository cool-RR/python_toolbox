# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
This module defines the Frame class.

See its documentation for more information.
'''

from __future__ import with_statement

import os
import sys
import random
import cPickle

import wx
from garlicsim_wx.general_misc.third_party import aui
import pkg_resources


from garlicsim.general_misc import dict_tools
from garlicsim.general_misc import string_tools
import garlicsim_wx.general_misc.thread_timer as thread_timer
import garlicsim
import garlicsim_wx.gui_project
import garlicsim_wx.widgets
from garlicsim_wx.widgets.workspace_widgets_warehouse import workspace_widgets

from . import images as __images_package
images_package = __images_package.__name__


class Frame(wx.Frame):
    '''
    The main window of garlicsim_wx.
    
    This window allows the user to create and manipulate gui projects.
    '''
    def __init__(self, *args, **keywords):
        
        wx.Frame.__init__(self, *args, **keywords)
        self.SetDoubleBuffered(True)
        
        self.Bind(wx.EVT_CLOSE, self.exit)
        
        """
        
        self.workspace_widgets = dict.fromkeys(workspace_widgets)
        
        list_of_default_widgets = [
            'StateReprViewer',
            'Shell',
            'SeekBar',
            'TreeBrowser'
        ]
        # todo: should be somewhere else        
        
        self.default_workspace_widgets = dict_tools.get_list(
            workspace_widgets,
            list_of_default_widgets
        )
        
        """
        
        self.tree_browser = None
        self.seek_bar = None
        self.shell = None
        self.state_repr_viewer = None
        
        
        self.aui_manager = aui.AuiManager()
        self.aui_manager.SetManagedWindow(self)
        
        
        self.aui_manager._art.SetMetric(aui.AUI_DOCKART_SASH_SIZE, 2)
        
        self.aui_manager._art.SetMetric(aui.AUI_DOCKART_CAPTION_SIZE, 10)
        self.aui_manager._art.SetFont(
            aui.AUI_DOCKART_CAPTION_FONT,
            wx.Font(7, wx.FONTFAMILY_MAX, wx.NORMAL, wx.NORMAL, False)
        )
        
        self.aui_manager._art.SetMetric(aui.AUI_DOCKART_GRADIENT_TYPE,
                                        aui.AUI_GRADIENT_NONE)
        self.aui_manager._art.SetColor(aui.AUI_DOCKART_INACTIVE_CAPTION_COLOUR,
                                        wx.Color(200, 200, 200))
        
        self.gui_project = None

        ######################################
        
        filemenu = wx.Menu()
        new_menu_button = filemenu.Append(-1 ,"&New", " New")
        """
        open_menu_button = filemenu.Append(-1 ,"&Open", " Open")
        save_menu_button = filemenu.Append(-1 ,"&Save", " Save")
        """
        exit_menu_button = filemenu.Append(-1 ,"E&xit", " Close the program")
        self.Bind(wx.EVT_MENU, self.on_new, new_menu_button)
        """
        self.Bind(wx.EVT_MENU, self.on_open, open_menu_button)        
        self.Bind(wx.EVT_MENU, self.on_save, save_menu_button)
        """
        self.Bind(wx.EVT_MENU, self.exit, exit_menu_button)        
        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")
        #menubar.Append(stuffmenu,"&Stuff")
        #menubar.Append(nodemenu,"&Node")
        self.SetMenuBar(menubar)
        self.CreateStatusBar()
        """
        ######################################
        
        toolbar = self.CreateToolBar()
        image_file_name = {
            'new': 'new.png',
            'done': 'check.png',
        }
        images = {}
        for key in image_file_name:
            file_name = pkg_resources.resource_filename(images_package,
                                                        image_file_name[key])
            images[key] = wx.Bitmap(file_name, wx.BITMAP_TYPE_ANY)
            
        new_tool = toolbar.AddSimpleTool(
            -1,
            images['new'],
            "New",
            " Create a new file"
        )
        toolbar.AddSeparator()
        done_tool = toolbar.AddSimpleTool(
            -1,
            images['done'],
            "Done editing",
            " Done editing"
        )
        toolbar.Realize()

        self.Bind(wx.EVT_TOOL, self.on_new, new_tool)
        self.Bind(wx.EVT_TOOL, self.done_editing, done_tool)
        """
        ######################################
        
        self.background_timer = thread_timer.ThreadTimer(self)
        self.background_timer.start(150)
        self.Bind(thread_timer.EVT_THREAD_TIMER, self.sync_crunchers,
                  self.background_timer)

        ######################################
        
        
        
        self.aui_manager.Update()
        
        self.Show()
        
        self.Maximize()

    """
    def on_open(self, event=None):
        '''Raise a dialog for opening a gui project from file.'''
        wcd = 'Text files (*.txt)|*.txt|All files (*)|*|'
        cur_dir = os.getcwd()
        tickled_gui_project = None
        try:
            open_dlg = wx.FileDialog(self, message='Choose a file',
                                     defaultDir=cur_dir, defaultFile='',
                                     wildcard=wcd, style=wx.OPEN | wx.CHANGE_DIR)
            if open_dlg.ShowModal() == wx.ID_OK:
                path = open_dlg.GetPath()
                
                try:
                    with file(path, 'r') as my_file:
                        tickled_gui_project = cPickle.load(my_file)
                        
                except IOError, error:
                    dlg = wx.MessageDialog(self,
                                           'Error opening file\n' + str(error))
                    dlg.ShowModal()
                        
                except UnicodeDecodeError, error:
                    dlg = wx.MessageDialog(self,
                                           'Error opening file\n' + str(error))
                    dlg.ShowModal()
                    
                
                    open_dlg.Destroy()
        finally:
            fuck_the_path()
            
        if tickled_gui_project:
            my_gui_project = garlicsim_wx.gui_project.load_tickled_gui_project\
                (tickled_gui_project, self.notebook)
        self.add_gui_project(my_gui_project)
    
    def on_save(self, event=None):
        '''Raise a dialog for saving a gui project to file.'''
        
        my_gui_project = self.gui_projects[0] # Change this to get the active
        tickled = my_gui_project.tickle()
        
        
        wcd='Text files (*.txt)|*.txt|All files (*)|*|'
        cur_dir = os.getcwd()
        try:
            save_dlg = wx.FileDialog(self, message='Save file as...',
                                     defaultDir=cur_dir, defaultFile='',
                                     wildcard=wcd,
                                     style=wx.SAVE | wx.OVERWRITE_PROMPT)
            if save_dlg.ShowModal() == wx.ID_OK:
                path = save_dlg.GetPath()
    
                try:
                    with file(path, 'w') as my_file:
                        cPickle.dump(tickled, my_file)
    
                except IOError, error:
                    dlg = wx.MessageDialog(self,
                                           'Error saving file\n' + str(error))
                    dlg.ShowModal()
            
        finally:
            fuck_the_path()
            
        save_dlg.Destroy()
    
    
    def delete_gui_project(self,gui_project):
        I did this wrong.
        self.gui_projects.remove(gui_project)
        self.notebook.AddPage(gui_project.main_window,"zort!")
        self.notebook.DeletePage(0)
        del gui_project
    """

    def exit(self, e=None):
        '''Close the application window.'''
        print('Frame.exit called.')
        if self.gui_project:
            self.gui_project.stop_playing()
        self.aui_manager.UnInit()
        self.Destroy()        
        e.Skip()        
        self.background_timer.stop()
        self.Close()

    def done_editing(self, e=None):
        '''Finalize editing of the active node in the active gui project.'''
        assert self.gui_project
        return self.gui_project.done_editing()

    def on_new(self, e):
        '''Create a new gui project.'''        
        if self.gui_project is not None:
            raise NotImplementedError
        
        dialog = garlicsim_wx.widgets.misc.SimpackSelectionDialog(self, -1)
        
        if dialog.ShowModal() == wx.ID_OK:
            simpack = dialog.get_simpack_selection()
        else:
            dialog.Destroy()
            return
        dialog.Destroy()

        self.gui_project = garlicsim_wx.gui_project.GuiProject(simpack, self)

        # todo: should create StateReprViewer only if the simpack got no
        # workspace widgets
        
        self.tree_browser = workspace_widgets['TreeBrowser'](self)
        self.tree_browser.aui_pane_info\
            .Bottom().Row(0)\
            .BestSize(1000, 100).MinSize(200, 50).MaxSize(10000, 250)\
            .Floatable(False)
        
        self.playback_controls = workspace_widgets['PlaybackControls'](self)
        self.playback_controls.aui_pane_info\
            .Bottom()\
            .BestSize(184, 128).MinSize(184, 128).MaxSize(184, 128)\
            .Resizable(False)        
        
        self.seek_bar = workspace_widgets['SeekBar'](self)
        self.seek_bar.aui_pane_info\
            .Bottom().Row(1)\
            .BestSize(600, 40).MinSize(200, 40).MaxSize(10000, 100)\
            .Floatable(False)
        
        self.shell = workspace_widgets['Shell'](self)
        self.shell.aui_pane_info\
            .Right().Row(0)\
            .BestSize(400, 600)\
            .MaximizeButton(True)

        
        """
        self.state_repr_viewer = workspace_widgets['StateReprViewer'](self)
        self.state_repr_viewer.aui_pane_info\
            .BestSize(300, 300)\
            .MaximizeButton(True)\
            .NotebookControl(notebook_id)\
            .Center()\
            .Floatable(False)
        """
        
        settings_wx = self.gui_project.simpack_wx_grokker.settings
        
        big_widget_classes = \
            settings_wx.BIG_WORKSPACE_WIDGETS + \
            [workspace_widgets['StateReprViewer']]
        
        self.big_widgets = []
        # todo: not the right way, should be easy listing of all widget
        

        #notebook_id = wx.NewId() # todo: apporopriate?

        self.aui_manager.AddPane(
            None,
            aui.AuiPaneInfo()\
            .BestSize(300, 300)\
            .MaximizeButton(True)\
            #.NotebookControl(notebook_id)\
            .Center()\
            .Floatable(False)
        )
        
        for i, BigWidget in enumerate(big_widget_classes):
            big_widget = BigWidget(self)
            big_widget.aui_pane_info\
                .BestSize(300, 300)\
                .MaximizeButton(True)\
                .Center()\
                .Floatable(False)
            #.NotebookPage(notebook_id, i)\
            self.big_widgets.append(big_widget)
            
        self.aui_manager.Update()
        
        """
        for Widget in self.default_workspace_widgets:
            w = self.workspace_widgets[Widget.__name__] = Widget(self)
        
        self.__organize_workspace_widgets()
        
    def __organize_workspace_widgets(self):
        
        self.aui_manager.GetPane(self.workspace_widgets['TreeBrowser'])\
            .Bottom().BestSize(0, 100).Row(0)
        self.aui_manager.GetPane(self.workspace_widgets['SeekBar'])\
            .Bottom().BestSize(0, 50).Row(1)
        self.aui_manager.GetPane(self.workspace_widgets['Shell'])\
            .Right().BestSize(500, 0).Row(0)
        
        
        self.aui_manager.Update()
        self.Refresh()
        """

    def sync_crunchers(self, e=None):
        '''
        Take work from the crunchers, and give them new instructions if needed.
                
        (This is a wrapper that calls the sync_crunchers method of all the
        gui projects.)
        
        Talks with all the crunchers, takes work from them for implementing
        into the tree, retiring crunchers or recruiting new crunchers as
        necessary.
        
        Returns the total amount of nodes that were added to each gui project's
        tree.
        '''
        nodes_added = self.gui_project.sync_crunchers() \
                    if self.gui_project else 0
        
        if nodes_added > 0:
            pass#self.Refresh()
        
        return nodes_added
    

