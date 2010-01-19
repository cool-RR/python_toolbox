# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied or
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
import garlicsim.general_misc.dict_tools as dict_tools
from general_misc.stringsaver import s2i,i2s
from garlicsim.general_misc.infinity import Infinity
import garlicsim_wx.general_misc.thread_timer as thread_timer

import garlicsim
from garlicsim.asynchronous_crunching.crunchers_warehouse import crunchers

import garlicsim_wx
from widgets.general_misc import FoldableWindowContainer
        

class GuiProject(object):
    '''
    A gui project encapsulates a project for use with a wxPython interface.
    '''
    
    def __init__(self, simpack, frame):
        # This is broken down into a few parts.
        self.__init_general(simpack, frame)
        self.__init_on_creation()

        
    def __init_general(self, simpack, frame, project=None,
                       active_node=None, path=None):
        '''
        General initialization.
        
        Sets up most of the important attributes of the GuiProject, such as
        `.path` and `.active_node`.
        '''
        
        self.frame = frame
        
        
        if isinstance(simpack, garlicsim.misc.SimpackGrokker):
            
            self.simpack_grokker = simpack
            
            self.simpack = self.simpack_grokker.simpack
            
        else:
            
            wrapped_simpack = \
                garlicsim.general_misc.module_wrapper.module_wrapper_factory \
                (simpack)
            
            self.simpack = wrapped_simpack
            
            self.simpack_grokker = \
                garlicsim_wx.misc.SimpackGrokker(wrapped_simpack)
        
        self.project = project or garlicsim.Project(simpack)
        

        ### Choosing a Cruncher class: ########################################
        
        if self.project.simpack_grokker.history_dependent is False and \
           self.project.simpack_grokker.Meta.force_cruncher is None and \
           'CruncherProcess' in crunchers:
            
            self.project.crunching_manager.Cruncher = \
                crunchers['CruncherProcess']
        
        #######################################################################
            
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
        self.default_buffer = 100 # Should be a mechanism for setting that

        self.timer_for_playing = None
        '''Contains the wx.Timer object used when playing the simulation.'''

        self.ran_out_of_tree_while_playing = False
        '''
        Becomes True when you are playing the simulation and the nodes are not
        ready yet. The simulation will continue playing when the nodes will be
        created.
        '''
        
    def __init_gui(self, parent_window):
        '''
        Initialization related to the widgets which make up the gui project.
        '''
        
        frame.Bind(wx.EVT_MENU, self.edit_from_active_node,
                         id=s2i("Fork by editing"))
        main_window.Bind(wx.EVT_MENU, self.fork_naturally,
                         id=s2i("Fork naturally"))
        
        self.stuff_to_do_when_idle = Queue.Queue()
        self.main_window.Bind(wx.EVT_IDLE, self.on_idle)

        
    def __init_on_creation(self):
        '''
        Initialization done when gui project is actually created, not loaded.
        '''
        wx.CallAfter(self.make_initial_dialog)

        
    def make_initial_dialog(self):
        '''Create a dialog for creating a root state.'''
        if hasattr(self.simpack, "make_initial_dialog"):
            return self.simpack.make_initial_dialog(self)
        else:
            return self.make_generic_initial_dialog()

    def get_active_state(self):#tododoc
        return self.active_node.state if self.active_node is not None else None
        
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
        root = self.project.make_plain_root(*args, **kwargs)
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
        self.active_node = node
        if was_playing:
            self.start_playing()
        if modify_path:
            self.__modify_path_to_include_active_node()
            
        if modify_path and was_playing:
            self.infinity_job.crunching_profile.clock_target = \
                self.infinity_job.node.state.clock + self.default_buffer
            self.infinity_job = self.project.ensure_buffer_on_path(node,
                                                                   self.path,
                                                                   Infinity)   
        
        self.frame.Refresh()

        
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
        '''Start playback of the simulation.'''
        if self.is_playing:
            return
        if self.active_node is None:
            return

        self.is_playing = True
        
        self.infinity_job = \
            self.project.ensure_buffer_on_path(self.active_node, self.path,
                                                 Infinity)
        
        self.timer_for_playing = thread_timer.ThreadTimer(self)
        self.timer_for_playing.start(1000//25)
        self.Bind(thread_timer.EVT_THREAD_TIMER, self.sync_crunchers)
        
        def mission():
            play_next = functools.partial(self.__play_next, self.active_node)
            self.timer_for_playing = wx.FutureCall(self.delay * 1000, play_next)
            
        self.stuff_to_do_when_idle.put(mission)


    def stop_playing(self):
        '''Stop playback of the simulation.'''
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


    def editing_state(self):
        '''
        Get a state suitable for editing.
        
        If the current active node is "still in editing", returns its state. If
        not, forks the tree with the active node as a template and returns the
        newly created state.
        '''
        node = self.active_node
        state = node.state
        if (node.touched is False) or (node.still_in_editing is False):
            new_node = self.edit_from_active_node()
            return new_node.state
        else:
            return state

        
    def toggle_playing(self):
        '''Toggle the onscreen playback of the simulation.'''
        return self.stop_playing() if self.is_playing else self.start_playing()


    def __play_next(self, node):
        '''
        Show the next node onscreen.
        
        This method is called repeatedly when playing the simulation.
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
            play_next = functools.partial(self.__play_next, next_node)
            self.timer_for_playing = wx.FutureCall(self.delay * 1000, play_next)
            
        self.stuff_to_do_when_idle.put(mission)
        

    def fork_naturally(self, e=None):
        '''
        Fork the simulation from the active node.
        
        Used for forking the simulation without modifying any states. Creates
        a new node from the active node via natural simulation.
        '''
        #todo: maybe not let to do it from unfinalized touched node?
        
        node = self.active_node
        self.project.begin_crunching(self.active_node, self.default_buffer)


    def edit_from_active_node(self, e=None):
        '''
        Fork the simulation from the active node by editing.
        
        Returns the new node.
        '''
        new_node = self.project.tree.fork_to_edit(template_node=self.active_node)
        new_node.still_in_editing = True #todo: should be in `fork_to_edit` ?
        self.set_active_node(new_node)
        return new_node


    def sync_crunchers(self):
        '''
        Take work from the crunchers, and give them new instructions if needed.
        
        (This is a wrapper for Project.sync_crunchers() with some gui-related
        additions.)
        
        Talks with all the crunchers, takes work from them for implementing
        into the tree, retiring crunchers or recruiting new crunchers as
        necessary.

        Returns the total amount of nodes that were added to the tree in the
        process.
        '''

        added_nodes = self.project.sync_crunchers()
        '''
        This is the important line here, which actually executes
        the Project's sync_crunchers function. As you can see,
        we put the return value in `added_nodes`.
        '''
            
        if self.ran_out_of_tree_while_playing:
            self.ran_out_of_tree_while_playing = False
            self.stop_playing()
            self.start_playing()
            
        return added_nodes


    def get_node_menu(self):
        '''
        Get the node menu.
        
        The node menu lets you do actions with the active node.
        '''
        nodemenu = wx.Menu()
        nodemenu.Append(
            s2i("Fork by editing"),
            "Fork by &editing",
            " Create a new edited node with the current node as the template"
        )
        nodemenu.Append(
            s2i("Fork naturally"),
            "Fork &naturally",
            " Run the simulation from this node"
        )
        nodemenu.AppendSeparator()
        nodemenu.Append(
            s2i("Delete..."),
            "&Delete...",
            " Delete the node"
        )
        return nodemenu

    
    def done_editing(self):
        '''Finalize the changes made to the active node.'''
        node = self.active_node
        if node.still_in_editing is False:
            raise Exception('''You said 'done editing', but you were not in \
editing mode.''')
        node.still_in_editing = False
        self.project.ensure_buffer(node, self.default_buffer)

        
    def make_generic_initial_dialog(self):
        '''
        Create a generic initial dialog.
        
        This is a dialog raised immediately when the gui project is created. It
        asks the user which kind of root state he would like to start with.
        '''
        initial_dialog = \
            garlicsim_wx.widgets.misc.GenericInitialDialog(self.frame, -1)
        if initial_dialog.ShowModal() == wx.ID_OK:
            if initial_dialog.info["random"]:
                self.make_random_root()
            else:
                self.make_plain_root()
        initial_dialog.Destroy()

    