# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.


import multiprocessing
import copy
import Queue
import sys
import os

try: import garlicsim.general_misc.process_priority
except Exception: pass

import garlicsim
from garlicsim.asynchronous_crunching import \
     BaseCruncher, CrunchingProfile, ObsoleteCruncherError


class Process(multiprocessing.Process):
    def __init__(self, step_iterator_getter, initial_state, crunching_profile):
        
        multiprocessing.Process.__init__(self)
        
        self.step_iterator_getter = step_iterator_getter
        self.initial_state = initial_state
        self.last_clock = self.initial_state.clock
        self.crunching_profile = crunching_profile
        
        self.daemon = True

        self.work_queue = multiprocessing.Queue()
        '''
        Queue for putting completed work to be picked up by the main thread.
        
        In this queue the cruncher will put the states that it produces, in
        chronological order. If the cruncher is being given a new crunching
        profile which has a new and different step profile, the cruncher
        will put the new step profile in this queue in order to signal that
        from that point on, all states were crunched with that step profile.
        '''
        
        self.order_queue = multiprocessing.Queue()
        '''Queue for receiving instructions from the main thread.'''
    
        
    def set_low_priority(self):
        '''Set a low priority for this process.'''
        
        try:
            sys.getwindowsversion()
        except Exception:
            is_windows = False
        else:
            is_windows = True

        if is_windows:
            try:
                garlicsim.general_misc.process_priority.set_process_priority(0)
            except Exception:
                pass
        else:
            try:
                os.nice(1)
            except Exception:
                pass

    def run(self):
        '''
        Internal method.
        
        This is called when the cruncher is started. It just calls the
        main_loop method in a try clause, excepting ObsoleteCruncherError;
        That exception means that the cruncher has been retired in the middle
        of its job, so it is propagated up to this level, where it causes the
        cruncher to terminate.
        '''
        try:
            self.main_loop()
        except ObsoleteCruncherError as e:
            return

        
    def main_loop(self):
        '''
        The main loop of the cruncher.
        
        Crunches the simulations repeatedly until the crunching profile is
        satisfied or a 'retire' order is received.
        '''
        self.set_low_priority()
        
        state = self.initial_state
        
        self.step_profile = self.crunching_profile.step_profile
        
        self.iterator = self.step_iterator_getter(self.initial_state,
                                                  self.step_profile)
        
        order = None
        
        try:
            for state in self.iterator:
                self.work_queue.put(state)
                self.check_crunching_profile(state)
                order = self.get_order()
                if order:
                    self.process_order(order) 
        except garlicsim.misc.WorldEnd:
            self.work_queue.put(garlicsim.asynchronous_crunching.misc.EndMarker())            

            
    def check_crunching_profile(self, state):
        '''
        Check if the cruncher crunched enough states. If so retire.
        
        The crunching manager specifies how much the cruncher should crunch.
        We consult with it to check if the cruncher has finished, and if it did
        we retire the cruncher.
        '''
        if self.crunching_profile.state_satisfies(state):
            raise ObsoleteCruncherError("We're done working, the clock target "
                                        "has been reached. Shutting down.")
    
        
    def get_order(self):
        '''
        Attempt to read an order from the order_queue, if one has been sent.
        
        Returns the order.
        '''
        try:
            return self.order_queue.get(block=False)
        except Queue.Empty:
            return None
    
        
    def process_order(self, order):
        '''Process an order receieved from order_queue.'''
        
        if order == 'retire':
            raise ObsoleteCruncherError("Cruncher received a 'retire' order; "
                                        "Shutting down.")
        
        elif isinstance(order, CrunchingProfile):
            self.process_crunching_profile_order(order)
            
            
            
    def process_crunching_profile_order(self, order):
        '''Process an order to update the crunching profile.'''
        if self.crunching_profile.step_profile != order.step_profile:
            raise ObsoleteCruncherError('Step profile changed; Shutting down. '
                                        'Crunching manager should create a '
                                        'new cruncher.')
        self.crunching_profile = order
