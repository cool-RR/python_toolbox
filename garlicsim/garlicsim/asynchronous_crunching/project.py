# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the Project class. See its documentation for more
information.
'''

from __future__ import with_statement

from garlicsim.general_misc import cute_iter_tools
import garlicsim.general_misc.read_write_lock
from garlicsim.general_misc.infinity import Infinity
import garlicsim.general_misc.module_wrapper
import garlicsim.general_misc.third_party.decorator

import garlicsim.data_structures
import garlicsim.misc.simpack_grokker
import garlicsim.misc.step_profile

from crunching_manager import CrunchingManager
from job import Job
from crunching_profile import CrunchingProfile

__all__ = ["Project"]

@garlicsim.general_misc.third_party.decorator.decorator
def with_tree_lock(method, *args, **kwargs):
    '''
    A decorator used in Project's methods to use the tree lock (in write mode)
    as a context manager when calling the method.
    '''
    self = args[0]
    with self.tree_lock.write:
        return method(*args, **kwargs)


class Project(object):
    '''
    You create a project when you want to do a simulation which will crunch
    in the background with worker threads or worker processes.

    A project contains within it a tree.
        
    The crunching is taken care of by the CrunchingManager which is a part of
    every project. The CrunchingManager employs CruncherThreads and/or
    CruncherProcesses to get the work done. To make the CrunchingManager take
    work from the crunchers and coordinate them, call the sync_crunchers method
    of the project.
    
    The crunching manager contains a list of jobs as an attribute `.jobs`. See
    documentation for garlicsim.asynchronous_crunching.Job for more info about
    jobs. The crunching manager will employ crunchers in order to complete the
    jobs. It will then take work from these crunchers, put it into the tree,
    and delete the jobs when they are completed.
    '''

    def __init__(self, simpack):
        
        wrapped_simpack = \
            garlicsim.general_misc.module_wrapper.module_wrapper_factory \
            (simpack)
        
        self.simpack = wrapped_simpack
        
        self.simpack_grokker = \
            garlicsim.misc.simpack_grokker.SimpackGrokker(wrapped_simpack)        

        self.tree = garlicsim.data_structures.Tree()
        
        self.crunching_manager = CrunchingManager(self)
        
        self.tree_lock = garlicsim.general_misc.read_write_lock.ReadWriteLock()
        '''
        The tree_lock is a read-write lock that guards access to the tree.
        We need such a thing because some simulations are history-dependent
        and require reading from the tree in the same time that sync_crunchers
        could potentially be writing to it.
        '''

    def make_plain_root(self, *args, **kwargs):
        '''
        Create a parentless node whose state is a simple plain state.
        
        The simulation package has to define the function `make_plain_state`
        for this to work.
        
        Returns the node.
        '''
        state = self.simpack.make_plain_state(*args, **kwargs)
        return self.root_this_state(state)

    def make_random_root(self, *args, **kwargs):
        '''
        Creates a parentless node whose state is a random and messy state.
        
        The simulation package has to define the function `make_random_state`
        for this to work.
        
        Returns the node.
        '''
        state = self.simpack.make_random_state(*args, **kwargs)
        return self.root_this_state(state)

    def root_this_state(self, state):
        '''
        Take a state, wrap it in a node and add to the tree without a parent.
        
        Returns the node.
        '''
        return self.tree.add_state(state)

    def ensure_buffer(self, node, clock_buffer=0):
        '''
        Ensure there's a large enough buffer of nodes after `node`.

        This method will ensure that every path that starts at `node` will have
        a clock buffer of at least `clock_buffer` after `node`. If there isn't,
        the leaves of `node` will be crunched until there's a buffer of
        `clock_buffer` between `node` and each of the leaves.
        '''
        leaves_dict = node.get_all_leaves(max_clock_distance=clock_buffer)
        new_clock_target = node.state.clock + clock_buffer
        
        for item in leaves_dict.items():

            leaf = item[0]
            
            jobs_of_leaf = self.crunching_manager.get_jobs_by_node(leaf)
            
            if not jobs_of_leaf:
                step_profile = leaf.step_profile or garlicsim.misc.StepProfile()
                crunching_profile = CrunchingProfile(new_clock_target,
                                                     step_profile)
                job = Job(leaf, crunching_profile)
                self.crunching_manager.jobs.append(job)
                continue
            
            for job in jobs_of_leaf:
                job.crunching_profile.raise_clock_target(new_clock_target)
            
    
    def ensure_buffer_on_path(self, node, path, clock_buffer=0):
        '''
        Ensure there's a large enough buffer of nodes after `node` on `path`.

        This method will ensure that on the given path there will be a clock
        buffer of at least `clock_buffer` after `node`. If there isn't, the
        leaf at the end of the path will be crunched until the buffer is big
        enough.
        '''
        
        leaf = path.get_last_node(starting_at=node)
        new_clock_target = node.state.clock + clock_buffer     

        jobs_of_leaf = self.crunching_manager.get_jobs_by_node(leaf)
        
        if jobs_of_leaf:
            job = jobs_of_leaf[-1]
            # We only want to take one job. We're guessing the last, and 
            # therefore the most recent one, will be the most wanted by the
            # user.
            job.crunching_profile.raise_clock_target(new_clock_target)
            return job
        else:
            step_profile = leaf.step_profile or garlicsim.misc.StepProfile()
            crunching_profile = CrunchingProfile(new_clock_target,
                                                 step_profile)
            job = Job(leaf, crunching_profile)
            self.crunching_manager.jobs.append(job)
            return job
          
    
    def begin_crunching(self, node, clock_buffer=None, *args, **kwargs):
        '''
        Start a new crunching job from `node`, possibly forking the simulation.
        
        On the next call to .sync_crunchers, a cruncher will start working on
        the new job.
        If there are already jobs on that node, they will all be crunched
        independently of each other to create different forks.
        Any args or kwargs will be packed in a StepProfile object and
        passed to the step function. You may pass a StepProfile
        yourself, as the only argument, and it will be noticed and used.
        
        Returns the job.
        '''
        
        step_profile = garlicsim.misc.StepProfile(*args, **kwargs)
        
        clock_target = node.state.clock + clock_buffer
        
        crunching_profile = CrunchingProfile(clock_target, step_profile)
        
        job = Job(node, crunching_profile)
        
        return self.crunching_manager.jobs.append(job)
    

    def sync_crunchers(self):
        '''
        Take work from the crunchers, and give them new instructions if needed.
        
        Talks with all the crunchers, takes work from them for implementing
        into the tree, retiring crunchers or recruiting new crunchers as
        necessary.

        Returns the total amount of nodes that were added to the tree in the
        process.
        '''        
        return self.crunching_manager.sync_crunchers()
    
    @with_tree_lock
    def simulate(self, node, iterations=1, *args, **kwargs):
        '''
        Simulate from the given node for the given number of iterations.
        
        The results are implemented the results into the tree. Note that the
        crunching for this is done synchronously, i.e. in the currrent thread.
        
        Any extraneous parameters will be passed to the step function.
        
        Returns the final node.
        '''
        # todo: is simulate a good name? Need to say it's synchronously
        
        step_profile = garlicsim.misc.StepProfile(*args, **kwargs)
        
        if self.simpack_grokker.history_dependent:
            return self.__history_dependent_simulate(node, iterations,
                                                     step_profile)
        else:
            return self.__non_history_dependent_simulate(node, iterations,
                                                         step_profile)
        
    @with_tree_lock        
    def __history_dependent_simulate(self, node, iterations,
                                     step_profile=None):
        '''
        For history-dependent simulations only:
        
        Simulate from the given node for the given number of iterations.
        
        The results are implemented the results into the tree. Note that the
        crunching for this is done synchronously, i.e. in the currrent thread.
        
        A step profile may be passed to be used with the step function.
        
        Returns the final node.
        '''
        
        if step_profile is None: step_profile = garlicsim.misc.StepProfile()
        
        path = node.make_containing_path()
        history_browser = \
            garlicsim.synchronous_crunching.HistoryBrowser(path, end_node=node)
        
        iterator = self.simpack_grokker.step_generator(history_browser,
                                                       step_profile)
        finite_iterator = cute_iter_tools.shorten(iterator, iterations)
        
        current_node = node
        for current_state in finite_iterator:
            current_node = self.tree.add_state(current_state,
                                               parent=current_node,
                                               step_profile=step_profile)
            history_browser.end_node = current_node
            
        return current_node
    
    @with_tree_lock
    def __non_history_dependent_simulate(self, node, iterations,
                                         step_profile=None):
        '''
        For non-history-dependent simulations only:
        
        Simulate from the given node for the given number of iterations.
        
        The results are implemented the results into the tree. Note that the
        crunching for this is done synchronously, i.e. in the currrent thread.
        
        A step profile may be passed to be used with the step function.
        
        Returns the final node.
        '''
        
        if step_profile is None: step_profile = garlicsim.misc.StepProfile()

        state = node.state
                
        iterator = self.simpack_grokker.step_generator(state, step_profile)
        finite_iterator = cute_iter_tools.shorten(iterator, iterations)
        
        current_node = node
        
        for current_state in finite_iterator:
            current_node = self.tree.add_state(current_state,
                                               parent=current_node,
                                               step_profile=step_profile)
            
        return current_node
    
    def __getstate__(self):
        my_dict = dict(self.__dict__)
        
        del my_dict['tree_lock']
        del my_dict['crunching_manager']
        del my_dict['simpack_grokker']
        
        return my_dict
    
    def __setstate__(self, pickled_project):
        self.__init__(pickled_project["simpack"])
        self.__dict__.update(pickled_project)
        
    def __repr__(self):
        '''
        Get a string representation of the project.
        
        Example output:
        <garlicsim.asynchronous_crunching.project.Project containing 101 nodes
        and employing 4 crunchers at 0x1f668d0>
        '''
        # Todo: better have the simpack mentioned here, not doing it cause it's
        # currently in a module wrapper.
        
        nodes_count = len(self.tree.nodes)
        crunchers_count = len(self.crunching_manager.crunchers)
                                   
        return '''<%s.%s containing %s nodes and employing %s crunchers at \
%s>''' % \
               (
                   self.__class__.__module__,
                   self.__class__.__name__,
                   nodes_count,
                   crunchers_count,
                   hex(id(self))
               )
        
        
        
        
        
        