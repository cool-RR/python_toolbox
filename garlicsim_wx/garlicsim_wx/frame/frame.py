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
import traceback

import wx
from garlicsim_wx.general_misc.third_party import aui
import pkg_resources

from garlicsim.general_misc import dict_tools
from garlicsim.general_misc import string_tools
from garlicsim_wx.general_misc import thread_timer
from garlicsim_wx.general_misc import wx_tools

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
        '''The aui manager, which manages the workspace widgets.'''
                
        self.gui_project = None
        '''The current gui project.'''
        
        self.CreateStatusBar()
        
        self.__init_menus()
        self.__init_key_handlers()
        
        self.Bind(wx.EVT_CONTEXT_MENU, self.on_context_menu, self)
        
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

        
    def __init_menus(self):
        '''Initialize the menu bar and the context menu.'''
        menu_bar = self.menu_bar = garlicsim_wx.misc.MenuBar(self)
        self.SetMenuBar(menu_bar)
        self._recalculate_all_menus()
        self.context_menu = \
            garlicsim_wx.general_misc.cute_menu.CuteMenu.add_menus([
                garlicsim_wx.misc.menu_bar.node_menu.NodeMenu(self),
                garlicsim_wx.misc.menu_bar.block_menu.BlockMenu(self)
            ])
        
        
    def _recalculate_all_menus(self):
        '''Recalculate all the menus, determining in which state they'll be.'''
        try_recalculate = lambda thing: \
            thing._recalculate() if hasattr(thing, '_recalculate') else None
        
        menus_to_recalculate = [menu for (menu, label) in                                 
                                self.menu_bar.GetMenus()]
        
        while menus_to_recalculate:
            menu = menus_to_recalculate.pop()
            for item in menu.GetMenuItems():
                if item.IsSubMenu():
                    menus_to_recalculate.append(item.GetSubMenu())
                else:
                    try_recalculate(item)
            try_recalculate(menu)
        try_recalculate(self.menu_bar)

        
    def __init_key_handlers(self):
        '''Initialize key shortcuts.'''
        
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
        
        def on_home():
            '''Go to root node.'''
            if self.gui_project is not None and \
               self.gui_project.path is not None:
                
                try:
                    self.gui_project.set_active_node(self.gui_project.path[0])
                except LookupError:
                    pass

                
        def on_end():
            '''Go to leaf node.'''
            if self.gui_project is not None and \
               self.gui_project.path is not None:
                
                try:
                    self.gui_project.set_active_node(self.gui_project.path[-1])
                except LookupError:
                    pass

                
        def on_up():
            '''Go one path upwards.'''
            if self.gui_project.path and self.gui_project.active_node:
                try:
                    new_path = self.gui_project.path._get_lower_path(
                        self.gui_project.active_node
                    )
                except LookupError:
                    return
                pseudoclock = self.gui_project.pseudoclock
                self.gui_project.path = new_path
                self.gui_project.path_changed_emitter.emit()
                self.gui_project.set_pseudoclock(pseudoclock)

                
        def on_down():
            '''Go one path downwards.'''
            if self.gui_project.path and self.gui_project.active_node:
                try:
                    new_path = self.gui_project.path._get_higher_path(
                        self.gui_project.active_node
                    )
                except LookupError:
                    return
                pseudoclock = self.gui_project.pseudoclock
                self.gui_project.path = new_path
                self.gui_project.path_changed_emitter.emit()
                self.gui_project.set_pseudoclock(pseudoclock)
                
                
        def on_left():
            '''Go one node backwards.'''
            if self.gui_project is not None and \
               self.gui_project.active_node is not None:
                
                parent = self.gui_project.active_node.parent
                if parent is not None:
                    self.gui_project.set_active_node(parent)
        
                    
        def on_right():
            '''Go one node forward.'''
            if self.gui_project is not None and \
               self.gui_project.path is not None and \
               self.gui_project.active_node is not None:
                
                try:
                    child = self.gui_project.path.next_node\
                          (self.gui_project.active_node)
                    self.gui_project.set_active_node(child)
                except LookupError:
                    pass
            
                
        def on_command_left():
            '''Go five nodes backwards.'''
            if self.gui_project is not None and \
               self.gui_project.active_node is not None:
                
                node = self.gui_project.active_node.get_ancestor(5, round=True)
                if node:
                    self.gui_project.set_active_node(node)
        
                    
        def on_command_right():
            '''Go five nodes forward.'''
            if self.gui_project is not None and \
               self.gui_project.path is not None and \
               self.gui_project.active_node is not None:
                
                current = self.gui_project.active_node
                for i in xrange(5):
                    try:
                        current = self.gui_project.path.next_node(current)
                    except LookupError:
                        pass
                self.gui_project.set_active_node(current)
        
                
        def on_page_up():
            '''Go 20 nodes backwards.'''
            if self.gui_project is not None and \
               self.gui_project.active_node is not None:
                
                node = self.gui_project.active_node.get_ancestor(20, round=True)
                if node:
                    self.gui_project.set_active_node(node)
        
                    
        def on_page_down():
            '''Go 20 nodes forward.'''
            if self.gui_project is not None and \
               self.gui_project.path is not None and \
               self.gui_project.active_node is not None:
                
                current = self.gui_project.active_node
                for i in xrange(20):
                    try:
                        current = self.gui_project.path.next_node(current)
                    except LookupError:
                        pass
                self.gui_project.set_active_node(current)

                
        def on_space():
            '''Toggle onscreen playback.'''
            if self.gui_project:
                self.gui_project.toggle_playing()
        
                
        def on_return():
            '''Finalize the active node, if it's in editing.'''
            if self.gui_project and self.gui_project.active_node.still_in_editing:
                self.gui_project.finalize_active_node()

        
                
        
        self.key_handlers = {
            wx_tools.Key(wx.WXK_HOME): on_home,
            wx_tools.Key(wx.WXK_END): on_end,
            wx_tools.Key(wx.WXK_UP): on_up,
            wx_tools.Key(wx.WXK_DOWN): on_down,
            wx_tools.Key(wx.WXK_LEFT): on_left,
            wx_tools.Key(wx.WXK_RIGHT): on_right,
            wx_tools.Key(wx.WXK_LEFT, cmd=True): on_command_left,
            wx_tools.Key(wx.WXK_RIGHT, cmd=True): on_command_right,
            wx_tools.Key(wx.WXK_PAGEUP): on_page_up,
            wx_tools.Key(wx.WXK_PAGEDOWN): on_page_down,
            wx_tools.Key(wx.WXK_SPACE): on_space,
            wx_tools.Key(wx.WXK_RETURN): on_return,
        }    
            
        
    def on_close(self, event):
        '''Close the frame.'''
        if self.gui_project:
            self.gui_project.stop_playing()
        self.aui_manager.UnInit()
        self.Destroy()
        garlicsim_wx.general_misc.cute_base_timer.CuteBaseTimer.\
                    stop_timers_by_frame(self)
        event.Skip()        
        self.background_timer.stop()

        
    def finalize_active_node(self, e=None):
        '''Finalize editing of the active node in the active gui project.'''
        assert self.gui_project
        return self.gui_project.finalize_active_node()

    
    def on_new(self, event=None):
        '''Create a new gui project.'''        
        
        if self.gui_project is not None:
            
            if hasattr(sys, 'frozen'):
                program_to_run = [sys.executable]
                we_are_main_program = 'GarlicSim' in sys.executable
            else:
                main_script = os.path.abspath(sys.argv[0])
                program_to_run = [sys.executable, main_script]
                we_are_main_program = ('run_gui' in main_script) or \
                                    ('garlicsim_wx' in main_script)
            
            if not we_are_main_program:
                warning_dialog = \
                    garlicsim_wx.widgets.misc.NotMainProgramWarningDialog(self)
                if warning_dialog.ShowModal() != wx.ID_YES:
                    return
        
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
                
            program_to_run.append('__garlicsim_wx_new=%s' % simpack.__name__)
         
            subprocess.Popen(program_to_run)
            
            return
            
    def _new_gui_project_from_simpack(self, simpack):
        '''
        Start a new gui project, given the simpack to start it with.
        
        Internal use.
        '''
        assert self.gui_project is None
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
        '''
        Setup a newly-created gui project.
        
        Internal use.
        '''
        
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
            self.state_repr_viewer = self.big_widget
        
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
        
        if self.gui_project is not None:
            
            if hasattr(sys, 'frozen'):
                program_to_run = [sys.executable]
                we_are_main_program = 'GarlicSim' in sys.executable
            else:
                main_script = os.path.abspath(sys.argv[0])
                program_to_run = [sys.executable, main_script]
                we_are_main_program = ('run_gui' in main_script) or \
                                    ('garlicsim_wx' in main_script)
            
            if not we_are_main_program:
                dialog = \
                    garlicsim_wx.widgets.misc.NotMainProgramWarningDialog(self)
                if dialog.ShowModal() != wx.ID_YES:
                    return
                
        wildcard = 'GarlicSim Simulation Pickle (*.gssp)|*.gssp|All files (*)|*|'
        
        # Todo: something more sensible here. Ideally should be last place you
        # saved in, but for starters can be desktop.
        folder = os.getcwd()
        
        gui_project_vars = None

        open_dialog = wx.FileDialog(self, message='Choose a file',
                                    defaultDir=folder, defaultFile='',
                                    wildcard=wildcard, style=wx.OPEN)
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
                    
                program.append(path)
             
                subprocess.Popen(program)
                        
        
    
    def _open_gui_project_from_path(self, path):
        '''
        Open a gui project saved to a file specified by `path`.
        
        Internal use.
        '''
        
        old_recursion_limit = sys.getrecursionlimit()
            
        try:
            sys.setrecursionlimit(10000)
            with open(path, 'rb') as my_file:
                gui_project_vars = pickle_module.load(my_file)
                
        except Exception, exception:
            dialog = wx.MessageDialog(
                self,
                'Error opening file:\n' + traceback.format_exc(),
                style=(wx.OK | wx.ICON_ERROR)
            )
            dialog.ShowModal()
            return
        
        finally:
            sys.setrecursionlimit(old_recursion_limit)
                
        if gui_project_vars:
            try:
                gui_project = GuiProject.load_from_vars(self, gui_project_vars)
            except Exception, exception:
                error_dialog = wx.MessageDialog(
                    self,
                    'Error opening file:\n' + traceback.format_exc(),
                    style=(wx.OK | wx.ICON_ERROR)
                )
                error_dialog.ShowModal()
                error_dialog.Destroy()
                
            self.__setup_gui_project(gui_project)

    
    
    def on_save(self, event=None):
        '''Raise a dialog for saving a gui project to file.'''
        
        assert self.gui_project is not None
        wildcard = 'GarlicSim Simulation Pickle (*.gssp)|*.gssp|All files (*)|*|'
        folder = os.getcwd()
        
        save_dialog = wx.FileDialog(self, message='Save file as...',
                                 defaultDir=folder, defaultFile='',
                                 wildcard=wildcard,
                                 style=wx.SAVE | wx.OVERWRITE_PROMPT)
        if save_dialog.ShowModal() == wx.ID_OK:
            path = save_dialog.GetPath()
            
            old_recursion_limit = sys.getrecursionlimit()
            
            try:
                sys.setrecursionlimit(10000)
                with open(path, 'wb') as my_file:
                    picklable_vars = self.gui_project.__getstate__()
                    pickle_module.dump(picklable_vars, my_file, protocol=2)

            except Exception, exception:
                error_dialog = wx.MessageDialog(
                    self,
                    'Error saving to file:\n' + traceback.format_exc(),
                    style=(wx.OK | wx.ICON_ERROR)
                )
                error_dialog.ShowModal()
                error_dialog.Destroy()
            
            finally:
                sys.setrecursionlimit(old_recursion_limit)
            
            
        save_dialog.Destroy()
    
    """    
    def delete_gui_project(self,gui_project):
        I did this wrong.
        self.gui_projects.remove(gui_project)
        self.notebook.AddPage(gui_project.main_window,"zort!")
        self.notebook.DeletePage(0)
        del gui_project
    """
    
    
    def on_key_down(self, event):
        '''wx.EVT_KEY_DOWN handler.'''
        key = wx_tools.Key.get_from_key_event(event)
        handler = self.key_handlers.get(key, None)
        if handler:
            handler()
        else:
            event.Skip()
            
            
    def on_context_menu(self, event):
        '''wx.EVT_CONTEXT_MENU handler.'''
        abs_position = event.GetPosition()
        if abs_position == wx.DefaultPosition:
            position = (0, 0)
        else:
            position = self.ScreenToClient(abs_position)
            
        self.PopupMenu(self.context_menu, position)
        
    
    
