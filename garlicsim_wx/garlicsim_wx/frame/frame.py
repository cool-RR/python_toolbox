# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the Frame class.

See its documentation for more information.
'''

from __future__ import with_statement

import os
import sys
import random
import pickle as pickle_module
import multiprocessing #tododoc: am i forcing multiprocessing here?

import wx
from garlicsim_wx.general_misc.third_party import aui
import pkg_resources

from garlicsim.general_misc import dict_tools
from garlicsim.general_misc import string_tools
import garlicsim_wx.general_misc.thread_timer as thread_timer

import garlicsim
import garlicsim_wx.gui_project
import garlicsim_wx.widgets
import garlicsim_wx.misc
from garlicsim_wx.widgets import workspace_widgets

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
        
        self.Bind(wx.EVT_CLOSE, self.on_close)
                
        self.tree_browser = None
        self.seek_bar = None
        self.shell = None
        self.state_repr_viewer = None
        
        self.aui_manager = garlicsim_wx.misc.aui.AuiManager(self)
                
        self.gui_project = None

        ######################################
        
        filemenu = wx.Menu()
        new_menu_button = filemenu.Append(-1 ,"&New", " New")
        #open_menu_button = filemenu.Append(-1 ,"&Open", " Open")
        save_menu_button = filemenu.Append(-1 ,"&Save", " Save")
        exit_menu_button = filemenu.Append(-1 ,"E&xit", " Close the program")
        self.Bind(wx.EVT_MENU, self.on_new, new_menu_button)
        #self.Bind(wx.EVT_MENU, self.on_open, open_menu_button)        
        self.Bind(wx.EVT_MENU, self.on_save, save_menu_button)
        self.Bind(wx.EVT_MENU, self.on_exit_menu_button, exit_menu_button)
        menubar = wx.MenuBar()
        menubar.Append(filemenu, "&File")
        #menubar.Append(stuffmenu,"&Stuff")
        #menubar.Append(nodemenu,"&Node")
        self.SetMenuBar(menubar)
        self.CreateStatusBar()
        
        ######################################
        
        self.background_timer = thread_timer.ThreadTimer(self)
        self.background_timer.start(150)
        self.Bind(
            thread_timer.EVT_THREAD_TIMER,
            lambda event: self.sync_crunchers(),
            self.background_timer
        )
        
        ######################################
        
        
        
        self.aui_manager.Update()
        
        self.Show()
        
        self.Maximize()

    

    def on_close(self, event):
        '''Close the application window.'''
        if self.gui_project:
            self.gui_project.stop_playing()
        self.aui_manager.UnInit()
        self.Destroy()        
        event.Skip()        
        self.background_timer.stop()

    def finalize_active_node(self, e=None):
        '''Finalize editing of the active node in the active gui project.'''
        assert self.gui_project
        return self.gui_project.finalize_active_node()

    def on_new(self, event=None):
        '''Create a new gui project.'''        
        if self.gui_project is not None:
            new_process = multiprocessing.Process(
                target=garlicsim_wx.start,
                kwargs={'new_gui_project': True}
            )
            new_process.start()
            return
        
        dialog = garlicsim_wx.widgets.misc.SimpackSelectionDialog(self)
        
        if dialog.ShowModal() == wx.ID_OK:
            simpack = dialog.get_simpack_selection()
        else:
            dialog.Destroy()
            return
        dialog.Destroy()

        self.gui_project = garlicsim_wx.gui_project.GuiProject(simpack, self)

        # todo: should create StateReprViewer only if the simpack got no
        # workspace widgets
        
        self.tree_browser = workspace_widgets.TreeBrowser(self)
        self.aui_manager.AddPane(
            self.tree_browser,
            aui.AuiPaneInfo()\
            .Bottom().Row(0)\
            .BestSize(1000, 100).MinSize(200, 50).MaxSize(10000, 250)\
            .Caption(self.tree_browser.get_uppercase_name())
            .Floatable(False)\
            .CloseButton(False)
        )
        
        self.playback_controls = workspace_widgets.PlaybackControls(self)
        self.aui_manager.AddPane(
            self.playback_controls,
            aui.AuiPaneInfo()\
            .Bottom()\
            .BestSize(184, 128).MinSize(184, 128).MaxSize(184, 128)\
            .Caption(self.playback_controls.get_uppercase_name())
            .Resizable(False)\
            .CloseButton(False)        
        )
        
        self.seek_bar = workspace_widgets.SeekBar(self)
        self.aui_manager.AddPane(
            self.seek_bar,
            aui.AuiPaneInfo()\
            .Bottom().Row(1)\
            .BestSize(600, 40).MinSize(200, 40).MaxSize(10000, 100)\
            .Caption(self.seek_bar.get_uppercase_name())
            .Floatable(False)\
            .CloseButton(False)
        )
        
        self.shell = workspace_widgets.Shell(self)
        self.aui_manager.AddPane(
            self.shell,
            aui.AuiPaneInfo()\
            .Right().Row(0)\
            .BestSize(400, 600)\
            .Caption(self.shell.get_uppercase_name())
            .MaximizeButton(True)\
            .CloseButton(False)
        )
        
        """
        self.state_repr_viewer = workspace_widgets.StateReprViewer(self)
        self.aui_manager.AddPane(
            self.state_repr_viewer,
            aui.AuiPaneInfo()\
            .BestSize(300, 300)\
            .MaximizeButton(True)\
            .Center()\
            .Caption(self.state_repr_viewer.get_uppercase_name())
            .Floatable(False)\
            .CloseButton(False)
        )
        """
        settings_wx = self.gui_project.simpack_wx_grokker.settings
        

        big_widget_class = settings_wx.BIG_WORKSPACE_WIDGETS[0] if \
                         settings_wx.BIG_WORKSPACE_WIDGETS else \
                         workspace_widgets.StateReprViewer

        self.big_widget = big_widget_class(self)
        self.aui_manager.AddPane(
            self.big_widget,
            aui.AuiPaneInfo()\
            .BestSize(300, 300)\
            .MaximizeButton(True)\
            .Center()\
            .Caption(self.big_widget.get_uppercase_name())
            .Floatable(False)\
            .CloseButton(False)
        )
        
        if isinstance(self.big_widget, workspace_widgets.StateReprViewer):
            self.state_repr_viewer= self.big_widget
        
        """
        big_widget_classes = \
            settings_wx.BIG_WORKSPACE_WIDGETS #+ \
        #    [workspace_widgets['StateReprViewer']]
        
        self.big_widgets = []
        # todo: not the right way, should be easy listing of all widget
        
        
        for i, BigWidget in enumerate(big_widget_classes):
            big_widget = BigWidget(self)
            self.aui_manager.AddPane(
                big_widget,
                aui.AuiPaneInfo()\
                .BestSize(300, 300)\
                .MaximizeButton(True)\
                .Center()\
                .Caption(big_widget.get_uppercase_name())\
                .Floatable(False)\
                .CloseButton(False),
                target=self.state_repr_viewer.get_aui_pane_info()
            )
            #.NotebookPage(notebook_id, i)\
            self.big_widgets.append(big_widget)

        """
        
        self.aui_manager.Update()
        

    def on_exit_menu_button(self, event):
        '''Exit menu button handler.'''
        self._post_close_event()

        
    def _post_close_event(self):
        '''Post a close event to the frame.'''
        event = wx.PyEvent(self.Id)
        event.SetEventType(wx.wxEVT_CLOSE_WINDOW)
        wx.PostEvent(self, event)
        
        
    def sync_crunchers(self):
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
                        tickled_gui_project = pickle_module.load(my_file)
                        
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
    """
    def on_save(self, event=None):
        '''Raise a dialog for saving a gui project to file.'''
        
        wcd='GarlicSim simulation pickle (*.gssp)|*.gssp|All files (*)|*|'
        cur_dir = os.getcwd()
        try:
            save_dialog = wx.FileDialog(self, message='Save file as...',
                                     defaultDir=cur_dir, defaultFile='',
                                     wildcard=wcd,
                                     style=wx.SAVE | wx.OVERWRITE_PROMPT)
            if save_dialog.ShowModal() == wx.ID_OK:
                path = save_dialog.GetPath()
    
                try:
                    with file(path, 'w') as my_file:
                        pickle_module.dump(self.gui_project, my_file)
    
                except IOError, error:
                    error_dialog = wx.MessageDialog(
                        self,
                        'Error saving file\n' + str(error)
                    )
                    error_dialog.ShowModal()
            
        finally:
            # fuck_the_path()
            pass
            
        save_dialog.Destroy()
    
    """    
    def delete_gui_project(self,gui_project):
        I did this wrong.
        self.gui_projects.remove(gui_project)
        self.notebook.AddPage(gui_project.main_window,"zort!")
        self.notebook.DeletePage(0)
        del gui_project
    """
