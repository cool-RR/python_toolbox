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
import cPickle as pickle_module
import subprocess
import webbrowser

import wx
from garlicsim_wx.general_misc.third_party import aui
import pkg_resources

from garlicsim.general_misc import dict_tools
from garlicsim.general_misc import string_tools
import garlicsim_wx.general_misc.thread_timer as thread_timer

import garlicsim
from garlicsim_wx.gui_project import GuiProject
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
        self.SetIcons(garlicsim_wx.misc.icon_bundle.get_icon_bundle())
        
        self.Bind(wx.EVT_CLOSE, self.on_close)
                
        self.tree_browser = None
        self.seek_bar = None
        self.shell = None
        self.state_repr_viewer = None
        
        self.aui_manager = garlicsim_wx.misc.aui.AuiManager(self)
                
        self.gui_project = None
        
        # tododoc properties here
        
        self.CreateStatusBar()
        
        self.__init_menu_bar()        
        
        self.background_timer = thread_timer.ThreadTimer(self)
        
        self.background_timer.start(150)
        
        self.Bind(
            thread_timer.EVT_THREAD_TIMER,
            lambda event: self.sync_crunchers(),
            self.background_timer
        )
        
        self.aui_manager.Update()
        
        self.Show()
        
        self.Maximize()

        
    def __init_menu_bar(self):
                
        
        menu_bar = self.menu_bar = wx.MenuBar()
        
        self.SetMenuBar(menu_bar)        
        

        file_menu = menu_bar.file_menu = wx.Menu()
        
        menu_bar.Append(file_menu, '&File')
        
        
        file_menu.new_button = \
            file_menu.Append(-1 ,'&New...\tCtrl+N', ' Create a new simulation')
        
        self.Bind(wx.EVT_MENU, self.on_new, file_menu.new_button)
        
        
        file_menu.open_button = \
            file_menu.Append(-1 ,'&Open...\tCtrl+O', ' Open a saved simulation')
        
        self.Bind(wx.EVT_MENU, self.on_open, file_menu.open_button)        
        
        
        # todo: put open recent here

        
        file_menu.AppendSeparator()

        
        file_menu.close_button = file_menu.Append(
            -1 ,'&Close\tCtrl+W', ' Close the currently open simulation')
        
        file_menu.close_button.Enable(False)

        
        file_menu.save_button = file_menu.Append(
            -1 ,'&Save\tCtrl+S', ' Save the currently open simulation')
        
        self.Bind(wx.EVT_MENU, self.on_save, file_menu.save_button)
        
        
        file_menu.save_as_button = file_menu.Append(
            -1, 'Save &as...\tShift+Ctrl+S',
            ' Save the currently open simulation under a different name'
        )
        
        file_menu.save_as_button.Enable(False)
                
        
        file_menu.AppendSeparator()

        
        export_menu = file_menu.export_menu = wx.Menu()

        file_menu.export_menu_button = file_menu.AppendMenu(
            -1, '&Export', export_menu,
            ' Export simulation data'
        )
        
        # file_menu.export_menu_button.Enable(False) tododoc: uncomment

        
        export_menu.video_button = export_menu.Append(
            -1, '&Video',
            ' Export a video sequence showing playback of the simulation'
        )

        export_menu.video_button.Enable(False)
        
        
        export_menu.image_button = export_menu.Append(
            -1, '&Image',
            ' Export an image showing a single state in the simulation'
        )
        
        export_menu.image_button.Enable(False)
        
                
        file_menu.AppendSeparator()
        
        
        file_menu.print_button = file_menu.Append(
            -1, 'Print...\tCtrl+P',
            ' Print the current state of the simulation'
        )

        file_menu.print_button.Enable(False)
        
        
        file_menu.AppendSeparator()
        

        file_menu.exit_button = \
            file_menu.Append(wx.ID_EXIT ,'E&xit', ' Close GarlicSim')        
                
        self.Bind(wx.EVT_MENU, self.on_exit_menu_button, file_menu.exit_button)

        
        edit_menu = menu_bar.edit_menu = wx.Menu()
        
        menu_bar.Append(edit_menu, '&Edit')
        
        # This disables a menu from the bar:
        # menu_bar.EnableTop(menu_bar.FindMenu('Edit'), False)
        # Logically it makes sense, but it makes it hard to see all the options
        # in the menu, so at least for now I'm not doing it.

        
        edit_menu.undo_button = edit_menu.Append(
            -1, '&Undo\tCtrl+Z',
            ' Undo the last operation'
        )

        edit_menu.undo_button.Enable(False)
        
        
        edit_menu.redo_button = edit_menu.Append(
            -1, '&Redo\tCtrl+Y',
            ' Redo the last operation that was undone'
        )

        edit_menu.redo_button.Enable(False)
        
        
        edit_menu.AppendSeparator()
        
                
        edit_menu.cut_button = edit_menu.Append(
            -1, 'Cu&t\tCtrl+X',
            ''' Cut the current selection, copying to the clipboard and \
deleting it from the simulation'''
        )

        edit_menu.cut_button.Enable(False)
        
                
        edit_menu.copy_button = edit_menu.Append(
            -1, '&Copy\tCtrl+C',
            ' Copy the current selection to the clipboard'
        )

        edit_menu.copy_button.Enable(False)
        
                
        edit_menu.paste_button = edit_menu.Append(
            -1, '&Paste\tCtrl+V',
            ' Paste the content of the clipboard into the simulation'
        )

        edit_menu.paste_button.Enable(False)
        
                
        edit_menu.clear_button = edit_menu.Append(
            -1, 'Cl&ear\tDel',
            ' Delete the current selection'
        )

        edit_menu.clear_button.Enable(False)
        
        
        edit_menu.AppendSeparator()


        edit_menu.select_all_button = edit_menu.Append(
            -1, 'Select &All\tCtrl+A',
            ' Select all the nodes'
        )

        edit_menu.select_all_button.Enable(False)
        
        
        edit_menu.deselect_button = edit_menu.Append(
            -1, '&Deselect\tCtrl+D',
            ' Deselect all the selected nodes'
        )

        edit_menu.deselect_button.Enable(False)
        
        
        edit_menu.invert_selection_button = edit_menu.Append(
            -1, 'Invert selection\tCtrl+Shift+I',
            ''' Select all the nodes that aren't selected, and deselect \
those that are selected'''
        )

        edit_menu.invert_selection_button.Enable(False)
        
        
        edit_menu.AppendSeparator()
        
        
        edit_menu.merge_to_blocks_button = edit_menu.Append(
            -1, 'Merge to blocks where possible',
            ' Merge adjacant nodes to blocks, where possible'
        )

        edit_menu.merge_to_blocks_button.Enable(False)
        
        
        edit_menu.AppendSeparator()
        
        
        edit_menu.preferences_button = edit_menu.Append(
            -1, 'Prefere&nces',
            " View and modify GarlicSim's program-wide preferences"
        )

        edit_menu.preferences_button.Enable(False)
        

        node_menu = menu_bar.node_menu = wx.Menu()
        
        menu_bar.Append(node_menu, '&Node')
        
        menu_bar.EnableTop(menu_bar.FindMenu('Node'), False)
        

        node_menu.fork_by_editing_button = node_menu.Append(
            -1, 'Fork by &editing',
            ' Fork the simulation by making a copy of the active node and editing it'
        )
        
        self.Bind(
            wx.EVT_MENU,
            lambda event: self.gui_project.fork_by_editing(),
            node_menu.fork_by_editing_button
        )

        
        node_menu.fork_by_crunching_button = node_menu.Append(
            -1, 'Fork by &crunching',
            ' Fork the simulation by crunching from the active node'
        )

        self.Bind(
            wx.EVT_MENU,
            lambda event: self.gui_project.fork_by_crunching(),
            node_menu.fork_by_crunching_button
        )

        
        node_menu.AppendSeparator()
        
        
        node_menu.properties_button = node_menu.Append(
            -1, 'Node &properties...',
            " See the active node's properties"
        )

        node_menu.properties_button.Enable(False)        
        
        
        node_menu.AppendSeparator()
        
        
        node_menu.delete_button = node_menu.Append(
            -1, '&Delete active node...',
            " Delete the active node"
        )

        node_menu.delete_button.Enable(False)
        
        
        block_menu = menu_bar.block_menu = wx.Menu()

        menu_bar.Append(block_menu, '&Block')
        
        
        block_menu.split_button = block_menu.Append(
            -1, '&Split active block...',
            " Split the active block into two separate blocks"
        )

        block_menu.split_button.Enable(False)
        
        
        block_menu.scatter_button = block_menu.Append( # todo: rename
            -1, 'S&catter active block...',
            " Scatter the active block, leaving all its nodes blockless"
        )

        block_menu.scatter_button.Enable(False)
        
        
        window_menu = menu_bar.window_menu = wx.Menu()

        menu_bar.Append(window_menu, '&Window')
        
        
        window_menu.workspace_menu = workspace_menu = wx.Menu()
        
        window_menu.workspace_menu_button = window_menu.AppendMenu(
            -1, '&Workspace', window_menu.workspace_menu,
            ' Manipulate the workspace, i.e. the arrangement of widgets on the screen'
        )

        # window_menu.workspace_menu_button.Enable(False) tododoc: uncomment
        
        
        workspace_menu.save_workspace_button = workspace_menu.Append(
            -1, '&Save workspace...',
            ''' Save the current workspace configuration, so that it may be \
recalled in the future'''
        )
        
        workspace_menu.save_workspace_button.Enable(False)
        
        
        workspace_menu.delete_workspace_button = workspace_menu.Append(
            -1, '&Delete workspace...',
            ' Delete one of the saved workspace configurations'
        )
        
        workspace_menu.delete_workspace_button.Enable(False)
        
        
        workspace_menu.AppendSeparator()
        
                
        workspace_menu.delete_workspace_button = workspace_menu.Append(
            -1, '&Default workspace',
            ' Use the factory-default workspace configuration'
        )
        
        workspace_menu.delete_workspace_button.Enable(False)
        
        
        window_menu.AppendSeparator()
        
        
        window_menu.crunching_button = window_menu.Append(
            -1, '&Crunching',
            ''' Show/hide the crunching tool, which lets you control how your \
simulation is crunched''', wx.ITEM_CHECK
        )
                
        window_menu.crunching_button.Enable(False)
        
        
        window_menu.local_nodes_examiner_button = window_menu.Append(
            -1, '&Local nodes examiner',
            ''' Show/hide the local nodes examiner, which lets you manipulate \
tree nodes one-by-one''', wx.ITEM_CHECK
        )
                
        window_menu.local_nodes_examiner_button.Enable(False)
        
        
        window_menu.playback_controls_button = window_menu.Append(
            -1, '&Playback Controls',
            ''' Show/hide the playback controls, which let you control the \
onscreen playback of the simulation''', wx.ITEM_CHECK
        )
                
        window_menu.playback_controls_button.Enable(False)
        
        
        window_menu.seek_bar_button = window_menu.Append(
            -1, 'Seek-&bar',
            ''' Show/hide the seek-bar, which lets you navigate the active \
timeline''', wx.ITEM_CHECK
        )
                
        window_menu.seek_bar_button.Enable(False)
        
        
        window_menu.shell_button = window_menu.Append(
            -1, '&Shell',
            ''' Show/hide the shell, which lets you analyze your simulation \
using arbitrary Python code''', wx.ITEM_CHECK
        )
                
        window_menu.shell_button.Enable(False)
        
        
        window_menu.toolbox_button = window_menu.Append(
            -1, 'Toolbo&x',
            ''' Show/hide the toolbox, in which you can choose between \
different tools to use in the other widgets''', wx.ITEM_CHECK
        )
                
        window_menu.toolbox_button.Enable(False)
        
        
        window_menu.tree_browser_button = window_menu.Append(
            -1, '&Tree browser',
            ''' Show/hide the tree browser, which lets you navigate the time \
tree''', wx.ITEM_CHECK
        )
                
        window_menu.tree_browser_button.Enable(False)
        
                
        help_menu = menu_bar.help_menu = wx.Menu()
        
        menu_bar.Append(help_menu, '&Help')
                
        
        help_menu.garlicsim_help_button = help_menu.Append(
            -1, 'GarlicSim &Help...\tF1',
            ' Display the help documents for GarlicSim'
        )
        
        help_menu.garlicsim_help_button.Enable(False)
        
        
        help_menu.welcome_screen_button = help_menu.Append(
            -1, '&Welcome screen...',
            ' Show the welcome screen'
        )
        
        help_menu.welcome_screen_button.Enable(False)
        
                
        help_menu.garlicsim_book_button = help_menu.Append(
            -1, 'Read the &book, "Introduction to GarlicSim"...',
            ' Open the GarlicSim book, a PDF document'
        )
        
        help_menu.garlicsim_book_button.Enable(False)
        
        
        help_menu.AppendSeparator()
        
        
        online_resources_menu = help_menu.online_resources_menu = wx.Menu()
        
        help_menu.online_resources_menu_button = help_menu.AppendMenu(
            -1, '&Online resources', online_resources_menu,
            ' Use resources that require an internet connection'
        )
        
        #help_menu.online_resources_menu_button.Enable(False) tododoc: uncomment
        
        
        online_resources_menu.website_button = online_resources_menu.Append(
            -1, 'Official &website...',
            ' Open the official GarlicSim website in your browser'
        )
        
        self.Bind(
            wx.EVT_MENU,
            lambda event: webbrowser.open_new_tab('http://garlicsim.org'),
            online_resources_menu.website_button
        )
        
        
        online_resources_menu.mailing_lists_button = online_resources_menu.Append(
            -1, '&Mailing lists...',
            ''' Open the page with info about GarlicSim mailing lists\
in your browser'''
        )
        
        self.Bind(
            wx.EVT_MENU,
            lambda event: webbrowser.open_new_tab(
                'http://garlicsim.org/#mailing_lists'
                ),
            online_resources_menu.mailing_lists_button
        )
        
        
        online_resources_menu.blog_button = online_resources_menu.Append(
            -1, '&Blog...',
            ' Open the GarlicSim blog in your browser'
        )
        
        self.Bind(
            wx.EVT_MENU,
            lambda event: webbrowser.open_new_tab(
                'http://blog.garlicsim.org'
                ),
            online_resources_menu.blog_button
        )
        

        online_resources_menu.github_button = online_resources_menu.Append(
            -1, 'Code &repository...',
            ' Open the GitHub code repository for GarlicSim in your browser'
        )
        
        self.Bind(
            wx.EVT_MENU,
            lambda event: webbrowser.open_new_tab(
                'http://github.com/cool-RR/GarlicSim'
                ),
            online_resources_menu.github_button
        )
        
        
        help_menu.AppendSeparator()
        
                
        help_menu.about_button = help_menu.Append(
            wx.ID_ABOUT, '&About GarlicSim...',
            ' Tell me a little bit about the GarlicSim software'
        )
        
        self.Bind(
            wx.EVT_MENU,
            lambda event: \
                garlicsim_wx.widgets.misc.AboutDialog(self).ShowModal(),
            help_menu.about_button
        )
        
        

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
        
        dialog = garlicsim_wx.widgets.misc.SimpackSelectionDialog(self)
        
        if dialog.ShowModal() == wx.ID_OK:
            simpack = dialog.get_simpack_selection()
        else:
            dialog.Destroy()
            return
        dialog.Destroy()

        
        if self.gui_project is None:
            self._new_gui_project_from_simpack(simpack)
        else:

            if hasattr(sys, 'frozen'):
                program = [sys.executable]
            else:
                program = [sys.executable, os.path.abspath(sys.argv[0])]
                # Todo: what if some other program is launching my code?
                
            program.append('__garlicsim_wx_new=%s' % simpack.__name__)
         
            subprocess.Popen(program)
            
            return
            
    def _new_gui_project_from_simpack(self, simpack):
        assert self.gui_project is None # tododoc
        gui_project = GuiProject(simpack, self)
        self.__setup_gui_project(gui_project)

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
    
    def __setup_gui_project(self, gui_project):
        
        self.gui_project = gui_project
        
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
        
        self.gui_project.emitter_system.top_emitter.emit()
        
    
    def on_open(self, event=None):
        '''Raise a dialog for opening a gui project from file.'''
        wcd = 'GarlicSim Simulation Pickle (*.gssp)|*.gssp|All files (*)|*|'
        cur_dir = os.getcwd()
        gui_project_vars = None

        open_dialog = wx.FileDialog(self, message='Choose a file',
                                    defaultDir=cur_dir, defaultFile='',
                                    wildcard=wcd, style=wx.OPEN)
        if open_dialog.ShowModal() == wx.ID_OK:
            path = open_dialog.GetPath()
            
            if self.gui_project is None:
                self._open_gui_project_from_path(path)
            else:
                if hasattr(sys, 'frozen'):
                    program = [sys.executable]
                else:
                    program = [sys.executable, os.path.abspath(sys.argv[0])]
                    # Todo: what if some other program is launching my code?
                    
                program.append('__garlicsim_wx_load=%s' % path)
             
                subprocess.Popen(program)
                        
        
    
    def _open_gui_project_from_path(self, path):
        
        try:
            with file(path, 'r') as my_file:
                gui_project_vars = pickle_module.load(my_file)
                
        except Exception, exception:
            dialog = wx.MessageDialog(
                self,
                'Error opening file:\n' + str(exception),
                style=(wx.OK | wx.ICON_ERROR)
            )
            dialog.ShowModal()
            return
                
        if gui_project_vars:
            try:
                gui_project = GuiProject.load_from_vars(self, gui_project_vars)
            except Exception, exception:
                dialog = wx.MessageDialog(
                    self,
                    'Error opening file:\n' + str(exception),
                    style=(wx.OK | wx.ICON_ERROR)
                )
                dialog.ShowModal()
                
            self.__setup_gui_project(gui_project)

    
    
    def on_save(self, event=None):
        '''Raise a dialog for saving a gui project to file.'''
        
        assert self.gui_project is not None
        wcd = 'GarlicSim Simulation Pickle (*.gssp)|*.gssp|All files (*)|*|'
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
                        picklable_vars = self.gui_project.__getstate__()
                        pickle_module.dump(picklable_vars, my_file)
    
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
