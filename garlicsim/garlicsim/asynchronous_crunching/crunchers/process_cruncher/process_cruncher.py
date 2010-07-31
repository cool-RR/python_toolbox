# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the ProcessCruncher class.

See its documentation for more information.

This module requires the multiprocessing package to be installed. It is part of
the standard library for Python 2.6 and above, but not for earlier versions.
Backports of it for Python 2.4 and 2.5 are available on the internet.
'''

import multiprocessing
import copy
import Queue
import sys
import os

import garlicsim
from garlicsim.asynchronous_crunching import \
     BaseCruncher, CrunchingProfile, ObsoleteCruncherError

from .process import Process

__all__ = ['ProcessCruncher']    

        
class ProcessCruncher(BaseCruncher):
    '''
    ProcessCruncher is a type of cruncher the works from a process.
    
    A cruncher is a worker which crunches the simulation. It receives a state
    from the main program, and then it repeatedly applies the step function of
    the simulation to produce more states. Those states are then put in the
    cruncher's work_queue. They are then taken by the main program when
    Project.sync_crunchers is called, and put into the tree.
        
    Read more about crunchers in the documentation of the crunchers package.
    
    The advantage of ProcessCruncher over ThreadCruncher is that
    ProcessCruncher is able to run on a different core of the processor
    in the machine, thus using the full power of the processor.
    '''
    
    def __init__(self, crunching_manager, initial_state, crunching_profile):
        
        BaseCruncher.__init__(self, crunching_manager,
                              initial_state, crunching_profile)
        
        self.process = Process(
            self.project.simpack_grokker.get_step_iterator,
            initial_state,
            crunching_profile
        )
        
        self.work_queue = self.process.work_queue
        '''
        Queue for putting completed work to be picked up by the main thread.
        
        In this queue the cruncher will put the states that it produces, in
        chronological order. If the cruncher is being given a new crunching
        profile which has a new and different step profile, the cruncher
        will put the new step profile in this queue in order to signal that
        from that point on, all states were crunched with that step profile.
        '''
        
        self.order_queue = self.process.order_queue
        '''Queue for receiving instructions from the main thread.'''
        
        
    def start(self):
        self.process.start()

            
    def retire(self):
        '''
        Retire the cruncher. Process-safe.
        
        Causes it to shut down as soon as it receives the order.
        '''
        self.order_queue.put("retire")
        
        
    def update_crunching_profile(self, profile):
        '''Update the cruncher's crunching profile. Process-safe.'''
        self.order_queue.put(profile)
        
        
    def is_alive(self):
        return self.process.is_alive()
        
        
    