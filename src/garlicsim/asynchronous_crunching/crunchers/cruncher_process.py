# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
This module defines the CruncherProcess class. See its documentation for
more information.
"""

import multiprocessing
import copy
import Queue as queue

import garlicsim
from garlicsim.asynchronous_crunching import \
     CrunchingProfile, ObsoleteCruncherError
try: import garlicsim.general_misc.process_priority as process_priority
except: pass

__all__ = ["CruncherProcess"]

class CruncherProcess(multiprocessing.Process):
    """
    CruncherProcess is a type of cruncher.
    
    A cruncher is a worker which crunches the simulation. It receives a state
    from the main program, and then it repeatedly applies the step function of
    the simulation to produce more states. Those states are then put in the
    cruncher's work_queue. They are then taken by the main program when
    Project.sync_crunchers is called, and put into the tree.
        
    Read more about crunchers in the documentation of the crunchers package.
    
    The advantage of CruncherProcess over CruncherThread is that
    CruncherProcess is able to run on a different core of the processor
    in the machine, thus using the full power of the processor.
    """
    def __init__(self, initial_state, step_generator,
                 crunching_profile):
        
        multiprocessing.Process.__init__(self)
        
        self.step_generator = step_generator
        self.initial_state = initial_state
        self.last_clock = self.initial_state.clock
        self.crunching_profile = copy.deepcopy(crunching_profile)
        
        self.daemon = True

        self.work_queue = multiprocessing.Queue()
        """
        The cruncher puts the work that it has completed into this queue, to be
        picked up by sync_crunchers.
        """
        
        self.order_queue = multiprocessing.Queue()
        """
        This queue is used to send instructions to the cruncher.
        """
        

    def set_priority(self,priority):
        """
        Set the priority of this process: Currently Windows only.
        """
        assert priority in [0, 1, 2, 3, 4, 5]
        try:
            process_priority.set_process_priority(self.pid, priority)
        except: #Not sure what to "except" here; wary of non-windows systems.
            pass

    def run(self):
        """
        This is called when the cruncher is started. It just calls the
        main_loop method in a try clause, excepting ObsoleteCruncherError;
        That exception means that the cruncher has been retired in the middle
        of its job, so it is propagated up to this level, where it causes the
        cruncher to terminate.
        """
        try:
            self.main_loop()
        except ObsoleteCruncherError:
            return

    def main_loop(self):
        """
        The main loop of the cruncher.
        
        Crunches the simulations repeatedly until the crunching profile is
        satisfied or a 'retire' order is received.
        """
        self.set_priority(0)
        
        step_options_profile = self.crunching_profile.step_options_profile or \
                          garlicsim.misc.StepOptionsProfile()
        
        self.step_iterator = \
            self.step_generator(self.initial_state,
                                *step_options_profile.args,
                                **step_options_profile.kwargs)
        order = None
        
        for state in self.step_iterator:
            self.auto_clock(state)
            self.work_queue.put(state)
            self.check_crunching_profile(state)
            order = self.get_order()
            if order:
                self.process_order(order)
    
             
    def auto_clock(self, state):
        """
        If the state lacks a clock attribute, set one up automatically.
        
        The new clock attribute will be equal to the clock of the old state
        plus 1.
        """
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
        """
        Attempt to read an order from the order_queue, if one has been sent.
        
        Returns the order.
        """
        try:
            return self.order_queue.get(block=False)
        except queue.Empty:
            return None
    
    def process_order(self, order):
        """
        Process an order receieved from order_queue.
        """
        if order=="retire":
            raise ObsoleteCruncherError
        elif isinstance(order, CrunchingProfile):
            self.crunching_profile = order

    def retire(self):
        """
        Retire the cruncher. Process-safe.
        
        Cause it to shut down as soon as it receives the order.
        """
        self.order_queue.put("retire")
        
    def update_crunching_profile(self, profile):
        """
        Update the cruncher's crunching profile. Process-safe.
        """
        self.order_queue.put(profile)
