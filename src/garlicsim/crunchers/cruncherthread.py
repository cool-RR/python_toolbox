"""
This module defines CruncherThread. See its documentation.
"""
import threading

try:
    import queue
except ImportError:
    import Queue as queue

from garlicsim.historybrowser import HistoryBrowser


class CruncherThread(threading.Thread):
    """
    CruncherThread is a type of cruncher.
    
    A cruncher is a dumb little drone. It receives a state from the main
    program, and then it repeatedly applies the step funcion of the simulation
    to produce more states. Those states are then put in the cruncher's
    work_queue. They are then taken by the main program when
    Project.sync_workers is called, and put into the tree.
        
    Read more about crunchers in the documentation of the crunchers package.
    
    The advantage of CruncherThread over CruncherProcess is that
    CruncherThread is able to handle simulations that are history-dependent.
    """
    def __init__(self, initial_state, project ,step_function, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        
        self.project = project
        self.step = step_function
        
        self.history_dependent = \
            hasattr(self.step,"history_dependent") and self.step.history_dependent
        
        if self.history_dependent:
            self.do_work = self.do_history_dependent_work
        else:
            self.do_work = self.do_non_history_dependent_work

        
        self.initial_state = initial_state
        self.daemon = True

        self.work_queue = queue.Queue()
        """
        The cruncher puts the work that it has completed
        into this queue, to be picked up by sync_workers.
        """

        self.order_queue = queue.Queue()
        """
        This queue is used to send instructions
        to the cruncher.
        """


    def run(self):
        """
        This is called when the cruncher is started. It just calls
        the main_loop method.
        """
        try:
            self.main_loop()
        except ObsoleteCruncherError:
            return

    def main_loop(self):
        """
        The main loop of the cruncher. It's basically, "As long as no one
        tells you to retire, apply the step function repeatedly."
        """
        self.current = self.initial_state
        order = None
        if self.history_dependent:
            self.history_browser = HistoryBrowser(cruncher=self)
        
        while True:
            self.do_work()
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
        
    def do_non_history_dependent_work(self):
        """
        This is the "work" function for the cruncher in the case the simulation
        is NOT history-dependent.
        It calls the step function on the current state and makes that result
        the current state, putting it in the work_queue.
        """
        next = self.step(self.current)
        self.work_queue.put(next)
        self.current = next
    
    def do_history_dependent_work(self):
        """
        This is the "work" function for the cruncher in the case the simulation
        is history-dependent.
        It calls the step function on the history browser. It then put the
        returned state in the work_queue.
        """
        next = self.step(self.history_browser)
        self.work_queue.put(next)        
        self.current = next
    
    def retire(self):
        """
        Retiring the cruncher, causing it to shut down as soon as it receives
        the order. This method may be called either from within the thread or
        from another thread.
        """
        self.order_queue.put("Retire")

from garlicsim.crunchers import ObsoleteCruncherError