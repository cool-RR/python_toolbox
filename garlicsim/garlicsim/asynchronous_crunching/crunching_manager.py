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
from garlicsim.general_misc import address_tools
from garlicsim.general_misc import cute_iter_tools

import garlicsim
import garlicsim.data_structures
import garlicsim.misc
import crunchers
from crunching_profile import CrunchingProfile
from garlicsim.misc.step_profile import StepProfile
from .misc import EndMarker


__all__ = ['CrunchingManager', 'DefaultCruncher', 'DefaultHistoryCruncher']


DefaultCruncher = crunchers.ProcessCruncher
'''Cruncher class to be used by default in non-history-dependent simulations.'''


DefaultHistoryCruncher = crunchers.ThreadCruncher
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
        
        This exists because if the step profile for a job changes, we need to
        retire the cruncher and make a new ones; Crunchers can't change step
        profiles on the fly. So we use this dict to track which step profile
        each cruncher uses.
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
        # This is one of the most technical and sensitive functions in all of
        # GarlicSim-land. Be careful if you're trying to make changes.

        total_added_nodes = garlicsim.misc.NodesAdded(0)
        '''int-oid in which we track the number of nodes added to the tree.'''
        
        # The first thing we do is iterate over the crunchers whose jobs have
        # been terminated. We take work from them, put it into the tree, and
        # promptly retire them, deleting them from `self.crunchers`.
        
        for (job, cruncher) in self.crunchers.copy().items():
            if not (job in self.jobs):
                (added_nodes, new_leaf) = \
                    self.__add_work_to_tree(cruncher, job, retire=True)
                total_added_nodes += added_nodes
                del self.crunchers[job]

                
        # In this point all the crunchers in `self.crunchers` have an active job
        # associated with them.
        #
        # Now we'll iterate over the active jobs.
        
        for job in self.jobs[:]:
            
            
            if job not in self.crunchers:
                
                # If there is no cruncher associated with the job, we create
                # one. (As long as the job is unfinished, and the node isn't in
                # editing.) And that's it for this job, we `continue` to the
                # next one.
                
                if not job.is_done():
                    self.__conditional_create_cruncher(job)
                else: # job.is_done() is True
                    self.jobs.remove(job)
                continue

            # job in self.crunchers
            #
            # Okay, so it's an active job with an active cruncher working on it.
            # We'll take work from the cruncher and put in the tree, updating
            # the job to point at `new_leaf`, which is the node (leaf)
            # containing the most recent state produced by the cruncher.
            
            cruncher = self.crunchers[job]
            
            (added_nodes, new_leaf) = self.__add_work_to_tree(cruncher,
                                                              job)
            total_added_nodes += added_nodes

            job.node = new_leaf
            
            # We took work from the cruncher, now it's time to decide if we want
            # the cruncher to keep running or not. We will also update its
            # crunching profile, if that has been changed on the job.
            
            if not job.is_done():
                
                crunching_profile = job.crunching_profile
                
                if cruncher.is_alive():
                    
                    # The job is not the done, and the cruncher's still working.
                    # In this case, the only thing left to do is check if the
                    # crunching profile changed.

                    # First we'll check if the step profile changed:
                    
                    if crunching_profile.step_profile != \
                       self.step_profiles[cruncher]:
                        
                        # If it did, we immediately replace the cruncher,
                        # because crunchers can't change step profile on the
                        # fly.
                        
                        if cruncher.is_alive():
                            cruncher.retire()
                        
                        self.__conditional_create_cruncher(job)
                        
                        continue
                    
                        
                    # At this point we know that the step profile hasn't
                    # changed, but possibly some other part (i.e. clock target)
                    # has changed, and if so we update the cruncher about it.
                        
                    if self.crunching_profiles_change_tracker.check_in \
                       (crunching_profile):
                        
                        cruncher.update_crunching_profile(crunching_profile)
                        
                        continue
                        
                else: # cruncher.is_alive() is False
                    
                    # Cruncher died; We'll create another:
                    
                    self.__conditional_create_cruncher(job)
                    
                    continue
                    
                    
            else: # job.is_done() is True
                
                # The job is done; We remove it from the job list, and retire
                # and delete the cruncher.
                
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
            cruncher = self.Cruncher(self, node.state, crunching_profile)
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
                   address_tools.get_address(type(self), shorten=True),
                   crunchers_count,
                   job_count,
                   hex(id(self))
               )
    
