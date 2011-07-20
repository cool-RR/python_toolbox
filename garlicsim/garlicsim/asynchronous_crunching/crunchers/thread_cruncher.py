# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the `ThreadCruncher` class.

See its documentation for more information.
'''

import threading
import Queue
import copy

from garlicsim.general_misc import string_tools

import garlicsim
from garlicsim.asynchronous_crunching import \
     BaseCruncher, HistoryBrowser, ObsoleteCruncherException, CrunchingProfile


__all__ = ['ThreadCruncher']


class ThreadCruncher(threading.Thread, BaseCruncher):
    '''
    ThreadCruncher is cruncher that works from a thread.
    
    A cruncher is a worker which crunches the simulation. It receives a state
    from the main program, and then it repeatedly applies the step function of
    the simulation to produce more states. Those states are then put in the
    cruncher's `.work_queue`. They are then taken by the main program when
    `Project.sync_crunchers` is called, and put into the tree.
        
    Read more about crunchers in the documentation of the `crunchers` package.
    
    The advantages of `ThreadCruncher` over `ProcessCruncher` are:
    1. `ThreadCruncher` is able to handle simulations that are
       history-dependent, which would have been very hard to implement in a 
       Process, since processes don't share memory, while threads do share
       memory trivially.
    2. `ThreadCruncher` is based on the `threading` module, which is stabler
       and more mature than the `multiprocessing` module.
    3. `ThreadCruncher` is much easier to debug than `ProcessCruncher`, since
       there are currently many more tools for debugging Python threads than
       Python processes.
    4. On a single-core computer, `ThreadCruncher` may be faster than
       `ProcessCruncher` because of shared memory.
    '''
    
    gui_explanation = string_tools.docstring_trim(
    '''
    `ThreadCruncher`:
    
     - Works from a `threading.Thread`.
    
     - Able to handle simulations that are history-dependent.
    
     - Based on the `threading` module, which is stabler and more mature than
       the `multiprocessing` module.
    
     - Easy to debug.
    
     - On a single-core computer, it may be faster than `ProcessCruncher`\
       because of shared memory.
       
    '''
    )
    
    
    @staticmethod
    def can_be_used_with_simpack_grokker(simpack_grokker):
        '''
        Return whether `ThreadCruncher` can be used with a simpack grokker.
        
        The answer is always `True`.
        '''
        return True
    
    
    def __init__(self, crunching_manager, initial_state, crunching_profile):
        BaseCruncher.__init__(self, crunching_manager,
                              initial_state, crunching_profile)
        threading.Thread.__init__(self)
        
        self.step_iterator_getter = \
            self.project.simpack_grokker.get_step_iterator
        self.history_dependent = self.project.simpack_grokker.history_dependent
        
        self.daemon = True

        self.work_queue = Queue.Queue(
            garlicsim.asynchronous_crunching.CRUNCHER_QUEUE_SIZE
        )
        '''
        Queue for putting completed work to be picked up by the main thread.
        
        In this queue the cruncher will put the states that it produces, in
        chronological order. If the cruncher reaches a simulation ends, it will
        put an `EndMarker` in this queue.
        '''

        self.order_queue = Queue.Queue()
        '''Queue for receiving instructions from the main thread.'''

        
    def run(self):
        '''
        Internal method.
        
        This is called when the cruncher is started. It just calls the
        `main_loop` method in a `try` clause, excepting
        `ObsoleteCruncherException`; That exception means that the cruncher has
        been retired in the middle of its job, so it is propagated up to this
        level, where it causes the cruncher to terminate.
        '''
        try:
            self.main_loop()
        except ObsoleteCruncherException:
            return

        
    def main_loop(self):
        '''
        The main loop of the cruncher.
        
        Crunches the simulations repeatedly until either:

         1. The crunching profile is satisfied. (i.e. we have reached a
            high-enough clock reading,)
        
        or
        
         2. A 'retire' order has been received,
         
        or 
        
         3. We have reached a simulation end. (i.e. the step function raised
            `WorldEnded`.)
            
        or 
        
         4. We have received a new crunching profile which has a different step
            profile than the one we started with. We can't change step profile
            on the fly, so we simply retire and let the crunching manager 
            recruit a new cruncher.
            
        '''
        
        self.step_profile = self.crunching_profile.step_profile
        
        if self.history_dependent:
            self.history_browser = HistoryBrowser(cruncher=self)
            thing = self.history_browser
        else:
            thing = self.initial_state

        self.iterator = self.step_iterator_getter(thing, self.step_profile)
            
        order = None
        
        try:
            for state in self.iterator:
                self.work_queue.put(state)
                self.check_crunching_profile(state)
                order = self.get_order()
                if order:
                    self.process_order(order)
        except garlicsim.misc.WorldEnded:
            self.work_queue.put(
                garlicsim.asynchronous_crunching.misc.EndMarker()
            )

        
    def check_crunching_profile(self, state):
        '''
        Check if the cruncher crunched enough states. If so retire.
        
        The crunching manager specifies how much the cruncher should crunch.
        We consult with it to check if the cruncher has finished, and if it did
        we retire the cruncher.
        '''
        if self.crunching_profile.state_satisfies(state):
            raise ObsoleteCruncherException("We're done working, the clock "
                                            "target has been reached. "
                                            "Shutting down.")

        
    def get_order(self):
        '''
        Attempt to read an order from the `.order_queue`, if one has been sent.
        
        Returns the order.
        '''
        try:
            return self.order_queue.get(block=False)
        except Queue.Empty:
            return None

        
    def process_order(self, order):
        '''Process an order receieved from `.order_queue`.'''
        if order == 'retire':
            raise ObsoleteCruncherException("Cruncher received a 'retire' "
                                            "order; Shutting down.")
        
        elif isinstance(order, CrunchingProfile):
            self.process_crunching_profile_order(order)
            
            
    def process_crunching_profile_order(self, order):
        '''Process an order to update the crunching profile.'''
        if self.crunching_profile.step_profile != order.step_profile:
            raise ObsoleteCruncherException('Step profile changed; shutting '
                                            'down. Crunching manager should '
                                            'create a new cruncher.')
        self.crunching_profile = order

        
    def retire(self):
        '''
        Retire the cruncher. Thread-safe.
        
        Causes it to shut down as soon as it receives the order.
        '''
        self.order_queue.put('retire')        
        
        
    def update_crunching_profile(self, profile):
        '''Update the cruncher's crunching profile. Thread-safe.'''
        self.order_queue.put(profile)
        
        
    is_alive = threading.Thread.isAlive
    '''Crutch for Python 2.5 and below.'''
    

