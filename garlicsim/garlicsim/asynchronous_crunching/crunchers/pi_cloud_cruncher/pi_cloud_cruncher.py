# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.



import cloud
import copy
import Queue
import sys
import os

import garlicsim
from garlicsim.asynchronous_crunching import \
     BaseCruncher, CrunchingProfile, ObsoleteCruncherError


__all__ = ['PiCloudCruncher']    

        
class PiCloudCruncher(BaseCruncher):
    
    def __init__(self, crunching_manager, initial_state, crunching_profile):
        
        BaseCruncher.__init__(self, crunching_manager,
                              initial_state, crunching_profile)
        
        
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
        
        
    