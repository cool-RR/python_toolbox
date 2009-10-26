# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the CruncherThread class. See its documentation for
more information.
'''

import threading
import Queue
import copy

import garlicsim
from garlicsim.asynchronous_crunching import \
     HistoryBrowser, ObsoleteCruncherError, CrunchingProfile

__all__ = ["CruncherThread"]

class CruncherThread(threading.Thread):
    '''
    CruncherThread is a type of cruncher.
    
    A cruncher is a worker which crunches the simulation. It receives a state
    from the main program, and then it repeatedly applies the step function of
    the simulation to produce more states. Those states are then put in the
    cruncher's work_queue. They are then taken by the main program when
    Project.sync_crunchers is called, and put into the tree.
        
    Read more about crunchers in the documentation of the crunchers package.
    
    The advantage of CruncherThread over CruncherProcess is that
    CruncherThread is able to handle simulations that are history-dependent.
    '''
    def __init__(self, initial_state, project, crunching_profile):
        threading.Thread.__init__(self)
        
        self.project = project
        self.step_generator = project.simpack_grokker.step_generator
        self.crunching_profile = copy.deepcopy(crunching_profile)
        self.history_dependent = self.project.simpack_grokker.history_dependent
        
        self.initial_state = initial_state
        self.last_clock = initial_state.clock
        
        self.daemon = True

        self.work_queue = Queue.Queue()
        '''
        Queue for putting completed work to be picked up by the main thread.
        '''

        self.order_queue = Queue.Queue()
        '''
        Queue for receiving instructions from the main thread.
        '''

        
    def run(self):
        '''
        This is called when the cruncher is started. It just calls
        the main_loop method in a try clause, excepting ObsoleteCruncherError;
        That exception means that the cruncher has been retired in the middle
        of its job, so it is propagated up to this level, where it causes the
        cruncher to terminate.
        '''
        try:
            self.main_loop()
        except ObsoleteCruncherError:
            return

    def main_loop(self):
        '''
        The main loop of the cruncher.
        
        Crunches the simulations repeatedly until the crunching profile is
        satisfied or a 'retire' order is received.
        '''
        
        step_profile = self.crunching_profile.step_profile or \
                             garlicsim.misc.StepProfile()
        
        if self.history_dependent:
            self.history_browser = HistoryBrowser(cruncher=self)
            thing = self.history_browser
        else:
            thing = self.initial_state
            
        self.step_iterator = self.step_generator(thing,
                                                 *step_profile.args,
                                                 **step_profile.kwargs)
        
        order = None
        
        for state in self.step_iterator:
            self.auto_clock(state)
            self.work_queue.put(state)
            self.check_crunching_profile(state)
            order = self.get_order()
            if order:
                self.process_order(order)

                
    def auto_clock(self, state):
        '''
        If the state lacks a clock attribute, set one up automatically.
        
        The new clock attribute will be equal to the clock of the old state
        plus 1.
        '''
        if not hasattr(state, "clock"):
            state.clock = self.last_clock + 1
        self.last_clock = state.clock
        
    def check_crunching_profile(self, state):
        '''
        Check if the cruncher crunched enough states. If so retire.
        
        The crunching manager specifies how much the cruncher should crunch.
        We consult with it to check if the cruncher has finished, and if it did
        we retire the cruncher.
        '''
        if self.crunching_profile.state_satisfies(state):
            raise ObsoleteCruncherError
        
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
        '''
        Process an order receieved from order_queue.
        '''
        if order == "retire":
            raise ObsoleteCruncherError
        elif isinstance(order, CrunchingProfile):
            self.crunching_profile = copy.deepcopy(order)
    
    def retire(self):
        '''
        Retire the cruncher. Thread-safe.
        
        Cause it to shut down as soon as it receives the order.
        '''
        self.order_queue.put("retire")        
        
    def update_crunching_profile(self, profile):
        '''
        Update the cruncher's crunching profile. Thread-safe.
        '''
        self.order_queue.put(profile)
    

