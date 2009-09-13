"""
This module defines CruncherThread. See its documentation.
"""
import threading

try:
    import queue
except ImportError:
    import Queue as queue

from garlicsim.asynchronous_crunching.project.history_browser import HistoryBrowser

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
    def __init__(self, initial_state, project, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        
        self.project = project
        
        self.history_dependent = self.project.simpack_grokker.history_dependent
        

        
        self.initial_state = initial_state
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
    
        
        if self.history_dependent:
            self.history_browser = HistoryBrowser(cruncher=self)
            self.step_iterator = self.project.simpack_grokker.step_generator \
                             (self.history_browser)
        else:
            self.step_iterator = self.project.simpack_grokker.step_generator \
                              (self.initial_state) 
        
        order = None
        
        
        for state in self.step_iterator:
            
            self.work_queue.put(state)
        
            order = self.get_order()
            if order:
                self.process_order(order)
                order = None
    
                
            
                    
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
        if order=="Retire":
            raise ObsoleteCruncherError
        
    
    def retire(self):
        """
        Retiring the cruncher, causing it to shut down as soon as it receives
        the order. This method may be called either from within the thread or
        from another thread.
        """
        self.order_queue.put("Retire")

from exceptions import ObsoleteCruncherError