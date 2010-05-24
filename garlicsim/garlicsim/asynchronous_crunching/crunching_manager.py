# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the CrunchingManager class. See its documentation for more
information.
'''

from __future__ import with_statement

import garlicsim.general_misc.queue_tools as queue_tools
import garlicsim.general_misc.third_party.decorator
import garlicsim.general_misc.change_tracker
from garlicsim.general_misc.infinity import Infinity
from garlicsim.general_misc import misc_tools
from garlicsim.general_misc import cute_iter_tools

import garlicsim
import garlicsim.data_structures
import garlicsim.misc
import crunchers
from crunching_profile import CrunchingProfile
from garlicsim.misc.step_profile import StepProfile
from .misc import EndMarker


__all__ = ['CrunchingManager', 'DefaultCruncher', 'DefaultHistoryCruncher']


DefaultCruncher = crunchers.CruncherThread
'''Cruncher class to be used by default in non-history-dependent simulations.'''


DefaultHistoryCruncher = crunchers.CruncherThread
'''Cruncher class to be used by default in history-dependent simulations.'''


@garlicsim.general_misc.third_party.decorator.decorator
def with_tree_lock(method, *args, **kwargs):
    '''
    Decorator for using the tree lock (in write mode) as a context manager.
    '''
    self = args[0]
    with self.project.tree.lock.write:
        return method(*args, **kwargs)


class CrunchingManager(object):
    '''
    A crunching manager manages the background crunching for a project.
    
    Every project creates a crunching manager. The job of the crunching manager
    is to coordinate the crunchers, creating and retiring them as necessary.
    The main use of a crunching manager is through its sync_workers methods,
    which goes over all the crunchers and all the nodes of the tree that need
    to be crunched, making sure the crunchers are working on these nodes, and
    collecting work from them to implement into the tree.
    
    The crunching manager contains a list of jobs as an attribute `.jobs`. See
    documentation for garlicsim.asynchronous_crunching.Job for more info about
    jobs. The crunching manager will employ crunchers in order to complete the
    jobs. It will then take work from these crunchers, put it into the tree,
    and delete the jobs when they are completed.
    '''
    def __init__(self, project):        
        self.project = project
        

        FORCE_CRUNCHER = project.simpack_grokker.settings.FORCE_CRUNCHER
        
        if FORCE_CRUNCHER is not None:
            self.Cruncher = FORCE_CRUNCHER
        else:
            history_dependent = project.simpack_grokker.history_dependent
            
            self.Cruncher = DefaultHistoryCruncher if history_dependent \
                            else DefaultCruncher
        
        self.jobs = []
        '''
        The jobs that the crunching manager will be responsible for doing.
        
        These are of the class garlicsim.asynchronous_crunching.Job.
        '''
        
        self.crunchers = {}
        '''Dict that maps each job to the cruncher reponsible for doing it.'''
        
        self.step_profiles = {}
        '''
        Dict that maps each cruncher to its step options profile.
        
        This exists because a cruncher might change its step options profile
        in the course of its work. When it does, it announces this by putting
        the profile in the work queue. In this dict we keep track of the last
        step options profile each cruncher was known to use.
        '''
        
        self.crunching_profiles_change_tracker = \
            garlicsim.general_misc.change_tracker.ChangeTracker()
        '''
        A change tracker which tracks changes made to crunching profiles.
        
        This is used to update the crunchers if the crunching profile for the
        job they're working on has changed.
        '''

        
    @with_tree_lock
    def sync_crunchers(self):
        '''
        Take work from the crunchers, and give them new instructions if needed.
        
        Talks with all the crunchers, takes work from them for implementing
        into the tree, retiring crunchers or recruiting new crunchers as
        necessary.

        Returns the total amount of nodes that were added to the tree in the
        process.
        '''
        total_added_nodes = garlicsim.misc.NodesAdded(0)

        
        for (job, cruncher) in self.crunchers.copy().items():
            if not (job in self.jobs):
                (added_nodes, new_leaf) = \
                    self.__add_work_to_tree(cruncher, job, retire=True)
                total_added_nodes += added_nodes
                del self.crunchers[job]


        for job in self.jobs[:]:
            
            
            if job not in self.crunchers:
                if not job.is_done():
                    self.__conditional_create_cruncher(job)
                else: # job.is_done() is True
                    self.jobs.remove(job)
                continue

            # job in self.crunchers
            
            cruncher = self.crunchers[job]
            
            (added_nodes, new_leaf) = self.__add_work_to_tree(cruncher,
                                                              job)
            total_added_nodes += added_nodes

            job.node = new_leaf
            
            if not job.is_done(): # (Need to call is_done again cause node changed)
                
                crunching_profile = job.crunching_profile
                
                if cruncher.is_alive():
                                        
                    if self.crunching_profiles_change_tracker.check_in \
                       (crunching_profile):
                        
                        cruncher.update_crunching_profile(crunching_profile)
                        
                else:
                    
                    self.__conditional_create_cruncher(job)
            else: # job.is_done() is True
                self.jobs.remove(job)
                if cruncher.is_alive():
                    cruncher.retire()
                del self.crunchers[job]
            
        return total_added_nodes

    
    def __conditional_create_cruncher(self, job):
        '''
        Create a cruncher to crunch the node, unless there is reason not to.
        '''
        node = job.node
        crunching_profile = job.crunching_profile
        
        if node.still_in_editing is False:
            step_function = self.project.simpack_grokker.step
            if self.Cruncher == getattr(crunchers, 'CruncherProcess', None):
                cruncher = self.Cruncher \
                         (node.state,
                          self.project.simpack_grokker.step_generator,
                          crunching_profile=crunching_profile)
            else: # self.Cruncher == crunchers.CruncherThread
                cruncher = self.Cruncher(node.state, self.project,
                                         crunching_profile=crunching_profile)
            cruncher.start()
            self.crunchers[job] = cruncher
            
            self.crunching_profiles_change_tracker.check_in(crunching_profile)
            self.step_profiles[cruncher] = \
                crunching_profile.step_profile
            
    
    def get_jobs_by_node(self, node):
        '''
        Get all the jobs that should be done on the specified Node.
        
        This is every job whose .node attribute is equal to the specified node.
        '''
        return [job for job in self.jobs if job.node == node]

    
    def __add_work_to_tree(self, cruncher, job, retire=False):
        '''
        Take work from cruncher and add to tree at the specified job's node.
        
        If `retire` is set to True, retires the cruncher. Keep in mind that if
        the cruncher gives an EndMarker, it will be retired regardless of the
        `retire` argument.
        
        Returns (number, leaf), where `number` is the number of nodes that were
        added, and `leaf` is the last node that was added.
        '''
        
        tree = self.project.tree
        node = job.node
        
        current = node
        counter = 0
        self.step_profiles[cruncher]
        
        for thing in queue_tools.iterate(cruncher.work_queue):
            
            if isinstance(thing, garlicsim.data_structures.State):
                counter += 1
                current = tree.add_state(
                    thing,
                    parent=current,
                    step_profile=self.step_profiles[cruncher],
                    
                )
                # todo optimization: save step profile in variable, it's
                # wasteful to do a dict lookup every state.
            
            elif isinstance(thing, EndMarker):
                tree.make_end(node=current,
                              step_profile=self.step_profiles[cruncher])
                job.resulted_in_end = True
                
                
            elif isinstance(thing, StepProfile):
                self.step_profiles[cruncher] = thing
            else:
                raise Exception('Unexpected object %s in work queue' % thing)
                        
        if retire or job.resulted_in_end:
            cruncher.retire()
        
        nodes_added = garlicsim.misc.NodesAdded(counter)

        return (nodes_added, current)
    
    def __repr__(self):
        '''
        Get a string representation of the crunching manager.
        
        Example output:
        <garlicsim.asynchronous_crunching.CrunchingManager
        currently employing 2 crunchers to handle 2 jobs at 0x1f699b0>
        '''
        
        crunchers_count = len(self.crunchers)
        job_count = len(self.jobs)
                                   
        return '<%s currently employing %s crunchers to handle %s jobs at %s>' % \
               (
                   misc_tools.shorten_class_address(
                       self.__class__.__module__,
                       self.__class__.__name__
                   ),
                   crunchers_count,
                   job_count,
                   hex(id(self))
               )
    
    
    
    
