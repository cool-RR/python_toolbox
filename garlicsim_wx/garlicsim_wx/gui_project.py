# Copyright 2009-2010 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
This module defines the GuiProject class. See its documentation for more info.
'''

import warnings
import copy
import functools
import Queue
import time

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
from garlicsim_wx.general_misc import pubsub
from widgets.general_misc import FoldableWindowContainer
        

class GuiProject(object):
    '''
    A gui project encapsulates a project for use with a wxPython interface.
    '''
    
    def __init__(self, simpack, frame):
        # This is broken down into a few parts.
        self.__init_general(simpack, frame)
        self.__init_gui()
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
            
        self._path = path
        '''tododoc (privatizing) The active path.'''

        self.active_node = active_node
        '''The node that is currently displayed onscreen.'''

        self.is_playing = False
        '''Says whether the simulation is currently playing.'''
        
        self.infinity_job = None
        '''
        The job of the playing leaf, which should be crunched to infinity.
        '''
        self.default_buffer = 100 # Should be a mechanism for setting that

        self.timer_for_playing = thread_timer.ThreadTimer(self.frame)
        '''Contains the wx.Timer object used when playing the simulation.'''
        
        self.frame.Bind(thread_timer.EVT_THREAD_TIMER, self.__play_next,
                        self.timer_for_playing)

        self.defacto_playing_speed = 4
        self.official_playing_speed = 4
        self.standard_playing_speed = 4
        
        self.real_time_krap = None
        self.simulation_time_krap = None 

        self.ran_out_of_tree_while_playing = False
        '''
        Becomes True when you are playing the simulation and the nodes are not
        ready yet. The simulation will continue playing when the nodes will be
        created.
        '''
        
        # todo: move to __init_event_types
        # todo: not clear that `TreeChanged` means that only data changed
        # and not structure.
        self.TreeChanged = pubsub.EventType('TreeChanged')
        self.TreeChangedOnPath = pubsub.EventType(
            'TreeChangedOnPath',
            bases=(self.TreeChanged,)
        )
        self.TreeChangedNotOnPath = pubsub.EventType(
            'TreeChangedNotOnPath',
            bases=(self.TreeChanged,)
        )
        
        self.TreeChangedAtUnknownLocation = pubsub.EventType(
            'TreeChangedAtUnknownLocation',
            bases=(self.TreeChangedNotOnPath, self.TreeChangedOnPath,)
        )
        
        self.TreeStructureChanged = pubsub.EventType(
            'TreeStructureChanged',
            bases=(self.TreeChanged,)
        )
        self.TreeStructureChangedOnPath = pubsub.EventType(
            'TreeStructureChangedOnPath',
            bases=(
                self.TreeChangedOnPath,
                self.TreeStructureChanged
            )
        )
        self.TreeStructureChangedNotOnPath = pubsub.EventType(
            'TreeStructureChangedNotOnPath',
            bases=(
                self.TreeChangedNotOnPath,
                self.TreeStructureChanged
            )
        )
        self.TreeStructureChangedAtUnknownLocation = pubsub.EventType(
            'TreeStructureChangedAtUnknownLocation',
            bases=(
                self.TreeStructureChangedOnPath,
                self.TreeStructureChangedNotOnPath
            )
        )
        

        self.PseudoclockChanged = pubsub.EventType('PseudoclockChanged')

        self.ActiveNodeChanged = pubsub.EventType('ActiveNodeChanged')
        # todo: should possibly be subclass of PseudoclockChanged
        
        self.PathChanged = pubsub.EventType('PathChanged')
        
        self.PathContentsChanged = pubsub.EventType(
            'PathContentsChanged',
            subs=(self.PathChanged, self.TreeChangedOnPath)
        )
        
        self.PlayingToggled = pubsub.EventType('PlayingToggled')
        self.PlayingStarted = pubsub.EventType(
            'PlayingStarted',
            bases=(self.PlayingToggled,)
        )
        self.PlayingStopped = pubsub.EventType(
            'PlayingStopped',
            bases=(self.PlayingToggled,)
        )
        #todo: maybe need an event type for when editing a state?
    

    ###########################################################################
        
    def _get_path(self):
        return self._path
    
    def _set_path(self, path):
        self._path = path
        self.PathChanged().send()
        
    path = property(_get_path, _set_path, doc='The active path.')
        
    ###########################################################################
        
    def __init_gui(self):
        '''
        Initialization related to the widgets which make up the gui project.
        '''
        
        self.frame.Bind(wx.EVT_MENU, self.edit_from_active_node,
                         id=s2i("Fork by editing"))
        self.frame.Bind(wx.EVT_MENU, self.fork_naturally,
                         id=s2i("Fork naturally"))
        

        
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
        self.TreeStructureChangedNotOnPath().send()
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
        self.TreeStructureChangedNotOnPath().send()
        self.set_active_node(root)
        return root

    
    def set_active_node(self, node, modify_path=True):
        '''Make `node` the active node, displaying it onscreen.'''
        self.project.ensure_buffer(node, clock_buffer=self.default_buffer)
        
        if self.active_node is node:
            return
        
        was_playing = self.is_playing
        if self.is_playing: self.stop_playing()
        self.active_node = node
        self.ActiveNodeChanged().send()
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
        
        self.frame.Refresh() # kill this

        
    def __modify_path_to_include_active_node(self):
        '''Ensure that self.path includes the active node.'''
        if self.path is None:
            self.path = self.active_node.make_containing_path()    
        else:
            self.path.modify_to_include_node(self.active_node)
            
        self.PathChanged().send()


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
        
        self.timer_for_playing.Start(1000//25)
        
        assert self.real_time_krap == self.simulation_time_krap == None
        self.real_time_krap = time.time()
        self.simulation_time_krap = self.active_node.state.clock
        self.PlayingStarted().send()
        self.PseudoclockChanged().send()
        


    def stop_playing(self):
        '''Stop playback of the simulation.'''
        
        if self.is_playing is False:
            return

        try:
            self.timer_for_playing.Stop()
        except Exception: # todo: Find out the type
            pass
        
        self.is_playing = False
        
        assert self.infinity_job is not None
        self.infinity_job.crunching_profile.clock_target = \
            self.infinity_job.node.state.clock + self.default_buffer
        
        self.real_time_krap = self.simulation_time_krap = None
        self.PlayingStopped().send()        
        self.PseudoclockChanged().send() #todo: relevant when changes to None?
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
    
        
    def __play_next(self, event=None):
        '''
        Show the next node onscreen.
        
        This method is called repeatedly when playing the simulation.
        '''
        if self.is_playing is False: return

        current_real_time = time.time()
        real_time_elapsed = (current_real_time - self.real_time_krap)
        desired_simulation_time = \
            self.simulation_time_krap + \
            (real_time_elapsed * self.defacto_playing_speed)
        
        both_nodes = self.path.get_node_by_clock(desired_simulation_time,
                                                 rounding='both')
        # correct rounding?
        
        
        if self.defacto_playing_speed < 0:
            both_nodes = (both_nodes[1], both_nodes[0])
                
        new_node = both_nodes[0]
        
        if new_node is None:
            # This is for dealing with this edge case:
            assert both_nodes[1].state.clock == desired_simulation_time
            # Happens when moving to start of path while playing.
            new_node = both_nodes[1]
            # todo: not sure this still happens after change i did in binary
            # search conventions
            

        self.real_time_krap = current_real_time

        if both_nodes[1] is not None:
            self.simulation_time_krap = desired_simulation_time#new_node.state.clock
        else:
            self.ran_out_of_tree_while_playing = True # unneeded?
            self.simulation_time_krap = new_node.state.clock
        self.active_node = new_node
        self.PseudoclockChanged().send()
        self.ActiveNodeChanged().send()
        self.frame.Refresh() #todo: kill
        
        
        

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
        # todo: event argument is bad, in other places too
        # todo: maybe not restrict it to "from_active_node"?
        '''
        Fork the simulation from the active node by editing.
        
        Returns the new node.
        '''
        new_node = \
            self.project.tree.fork_to_edit(template_node=self.active_node)
        new_node.still_in_editing = True #todo: should be in `fork_to_edit` ?
        self.TreeStructureChangedOnPath().send()
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
        
        #leaves_to_crunch = (job.node for job in 
                            #self.project.crunching_manager.jobs)
        feisty_jobs = [job for job in self.project.crunching_manager.jobs
                       if not job.node.is_last_on_block()]
        fesity_jobs_to_nodes = dict((job, job.node) for job in feisty_jobs)
        #feisty_leaves = [leaf for leaf in leaves_to_crunch
                         #if not leaf.is_last_on_block()]
        # todo: explain what i do here
        

        added_nodes = self.project.sync_crunchers()
        
        # This is the heavy line here, which actually executes the Project's
        # sync_crunchers function.
        
        
        
        if added_nodes > 0:
            if any(fesity_jobs_to_nodes[job] is not job.node
                   for job in feisty_jobs):
                self.TreeStructureChanged().send()
            else:
                self.TreeChanged().send()
            # todo: It would be hard but nice to know whether the tree changes
            # were on the path. This could save some rendering on SeekBar.
            
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
editing mode.''') # change to fitting exception class
        node.still_in_editing = False
        
        self.TreeStructureChangedOnPath()
        # not sure whether it's considered a structure change or even just a
        # change, but playing it safe
        
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

    