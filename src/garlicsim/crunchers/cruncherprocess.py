"""
This module defines CruncherProcess. See its documentation.
"""

import multiprocessing

try:
    import queue
except ImportError:
    import Queue as queue

try:
    import garlicsim.misc.processpriority as processpriority
except ImportError:
    pass

class CruncherProcess(multiprocessing.Process):
    """
    CruncherProcess is a type of cruncher.
    
    A cruncher is a dumb little drone. It receives a state from the main
    program, and then it repeatedly applies the step funcion of the simulation
    to produce more states. Those states are then put in the cruncher's
    work_queue. They are then taken by the main program when
    Project.sync_crunchers is called, and put into the tree.
        
    Read more about crunchers in the documentation of the crunchers package.
    
    The advantage of CruncherProcess over CruncherThread is that
    CruncherProcess is able to run on a different core of the processor
    in the machine, thus using the full power of the processor.
    """
    def __init__(self, initial_state, step_function, *args, **kwargs):
        multiprocessing.Process.__init__(self, *args, **kwargs)

        self.step = step_function
        self.initial_state = initial_state
        self.daemon = True

        self.work_queue = multiprocessing.Queue()
        """
        The cruncher puts the work that it has completed
        into this queue, to be picked up by sync_crunchers.
        """
        
        self.order_queue = multiprocessing.Queue()
        """
        This queue is used to send instructions
        to the cruncher.
        """


    def set_priority(self,priority):
        """
        Sets the priority of this process: Currently Windows only.
        """
        assert priority in [0,1,2,3,4,5]
        try:
            processpriority.set_process_priority(self.pid, priority)
        except: #Not sure exactly what to "except" here; wary of non-windows systems.
            pass

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
        self.set_priority(0)
        self.current = self.initial_state
        order = None
        
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
        
    def do_work(self):
        """
        This is the "work" function for the cruncher.
        It calls the step function on the current state and makes that result
        the current state, putting it in the work_queue.
        """
        next = self.step(self.current)
        self.work_queue.put(next)
        self.current = next

    def retire(self):
        """
        Retiring the cruncher, causing it to shut down as soon as it receives
        the order. This method may be called either from within the process or
        from another process.
        """
        self.order_queue.put("Retire")

from garlicsim.crunchers import ObsoleteCruncherError