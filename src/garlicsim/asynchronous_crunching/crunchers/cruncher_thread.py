# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
This module defines the CruncherThread class. See its documentation for
more information.
"""

import threading
import Queue as queue
import copy

import garlicsim
from garlicsim.asynchronous_crunching import \
     HistoryBrowser, ObsoleteCruncherError, CrunchingProfile

__all__ = ["CruncherThread"]

class CruncherThread(threading.Thread):
    """
    CruncherThread is a type of cruncher.
    
    A cruncher is a dumb little drone. It receives a state from the main
    program, and then it repeatedly applies the step funcion of the simulation
    to produce more states. Those states are then put in the cruncher's
    work_queue. They are then taken by the main program when
    Project.sync_crunchers is called, and put into the tree.
        
    Read more about crunchers in the documentation of the crunchers package.
    
    The advantage of CruncherThread over CruncherProcess is that
    CruncherThread is able to handle simulations that are history-dependent.
    """
    def __init__(self, initial_state, project, crunching_profile):
        threading.Thread.__init__(self)
        
        self.project = project
        self.crunching_profile = copy.deepcopy(crunching_profile)
        self.history_dependent = self.project.simpack_grokker.history_dependent
                
        self.initial_state = initial_state
        self.last_clock = initial_state.clock
        self.daemon = True

        self.work_queue = queue.Queue()
        """
        The cruncher puts the work that it has completed
        into this queue, to be picked up by sync_crunchers.
        """

        self.order_queue = queue.Queue()
        """
        This queue is used to send instructions
        to the cruncher.
        """

    def run(self):
        """
        This is called when the cruncher is started. It just calls
        the main_loop method in a try clause, excepting ObsoleteCruncherError;
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
        The main loop of the cruncher. It's basically, "As long as no one
        tells you to retire, apply the step function repeatedly and put the
        results in your work queue."
        """
        
        step_options_profile = self.crunching_profile.step_options_profile or \
                             garlicsim.misc.StepOptionsProfile()
        
        if self.history_dependent:
            self.history_browser = HistoryBrowser(cruncher=self)
            self.step_iterator = self.project.simpack_grokker.step_generator \
                             (self.history_browser, *step_options_profile.args,
                              **step_options_profile.kwargs)
        else:
            self.step_iterator = self.project.simpack_grokker.step_generator \
                              (self.initial_state, *step_options_profile.args,
                               **step_options_profile.kwargs) 
        
        order = None
        
        for state in self.step_iterator:
            self.autoclock(state)
            self.work_queue.put(state)
            self.check_crunching_profile(state)
            order = self.get_order()
            if order:
                self.process_order(order)

                
    def autoclock(self, state):
        if not hasattr(state, "clock"):
            state.clock = self.last_clock + 1
        self.last_clock = state.clock
        
    def check_crunching_profile(self, state):
        if self.crunching_profile.state_satisfies(state):
            raise ObsoleteCruncherError
        
    def get_order(self):
        """
        Attempts to read an order from the order_queue, if one has been sent.
        """
        try:
            return self.order_queue.get(block=False)
        except queue.Empty:
            return None
    
    def process_order(self, order):
        """
        Processes an order receieved from order_queue.
        """
        if order == "retire":
            raise ObsoleteCruncherError
        elif isinstance(order, CrunchingProfile):
            self.crunching_profile = copy.deepcopy(order)
    
    def retire(self):
        """
        Retire the cruncher. Thread-safe.
        
        TODORetiring the cruncher, causing it to shut down as soon as it receives
        the order. This method may be called either from within the thread or
        from another thread.
        """
        self.order_queue.put("retire")        
        
    def update_crunching_profile(self, profile):
        """
        Thread-safe TODO
        """
        self.order_queue.put(profile)
    

