# Copyright 2009-2011 Ram Rachum. No part of this program may be used, copied
# or distributed without explicit written permission from Ram Rachum.

'''
Defines the `GuiProject` class.

See its documentation for more info.
'''

from __future__ import with_statement

import time

import wx

from .general_misc.stringsaver import s2i, i2s
from garlicsim.general_misc.infinity import infinity
from garlicsim.general_misc import binary_search
from garlicsim.general_misc import import_tools
from garlicsim_wx.general_misc.emitting_ordered_set import EmittingOrderedSet
from garlicsim_wx.general_misc.emitting_weak_key_default_dict import \
     EmittingWeakKeyDefaultDict
from garlicsim_wx.misc.step_profile_hue_default_factory import \
     StepProfileHueDefaultFactory
from garlicsim_wx.general_misc import thread_timer

import garlicsim
from garlicsim.asynchronous_crunching import crunchers
import garlicsim_wx
from garlicsim_wx.general_misc import emitters
        

class GuiProject(object):
    '''Encapsulates a project for use with a wxPython interface.'''
    
    def __init__(self, simpack, frame, project=None):
        '''
        Construct the gui project.
        
        `simpack` is the simpack (or grokker) to use. `frame` is the frame in
        which this gui project will live.
        '''
        # This is broken down into a few parts.
        self.__init_general(simpack, frame, project)
        self.__init_gui()
        if not self.project.tree.roots:
            wx.CallAfter(self.make_state_creation_dialog)

            
    def __init_general(self, simpack, frame, project=None):
        '''General initialization.'''
        
        self.frame = frame
        '''The frame that this gui project lives in.'''
        
        assert isinstance(self.frame, garlicsim_wx.Frame)
        
        if isinstance(simpack, garlicsim.misc.SimpackGrokker):
            simpack_grokker = simpack            
            simpack = simpack_grokker.simpack
        else:
            simpack_grokker = garlicsim.misc.SimpackGrokker(simpack)
            
            
        self.simpack = simpack
        '''The simpack used for this gui project.'''
        
        self.simpack_grokker = simpack_grokker
        '''The simpack grokker used for this gui project.'''
        
        self.simpack_wx_grokker = garlicsim_wx.misc.SimpackWxGrokker(simpack)
        '''The simpack_wx used for this gui project.'''
        
        self.project = project or garlicsim.Project(simpack_grokker)
        '''The project encapsulated in this gui project.'''
        
        assert isinstance(self.project, garlicsim.Project)
        

        ### If it's a new project, use `ProcessCruncher` if available: ########
        #                                                                     #
        
        if (not project): # Note this is the project given as an argument
            if (crunchers.ProcessCruncher in 
                simpack_grokker.available_cruncher_types):
                
                self.project.crunching_manager.cruncher_type = \
                    crunchers.ProcessCruncher
        #                                                                     #
        #######################################################################
            
        self.path = None
        '''The active path.'''

        self.active_node = None
        '''The node that is currently displayed onscreen.'''

        self.is_playing = False
        '''Says whether the simulation is currently playing.'''
        
        self.infinity_job = None
        '''
        The job of the playing leaf, which should be crunched to infinity.
        '''
        
        self.default_buffer = 100
        '''
        The default clock buffer to crunch from an active node.

        For the user it is called "Autocrunch".
        '''
        
        self._default_buffer_before_cancellation = None
        '''
        The value of the default buffer before buffering was cancelled.

        When buffering will be enabled again, it will be set to this value.
        '''

        self.timer_for_playing = thread_timer.ThreadTimer(self.frame)
        '''Contains the timer object used when playing the simulation.'''
        
        self.frame.Bind(thread_timer.EVT_THREAD_TIMER, self.__play_next,
                        self.timer_for_playing)

        self.defacto_playing_speed = 4
        '''The playing speed that we are actually playing in.'''
        
        self.official_playing_speed = 4
        '''
        The playing speed that we're "officially" playing in.
        
        The defacto playing speed may deviate from this.
        '''
        
        self.standard_playing_speed = 4
        '''The reference playing speed. This speed is considered "normal".'''
        
        self.last_tracked_real_time = None
        '''
        The last tracked time point (real time, not simulation), for playback.
        '''
        
        self.pseudoclock = 0
        '''
        The current pseudoclock.
        
        The pseudoclock is *something like* the clock of the current active
        node. But not exactly. We're letting the pseudoclock slide more
        smoothly from one node to its neighbor, instead of jumping. This is in
        order to make some things smoother in the program. This is also why
        it's called "pseudo".
        '''
        
        self.default_step_profile = garlicsim.misc.StepProfile(
            self.simpack_grokker.default_step_function
        )
        '''The step profile that will be used be default.'''
        
        self.step_profiles = EmittingOrderedSet(
            emitter=None,
            items=(self.default_step_profile,)
        )
        '''An ordered set of step profiles that the user may use.'''
        
        self.step_profiles_to_hues = EmittingWeakKeyDefaultDict(
            emitter=None,
            default_factory=StepProfileHueDefaultFactory(self),
        )
        '''Mapping from step profile to hue that represents it in GUI.'''
        
        self._tracked_step_profile = None
        self._temp_shell_history = None
        self._temp_shell_command_history = None
        self._job_and_node_of_recent_fork_by_crunching = None
        
        ### Setting up namespace: #############################################
        #                                                                     #
        
        self.namespace = {
            
            '__name__': '__garlicsim_shell__',
            # This will become `.__module__` of classes and functions.
            
            'f': frame, 'frame': frame,
            'gp': self, 'gui_project': self,
            'p': self.project, 'project': self.project,
            't': self.project.tree, 'tree': self.project.tree,
            'gs': garlicsim, 'garlicsim': garlicsim,
            'gs_wx': garlicsim_wx, 'garlicsim_wx': garlicsim_wx,
            'wx': wx,
            'simpack': self.simpack,
            self.simpack.__name__.rsplit('.', 1)[-1]: self.simpack,
        }
        '''Namespace that will be used in shell and other places.'''
        
        garlicsim_lib = import_tools.import_if_exists('garlicsim_lib',
                                                      silent_fail=True)
        if garlicsim_lib:
            self.namespace.update({
                'gs_lib': garlicsim_lib,
                'garlicsim_lib': garlicsim_lib,
            })
        
        #                                                                     #
        ### Finished setting up namespace. ####################################
        
            
        self.__init_emitters()
        self.__init_menu_enablings()
        
        self.emitter_system.top_emitter.emit()
        # Just for good measure, jiggle all the widgets up.
        
        
    def __init_emitters(self):
        '''Create an emitter system and a bunch of emitters.'''
        
        # todo: not clear that `tree_modified_emitter` means that only data
        # changed and not structure.
        
        self.emitter_system = emitters.EmitterSystem()
                
        with self.emitter_system.freeze_cache_rebuilding:
        
            es = self.emitter_system
            
            self.tree_modified_emitter = es.make_emitter(
                name='tree_modified',
            )
            self.tree_modified_on_path_emitter = es.make_emitter(
                outputs=(self.tree_modified_emitter,),
                name='tree_modified_on_path',
            )
    
            self.tree_modified_not_on_path = es.make_emitter(
                outputs=(self.tree_modified_emitter,),
                name='tree_modified_not_on_path',
            )
            
            self.tree_modified_at_unknown_location_emitter = es.make_emitter(
                outputs=(
                    self.tree_modified_on_path_emitter,
                    self.tree_modified_not_on_path,
                ),
                name='tree_modified_at_unknown_location',
            )
            
            self.tree_structure_modified_emitter = es.make_emitter(
                outputs=(
                    self.tree_modified_emitter,
                    self._update_step_profiles_set,
                    self._if_forked_by_crunching_recently_switch_to_new_path,
                    ),
                name='tree_structure_modified',
            )
            
            self.tree_structure_modified_on_path_emitter = es.make_emitter(
                outputs=(
                    self.tree_modified_on_path_emitter,
                    self.tree_structure_modified_emitter
                ),
                name='tree_structure_modified_on_path',
            )
            self.tree_structure_modified_not_on_path_emitter = es.make_emitter(
                outputs=(
                    self.tree_modified_not_on_path,
                    self.tree_structure_modified_emitter
                ),
                name='tree_structure_modified_not_on_path',
            )
            self.tree_structure_modified_at_unknown_location_emitter = \
                es.make_emitter(
                outputs=(
                    self.tree_structure_modified_on_path_emitter,
                    self.tree_structure_modified_not_on_path_emitter,
                    self.tree_modified_at_unknown_location_emitter
                ),
                name='tree_structure_modified_at_unknown_location',
            )
            
    
            self.pseudoclock_modified_emitter = es.make_emitter(
                name='pseudoclock_modified'
            )
    
            self.active_node_changed_emitter = es.make_emitter(
                name='active_node_changed'
            )
            # todo: should possibly take input from
            # `pseudoclock_modified_emitter`
            
            self.active_node_modified_emitter = es.make_emitter(
                name='active_node_modified'
            )
            
            self.active_node_changed_or_modified_emitter = es.make_emitter(
                inputs=(
                    self.active_node_changed_emitter,
                    self.active_node_modified_emitter,
                ),
                outputs=(self.__check_if_step_profile_changed,),
                name='active_node_changed_or_modified'
            )
            
            self.active_step_profile_changed_emitter = es.make_emitter(
                name='active_step_profile_changed'
            )
            
            self.path_changed_emitter = es.make_emitter(
                name='path_changed'
            )
            
            self.path_contents_changed_emitter = es.make_emitter(
                inputs=(
                    self.path_changed_emitter,
                    self.tree_modified_on_path_emitter
                ),
                name='path_contents_changed',
            )
            
            self.playing_toggled_emitter = es.make_emitter(
                name='playing_toggled',
            )
            self.playing_started_emitter = es.make_emitter(
                outputs=(self.playing_toggled_emitter,),
                name='playing_started',
            )
            self.playing_stopped_emitter = es.make_emitter(
                outputs=(self.playing_toggled_emitter,),
                name='playing_stopped',
            )
    
            self.official_playing_speed_modified_emitter = es.make_emitter(
                outputs=(self.update_defacto_playing_speed,),
                name='official_playing_speed_modified',
            )
            
            self.active_node_finalized_emitter = es.make_emitter(
                inputs=(self.active_node_modified_emitter,),
                outputs=(self.tree_modified_on_path_emitter,), # todo: correct?
                name='active_node_finalized',
            )
            
            #todo: maybe need an emitter for when editing a state?
            
            ###################################################################
            
            self.default_buffer_modified_emitter = es.make_emitter(
                name='default_buffer_modified',
            )
            
            self.step_profiles_set_modified_emitter = es.make_emitter(
                outputs=(
                    self.frame.menu_bar.node_menu.\
                    fork_by_crunching_using_menu._recalculate,
                    self.frame.context_menu.\
                    fork_by_crunching_using_menu._recalculate
                ),
                name='step_profiles_set_modified'
            )
            self.step_profiles.set_emitter(
                self.step_profiles_set_modified_emitter
            )
            
            self.step_profiles_to_hues_modified_emitter = es.make_emitter(
                name='step_profiles_to_hues_modified',
            )
            self.step_profiles_to_hues.set_emitter(
                self.step_profiles_to_hues_modified_emitter
            )
            
            self.all_menus_need_recalculation_emitter = es.make_emitter(
                outputs=(self.frame._recalculate_all_menus,),
                name='all_menus_need_recalculation_emitter'
            )
            
            self.cruncher_type_changed_emitter = es.make_emitter(
                name='cruncher_type_changed_emitter'
            )
            
            

    def __init_menu_enablings(self):
        '''Connect the functions that (en/dis)able menus to the emitters.'''
        for menu in [self.frame.menu_bar.node_menu,
                     self.frame.menu_bar.block_menu]:
            
            self.active_node_changed_or_modified_emitter.add_output(
                menu._recalculate
            )
        
            
    def __init_gui(self):
        '''
        Initialization related to the widgets which make up the gui project.
        '''
        
        self.frame.Bind(wx.EVT_MENU, self.on_fork_by_editing_menu_item,
                         id=s2i("Fork by editing"))
        self.frame.Bind(wx.EVT_MENU, self.on_fork_by_crunching_menu_item,
                         id=s2i("Fork by crunching"))
        
        

    def on_fork_by_crunching_menu_item(self, event):
        '''Event handler for "Fork by crunching" menu item.'''
        self.fork_by_crunching()
        
        
    def on_fork_by_editing_menu_item(self, event):
        '''Event handler for "Fork by editing" menu item.'''
        self.fork_by_editing()

        
    def set_path(self, path):
        '''Set the path to `path`.'''
        self.path = path
        self.path_changed_emitter.emit()
        
        
    def set_official_playing_speed(self, value):
        '''Set the official playing speed.'''
        self.official_playing_speed = value
        self.official_playing_speed_modified_emitter.emit()

        
    def _set_pseudoclock(self, value):
        '''Set the pseudoclock. Internal use.'''
        if self.pseudoclock != value:
            self.pseudoclock = value
            self.pseudoclock_modified_emitter.emit()

            
    def set_pseudoclock(self, desired_pseudoclock,
                        rounding=binary_search.LOW_OTHERWISE_HIGH):
        '''
        Attempt to set the pseudoclock to a desired value.
        
        If value is outside the range of the current path, you'll get the clock
        of the closest edge node.
        
        The active node will be changed to one which is close to the
        `desired_pseudoclock`. In `rounding` use
        `binary_search.LOW_OTHERWISE_HIGH` to get the node just below, or
        `binary_search.HIGH_OTHERWISE_LOW` to get the node just above.
        
        See documentation for these two options for more details.
        '''
        # todo: check that everything that should use this does use this

        assert rounding in (binary_search.LOW_OTHERWISE_HIGH,
                            binary_search.HIGH_OTHERWISE_LOW)
        
        both_nodes = self.path.get_node_by_clock(desired_pseudoclock,
                                                 rounding=binary_search.BOTH)
        
        binary_search_profile = binary_search.BinarySearchProfile(
            self.path, 
            lambda node: node.state.clock,
            desired_pseudoclock,
            both_nodes
        )
        
        node = binary_search_profile.results[rounding]
        
        if node is None:
            return # todo: Not sure if I should raise something
        
        self._set_active_node(node)
        
        if binary_search_profile.is_surrounded:
            self._set_pseudoclock(desired_pseudoclock)
        else:
            self._set_pseudoclock(node.state.clock)
        
        self.project.ensure_buffer(node, clock_buffer=self.default_buffer)

        
    def set_default_buffer(self, default_buffer):
        '''Set the default buffer, saying how far we should crunch ahead.'''
        self.default_buffer = default_buffer
        if self.active_node:
            self.project.ensure_buffer(self.active_node,
                                       clock_buffer=self.default_buffer)
        self.default_buffer_modified_emitter.emit()
    
        
    def round_pseudoclock_to_active_node(self):
        '''Set the value of the pseudoclock to the clock of the active node.'''
        self._set_pseudoclock(self.active_node.state.clock)

        
    def update_defacto_playing_speed(self):
        '''Update the defacto playing speed to the official playing speed.'''
        # In the future this will check if someone's temporarily tweaking the
        # defacto speed, and let that override.
        self.defacto_playing_speed = self.official_playing_speed
        
    
    def make_state_creation_dialog(self):
        '''Create a dialog for creating a root state.'''
        Dialog = self.simpack_wx_grokker.settings.STATE_CREATION_DIALOG
        dialog = Dialog(self.frame)
        try:
            state = dialog.start()
        finally:
            dialog.Destroy()
        if state:
            root = self.project.root_this_state(state)
            self.tree_structure_modified_not_on_path_emitter.emit()
            self.set_active_node(root)
        self.frame.SetFocus()
        

    def get_active_state(self):
        '''Get the active state, i.e. the state of the active node.'''
        return self.active_node.state if self.active_node else None

    
    def get_active_step_profile(self):
        '''Get the active step profile, i.e. step profile of active node.'''
        return self.active_node.step_profile if self.active_node else None
                
    
    def _set_active_node(self, node):
        '''Set the active node, displaying it onscreen. Internal use.'''
        if self.active_node is not node:
            self.active_node = node
            self.active_node_changed_emitter.emit()

     
    def set_active_node(self, node, modify_path=True):
        '''
        Set the active node, displaying it onscreen.
        
        This will change the pseudoclock to the clock of the node.
        
        if `modify_path` is True, the method will modify the path to go through
        the node, if it doesn't already.        
        '''
        self.project.ensure_buffer(node, clock_buffer=self.default_buffer)
        
        if self.active_node is node:
            return
        
        was_playing = self.is_playing # todo: consider cancelling this
        if self.is_playing: self.stop_playing()
        
        self._set_active_node(node)

        self._set_pseudoclock(node.state.clock)
        
        if was_playing:
            self.start_playing()
        if modify_path:
            self.__modify_path_to_include_active_node()
            
        if modify_path and was_playing:
            if self.infinity_job:
                self.infinity_job.crunching_profile.clock_target = \
                    self.infinity_job.node.state.clock + self.default_buffer
                self.infinity_job = \
                    self.project.ensure_buffer_on_path(node,
                                                       self.path,
                                                       infinity)   
        
        
    def __modify_path_to_include_active_node(self):
        '''Ensure that `.path` includes the active node.'''
        if self.path is None:
            self.set_path(self.active_node.make_containing_path())
        else:
            self.path.modify_to_include_node(self.active_node)
            
        self.path_changed_emitter.emit()


    def start_playing(self):
        '''Start playback of the simulation.'''
        if self.is_playing:
            return
        if self.active_node is None:
            return

        self.is_playing = True
        
        
        self.infinity_job = \
            self.project.ensure_buffer_on_path(self.active_node, self.path,
                                               infinity)
        
        self.timer_for_playing.Start(1000//25)
        
        assert self.last_tracked_real_time == None
        self.round_pseudoclock_to_active_node()
        self.last_tracked_real_time = time.time()        
        self.playing_started_emitter.emit()
        
        # todo: maybe should start a call of __play_next right here, to save
        # 25ms delay on the first frame?
        


    def stop_playing(self):
        '''Stop playback of the simulation.'''
        
        if self.is_playing is False:
            return

        try:
            self.timer_for_playing.Stop()
        except Exception: # todo: Find out the type
            pass
        
        self.is_playing = False
        
        if self.infinity_job:
            self.infinity_job.crunching_profile.clock_target = \
                self.infinity_job.node.state.clock + self.default_buffer
        
        self.last_tracked_real_time = None
        self.round_pseudoclock_to_active_node()
        self.project.ensure_buffer(self.active_node, self.default_buffer)
        
        self.playing_stopped_emitter.emit()


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
            new_node = self.fork_by_editing()
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
        real_time_elapsed = (current_real_time - self.last_tracked_real_time)
        desired_pseudoclock = \
            self.pseudoclock + \
            (real_time_elapsed * self.defacto_playing_speed)
        

        rounding = binary_search.LOW_OTHERWISE_HIGH \
                 if self.defacto_playing_speed > 0 \
                 else binary_search.HIGH_OTHERWISE_LOW
        
        self.set_pseudoclock(desired_pseudoclock, rounding)

        self.last_tracked_real_time = current_real_time
        

    def fork_by_crunching(self, *args, **kwargs):
        '''
        Fork the simulation from the active node.
        
        Used for forking the simulation without modifying any states. Creates
        a new node from the active node via natural simulation.

        Any `*args` or `**kwargs` will be packed in a `StepProfile` object and
        passed to the step function. You may pass a `StepProfile` yourself, as
        the only argument, and it will be noticed and used. If nothing is
        passed in `*args` or `**kwargs`, the step profile of the active node
        will be used, unless it doesn't have a step profile, in which case the
        default step profile will be used.
        
        Returns the job.
        '''
        #todo: maybe not let to do it from unfinalized touched node?
        
        if not args and not kwargs and self.active_node.step_profile:
            step_profile = self.active_node.step_profile
        elif args or kwargs:
            parse_arguments_to_step_profile = \
                garlicsim.misc.StepProfile.build_parser(
                    self.active_node.step_profile.step_function if
                    self.active_node.step_profile else
                    self.simpack_grokker.default_step_function
                )
            step_profile = parse_arguments_to_step_profile(*args, **kwargs)
        else:
            assert not self.active_node.step_profile
            step_profile = self.default_step_profile
            
        job = self.project.begin_crunching(self.active_node,
                                           self.default_buffer or 1,
                                           step_profile)
        
        self._job_and_node_of_recent_fork_by_crunching = (job,
                                                          self.active_node)
        
        return job


    def fork_by_editing(self):
        '''
        Fork the simulation from the active node by editing.
        
        Returns the new node.
        '''
        # todo: event argument is bad, in other places too
        # todo: maybe not restrict it to "from_active_node"?
        new_node = \
            self.project.tree.fork_to_edit(template_node=self.active_node)
        self.tree_structure_modified_on_path_emitter.emit()
        self.set_active_node(new_node)
        return new_node


    def sync_crunchers(self):
        '''
        Take work from the crunchers, and give them new instructions if needed.
        
        (This is a wrapper for `Project.sync_crunchers()` with some gui-related
        additions.)
        
        Talks with all the crunchers, takes work from them for implementing
        into the tree, retiring crunchers or recruiting new crunchers as
        necessary.

        Returns the total amount of nodes that were added to the tree in the
        process.
        '''
        
        # This method basically has two tasks. The first one is to take work
        # from the crunchers and retire/recruit/redirect them as necessary.
        # This is done by `Project.sync_crunchers`, which we call here, so
        # that's not the tricky part here.
        #
        # The second task is the tricky part. We want to know just how much the
        # tree was modified during this action. And the tricky thing is that
        # `Project.sync_crunchers` won't do that for us, so we're going to have
        # to try to deduce how much the tree modified ourselves, just by
        # looking at the `jobs` list before and after calling
        # `Project.sync_crunchers`.
        #
        # And when I say "to know how much the tree modified", I mean mainly to
        # know if the modification is a structural modification, or just some
        # blocks getting fatter. And the reason we want to know this is so
        # we'll know whether to update various workspace widgets.
        
        jobs = self.project.crunching_manager.jobs
        
        jobs_to_nodes = dict((job, job.node) for job in jobs)

                
        added_nodes = self.project.sync_crunchers()        
        # This is the heavy line here, which actually executes the Project's
        # `sync_crunchers` function.
        
        
        if any(
            (job not in jobs) or \
            (job.node.soft_get_block() is not old_node.soft_get_block())
            for job, old_node in jobs_to_nodes.iteritems()
               ):

            # What does this codition mean?
            # 
            # It means that there is at least one job that either:
            # (a) Was removed from the jobs list, or
            # (b) Changed the soft block it's pointing to.            
            #
            # The thing is, if there was a structural modification in the tree,
            # this condition must be `True`. So we report a structure
            # modification:
            
            self.tree_structure_modified_at_unknown_location_emitter.emit()
            
            # Even though we are not sure that the tree structure was modified.
            # We have to play it safe. And since this condition doesn't happen
            # most of the time when crunching, we're not wasting too much
            # rendering time by assuming this is a structural modification.
            
            # Note that we didn't check if `added_nodes > 0`: This is because
            # if an `End` was added to the tree, it wouldn't have been counted
            # in `added_nodes`.
            
        elif added_nodes > 0:
            
            # If this condition is `True`, we know as a fact that there was no
            # structural modification, and we know as a fact that some blocks
            # have gotten fatter.
            
            self.tree_modified_at_unknown_location_emitter.emit()
            
        # todo: It would be hard but nice to know whether the tree changes were
        # on the path. This could save some rendering on `SeekBar`.
            
        return added_nodes

    
    def finalize_active_node(self):
        '''Finalize the changes made to the active node.'''
        self.active_node.finalize()
        
        self.active_node_finalized_emitter.emit()
        
        self.project.ensure_buffer(self.active_node, self.default_buffer)
        
    
    def _update_step_profiles_set(self):
        '''Update the step profiles set to include ones used in the tree.'''
        self.step_profiles |= self.project.tree.get_step_profiles()
    
    
    def __check_if_step_profile_changed(self):
        '''Check if the active step profile has changed.'''
        active_step_profile = self.get_active_step_profile()
        if active_step_profile != self._tracked_step_profile:
            self._tracked_step_profile = active_step_profile
            self.active_step_profile_changed_emitter.emit()
        
        
    def _if_forked_by_crunching_recently_switch_to_new_path(self):
        '''If user did "fork by crunching" and new path is ready, switch to.'''
        if self._job_and_node_of_recent_fork_by_crunching:
            job, old_node = self._job_and_node_of_recent_fork_by_crunching
            new_node = job.node
            
            if new_node is not old_node:
                new_path = new_node.make_containing_path()
                
                assert old_node in new_path
                # Cause `new_node` was born out of `old_node`.
                
                self.set_path(new_path)
                self._job_and_node_of_recent_fork_by_crunching = None
            
        
    def __reduce__(self):
        my_dict = dict(self.__dict__)
        
        del my_dict['frame']
        del my_dict['timer_for_playing']
        del my_dict['simpack_grokker']
        del my_dict['simpack_wx_grokker']
        
        # Getting rid of emitter:
        del my_dict['step_profiles']
        my_dict['step_profiles'] = list(self.step_profiles)
        
        # Getting rid of emitter and default factory:
        del my_dict['step_profiles_to_hues']
        my_dict['step_profiles_to_hues'] = dict(self.step_profiles_to_hues)
        
        if self.frame.shell:
            my_dict['_temp_shell_history'] = self.frame.shell.GetText()
            my_dict['_temp_shell_command_history'] = \
                self.frame.shell.history[:]
        
        my_namespace = my_dict['namespace'] = my_dict['namespace'].copy()
        try:
            del my_namespace['__builtins__']
        except KeyError:
            pass
        

        for (key, value) in my_dict.items():
            
            if isinstance(value, emitters.Emitter) or \
               isinstance(value, emitters.EmitterSystem):
                
                del my_dict[key]
            
        return (
            GuiProject._reconstruct,
            (self.simpack, self.project),
            my_dict
        )

    
    def __setstate__(self, my_dict):
        isinstance(my_dict, dict)
        
        if 'step_profiles' in my_dict:
            self.step_profiles.clear()
            self.step_profiles |= my_dict.pop('step_profiles')
            # todo: Last line not idiomatic
            
        if 'step_profiles_to_hues' in my_dict:
            self.step_profiles_to_hues.clear()
            self.step_profiles_to_hues.update(
                my_dict.pop('step_profiles_to_hues')
            )
            
        if 'namespace' in my_dict:
            pickled_namespace = my_dict.pop('namespace')
            pickled_namespace.update(self.namespace)
            self.namespace.update(pickled_namespace)
        
        for (key, value) in my_dict.iteritems():
            setattr(self, key, value)
    
    
    @staticmethod
    def _reconstruct(simpack, project):
        '''Reconstruct a pickled gui project.'''

        frame = garlicsim_wx._active_frame
        # todo: Make Frame inherit from some "InstanceHolder" instead
        
        gui_project = GuiProject(simpack, frame, project)
        
        return gui_project
    
    
_reconstruct = GuiProject._reconstruct
# Anchored because static methods cannot be pickled, because they are
# desciptors which return a function and (c)pickle sucks at functions defined
# in classes.

