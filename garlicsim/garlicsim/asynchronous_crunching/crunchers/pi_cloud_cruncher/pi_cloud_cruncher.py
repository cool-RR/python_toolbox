# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.


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
        threading.Thread.__init__(self)
        
        cloud = import_tools.import_if_exists('cloud', silent_fail=True)
        if not cloud:
            raise ImportError("The `cloud` module is needed. Get it at "
                              "http://picloud.com.")

        self.step_iterator_getter = \
            self.project.simpack_grokker.get_step_iterator
        self.history_dependent = self.project.simpack_grokker.history_dependent

        self.last_clock = initial_state.clock

        self.daemon = True

        self.work_queue = Queue.Queue()
        ''' 
        Queue for putting completed work to be picked up by the main thread.

        In this queue the cruncher will put the states that it produces, in
        chronological order. If the cruncher is being given a new crunching
        profile which has a new and different step profile, the cruncher
        will put the new step profile in this queue in order to signal that
        from that point on, all states were crunched with that step profile.
        '''

        self.order_queue = Queue.Queue()
        '''Queue for receiving instructions from the main thread.'''


    def run(self):
        '''
        Internal method.

        This is called when the cruncher is started. It just calls the main_loop
        method in a try clause, excepting ObsoleteCruncherError; That exception
        means that the cruncher has been retired in the middle of its job, so it
        is propagated up to this level, where it causes the cruncher to
        terminate.
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


    def retire(self):
        '''
        Retire the cruncher. Thread-safe.

        Causes it to shut down as soon as it receives the order.
        '''
        self.order_queue.put('retire')        


    def update_crunching_profile(self, profile):
        '''Update the cruncher's crunching profile. Thread-safe.'''
        self.order_queue.put(profile)


    def is_alive(self):
        1/0


