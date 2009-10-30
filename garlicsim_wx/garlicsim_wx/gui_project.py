# Copyright 2009 Ram Rachum. No part of this program may be used, copied or
# distributed without explicit written permission from Ram Rachum.

'''
This module defines the GuiProject class. See its documentation for more info.
'''

import warnings
import copy
import functools
import Queue

import wx
import wx.lib.scrolledpanel
import wx.py.shell

import garlicsim.general_misc.queue_tools as queue_tools
from general_misc.stringsaver import s2i,i2s
from garlicsim.general_misc.infinity import Infinity

import garlicsim
import garlicsim.asynchronous_crunching.crunchers

import custom_widgets
from custom_widgets import FoldableWindowContainer


class GuiProject(object):
    '''
    A GuiProject encapsulates a Project for use with a wxPython interface.
    '''
    
    def __init__(self, simpack, parent_window):
        # This is broken down into a few parts.
        self.__init_general(simpack, parent_window)
        self.__init_on_creation()

        
    def __init_general(self, simpack, parent_window, project=None,
                       active_node=None, path=None):
        '''
        General initialization.
        
        Sets up most of the important attributes of the GuiProject, such as
        `.path` and `.active_node`.
        '''
        
        self.simpack = \
            garlicsim.general_misc.module_wrapper.ModuleWrapper(simpack)
        
        self.project = project or garlicsim.Project(simpack)
        if self.project.simpack_grokker.history_dependent is False:
            self.project.crunching_manager.Cruncher = \
                garlicsim.asynchronous_crunching.crunchers.CruncherProcess
        
        self.path = path
        '''The active path.'''

        self.active_node = active_node
        '''The node that is currently displayed onscreen.'''

        self.is_playing = False
        '''Says whether the simulation is currently playing.'''
        
        self.infinity_job = None
        '''
        The job of the playing leaf, which should be crunched to infinity.
        '''

        self.delay = 0.05 # Should be a mechanism for setting that
        self.default_buffer = 100 # Should be a mechanism for setting that

        self.timer_for_playing=None
        '''Contains the wx.Timer object used when playing the simulation.'''

        self.ran_out_of_tree_while_playing = False
        '''
        Becomes True when you are playing the simulation and the nodes are not
        ready yet. The simulation will continue playing when the nodes will be
        created.
        '''

        self.__init_gui(parent_window)
        
        simpack.initialize(self)

        
    def __init_gui(self, parent_window):
        '''
        Initialization related to the GUI widgets which make up the GuiProject.
        '''
        main_window = self.main_window = wx.ScrolledWindow(parent_window, -1)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_window.SetSizer(self.main_sizer)

        self.state_showing_window = \
            wx.lib.scrolledpanel.ScrolledPanel(self.main_window, -1)

        locals_for_shell = locals()
        locals_for_shell.update({'gp': self,
                                 'p': self.project,
                                 't': self.project.tree,
                                 'garlicsim': garlicsim})
        self.shell = wx.py.shell.Shell(self.main_window, -1, size=(400, -1),
                                       locals=locals_for_shell)
        self.seek_bar = custom_widgets.SeekBar(self.main_window, -1, self)
        self.tree_browser = custom_widgets.TreeBrowser(self.main_window, -1,
                                                       self)


        self.top_fwc = FoldableWindowContainer(self.main_window, -1,
                                               self.state_showing_window,
                                               self.shell, wx.RIGHT,
                                               folded=True)
        temp = FoldableWindowContainer(self.main_window, -1, self.top_fwc,
                                       self.seek_bar, wx.BOTTOM)
        temp = FoldableWindowContainer(self.main_window, -1, temp,
                                       self.tree_browser, wx.BOTTOM)
        self.main_sizer.Add(temp, 1, wx.EXPAND)
        self.main_sizer.Fit(self.main_window)
        
        main_window.Bind(wx.EVT_MENU, self.edit_from_active_node,
                         id=s2i("Fork by editing"))
        main_window.Bind(wx.EVT_MENU, self.fork_naturally,
                         id=s2i("Fork naturally"))
        
        self.stuff_to_do_when_idle = Queue.Queue()
        self.main_window.Bind(wx.EVT_IDLE, self.on_idle)

        
    def __init_on_creation(self):
        '''
        Initialization done when the GuiProject is actually created, not loaded.
        '''
        wx.CallAfter(self.make_initial_dialog)

        
    def make_initial_dialog(self):
        '''
        Create a dialog for creating a root state.
        '''
        if hasattr(self.simpack,"make_initial_dialog"):
            return self.simpack.make_initial_dialog(self)
        else:
            return self.make_generic_initial_dialog()

        
    def show_state(self, state):
        '''Show the state onscreen.'''
        self.simpack.show_state(self,state)

        
    def set_parent_window(self, parent_window):
        '''
        Set the parent wxPython window of the main window of the GuiProject.
        '''
        self.main_window.Reparent(parent_window)        
        
        
    def on_idle(self, event=None):
        '''Handler for the wx.EVT_IDLE event.'''
        try:
            mission = self.stuff_to_do_when_idle.get(block=False)
            mission()
            event.RequestMore(True)
        except Queue.Empty:
            pass
                

    def make_plain_root(self, *args, **kwargs):
        '''
        Create a parentless node, whose state is a simple plain state.
        
        The simpack must define the function "make_plain_state" for this to
        work.
        Updates the active path to start from this root.
        Starts crunching on this new root.
        Returns the node.
        '''
        root = self.project.make_plain_root(*args,**kwargs)
        self.set_active_node(root)
        return root

    
    def make_random_root(self, *args, **kwargs):
        '''
        Create a parentless node, whose state is a random and messy state.
        
        The simpack must should define the function "make_random_state" for
        this to work.
        Updates the active path to start from this root.
        Starts crunching on this new root.
        Returns the node.
        '''
        root = self.project.make_random_root(*args, **kwargs)
        self.set_active_node(root)
        return root

    
    def set_active_node(self, node, modify_path=True):
        '''
        Make `node` the active node, displaying it onscreen.
        '''
        self.project.ensure_buffer(node, clock_buffer=self.default_buffer)
        
        was_playing = self.is_playing
        if self.is_playing: self.stop_playing()

        self.show_state(node.state)
        self.active_node = node
        if was_playing:
            self.start_playing()
        if modify_path:
            self.__modify_path_to_include_active_node()
            
        if modify_path and was_playing:
            self.infinity_job.crunching_profile.clock_buffer = \
                self.infinity_job.node.state.clock + self.default_buffer
            self.infinity_job = self.project.ensure_buffer_on_path(node,
                                                                   self.path,
                                                                   Infinity)    
            
        self.main_window.Refresh()

        
    def __modify_path_to_include_active_node(self):
        '''
        Ensure that self.path includes the active node.
        '''
        if self.path is None:
            self.path = self.active_node.make_containing_path()
            return
        if not self.active_node in self.path:
            self.path.modify_to_include_node(self.active_node)


    def start_playing(self):
        '''
        Start playback of the simulation.
        '''
        if self.is_playing:
            return
        if self.active_node is None:
            return

        self.is_playing = True
        
        self.infinity_job = \
            self.project.ensure_buffer_on_path(self.active_node, self.path,
                                                 Infinity)
        
        def mission():
            self.timer_for_playing = wx.FutureCall(self.delay*1000, functools.partial(self.__play_next, self.active_node))
        self.stuff_to_do_when_idle.put(mission)


    def stop_playing(self):
        '''
        Stops playback of the simulation.
        '''
        if self.timer_for_playing is not None:
            try:
                self.timer_for_playing.Stop()
            except Exception:
                pass
            
        if self.is_playing is False:
            return
        
        self.is_playing = False
        
        assert self.infinity_job is not None
        self.infinity_job.crunching_profile.clock_target = \
            self.infinity_job.node.state.clock + self.default_buffer
        
        queue_tools.dump(self.stuff_to_do_when_idle)
        assert self.stuff_to_do_when_idle.qsize() == 0
        self.project.ensure_buffer(self.active_node, self.default_buffer)


    def __editing_state(self):
        node=self.active_node
        state=node.state
        if node.touched is False or node.still_in_editing is False:
            new_node=self.edit_from_active_node()
            return new_node.state
        else:
            return state

        
    def toggle_playing(self):
        '''
        If the simulation is currently playing, stops it.
        Otherwise, starts playing.
        '''
        return self.stop_playing() if self.is_playing else self.start_playing()


    def __play_next(self, node):
        '''
        A function called repeatedly while playing the simulation.
        '''
        if self.is_playing is False: return
        self.show_state(node.state)
        self.main_window.Refresh() # Make more efficient?
        self.active_node = node
        try:
            next_node = self.path.next_node(node)
        except garlicsim.data_structures.path.PathOutOfRangeError:
            self.ran_out_of_tree_while_playing = True
            return
        
        def mission():
            self.timer_for_playing = wx.FutureCall(self.delay*1000,
                                                   functools.partial(self.__play_next,
                                                                     next_node))
            
        self.stuff_to_do_when_idle.put(mission)
        

    def fork_naturally(self, *args, **kwargs):
        '''
        Used for forking the simulation without modifying any states.
        Creates a new node from the active node via natural simulation.

        todo: maybe not let to do it from unfinalized touched node?
        '''
        
        node = self.active_node
        self.project.begin_crunching(self.active_node, self.default_buffer)
        # todo: give so_profile


    def edit_from_active_node(self,*args,**kwargs):
        '''
        Used for forking the simulation by editing.
        Creates a new node from the active node via
        editing.
        Returns the new node.
        '''
        new_node = self.project.tree.fork_to_edit(template_node=self.active_node)
        new_node.still_in_editing = True #todo: should be in `fork_to_edit` ?
        self.set_active_node(new_node)
        return new_node


    def sync_crunchers(self):
        '''
        A wrapper for Project.sync_crunchers(). (todo: add real explanation)
        Returns how many nodes were added to the tree.
        '''

        added_nodes=self.project.sync_crunchers()
        '''
        This is the important line here, which actually executes
        the Project's sync_crunchers function. As you can see,
        we put the return value in `added_nodes`.
        '''

        if added_nodes>0:
            self.tree_modify_refresh()
        if self.ran_out_of_tree_while_playing:
            self.ran_out_of_tree_while_playing = False
            self.stop_playing()
            self.start_playing()
        return added_nodes


    def get_node_menu(self):
        nodemenu=wx.Menu()
        nodemenu.Append(s2i("Fork by editing"),"Fork by &editing"," Create a new edited node with the current node as the template")
        nodemenu.Append(s2i("Fork naturally"),"Fork &naturally"," Run the simulation from this node")
        nodemenu.AppendSeparator()
        nodemenu.Append(s2i("Delete..."),"&Delete..."," Delete the node")
        return nodemenu

    
    def done_editing(self):
        node=self.active_node
        if node.still_in_editing==False:
            raise StandardError("You said 'done editing', but you were not in editing mode.")
        node.still_in_editing=False
        self.project.ensure_buffer(node, self.default_buffer)

        
    def make_generic_initial_dialog(self):
        initial_dialog=custom_widgets.GenericInitialDialog(self.main_window, -1)
        if initial_dialog.ShowModal()==wx.ID_OK:
            if initial_dialog.info["random"]:
                self.make_random_root()
            else:
                self.make_plain_root()
        initial_dialog.Destroy()

        
    def tree_modify_refresh(self):
        self.seek_bar.Refresh()
        self.tree_browser.Refresh()
        
    def tickle(self):
        stuff_we_want = ["project", "path", "active_node", "simpack"]
        my_dict = {}
        for thing in stuff_we_want:
            my_dict[thing] = self.__dict__[thing]
        return my_dict
    
    
def load_tickled_gui_project(tickled_gui_project, parent_window):
    gui_project = GuiProject.__new__(GuiProject)
    
    simpack = tickled_gui_project.pop("simpack")
    
    gui_project._GuiProject__init_general(simpack, parent_window,
                                          **tickled_gui_project)
    return gui_project
        
    
    
    