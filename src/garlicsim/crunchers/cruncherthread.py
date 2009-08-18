"""

Maybe be more DRYish in thread and process?

Maybe make the process/thread just an attribute?

todo: What if EdgeRenderer has a run-time error?


todo: In the future, we may want the EdgeCruncher to receive a
copy of the SimulationCore object. We will have to implement
a copy() method on SimulationCore and pass it on to the new process.


todo maybe: put something on edgecruncher that will shut it off
if the main program is killed

todo maybe: process creation is sometimes slow on windows.
maybe have a spare EdgeCruncher at all times?

todo maybe: instead of passing the starter state as a parameter,
it should be sent in a queue.

todo: make sure the cursor does not get an hourglass when it shouldn't

todo: Smarter priority setting. Besides, obviously, supporting Linux,
Mac OS, etc., we need to monitor how much de-facto priority the
process is actually getting from the OS, and to tweak its "official"
priority accordingly.

todo: it seems that on one-core systems the crunching is very slow.
Maybe due to very low process priority of edgecruncher.


"""


import threading

try:
    import queue
except ImportError:
    import Queue as queue

from garlicsim.historybrowser import HistoryBrowser

try:
    from misc.processpriority import set_process_priority
except:
    pass

class CruncherThread(threading.Thread):
    """
    EdgeCruncher is a subclass of multiprocessing.Process. An EdgeCruncher
    is responsible for crunching the simulation in the background.
    An EdgeCruncher gets its instruction from the method `Project.sync_workers`.

    How does the EdgeCruncher work? Essentially, it gets sent a state from
    sync_workers. It then starts repeatedly stepping from this state, and puts
    all the resulting states in a queue. An EdgeCruncher is quite dumb actually,
    most of the smart work is being done by sync_workers.
    """
    def __init__(self, initial_node, project ,step_function, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        
        self.project = project
        self.step = step_function
        self.history_looker = hasattr(self.step,"history_looker") and self.step.history_looker
        if self.history_looker:
            self.do_work = self.do_history_looker_work
        else:
            self.do_work = self.do_non_history_looker_work
    
        if self.history_looker:
            self.history_browser = HistoryBrowser(cruncher=self, initial_node=initial_node)
        
        self.initial_state = initial_node.state
        self.daemon = True

        self.work_queue = queue.Queue()
        """
        The EdgeCruncher puts the work that it has completed
        into this queue, to be picked up by sync_workers.
        """

        self.message_queue = queue.Queue()
        """
        This queue is used by sync_workers to send instructions
        to the EdgeRenderer.
        """


    def set_priority(self,priority):
        """
        Sets the priority of this process: Currently Windows only.
        """
        assert priority in [0,1,2,3,4,5]
        set_process_priority(self.pid,priority)

    def run(self):
        """
        The function ran by EdgeCruncher. Does the actual work.
        """

        try:
            #self.set_priority(0)
            pass
        except:
            pass

        #import psyco #These two belong here?
        #psyco.full()

        self.current = self.starter
        order = None
        if self.history_looker:
            self.history_browser = historybrowser.HistoryBrowser(self)
            
        while True:
            self.do_work()

            try:
                order=self.message_queue.get(block=False)
                #do something with order
                if order=="Retire":
                    return
                order = None
            except queue.Empty:
                pass
            
    def do_non_history_looker_work(self):
        next = self.step(self.current)
        self.work_queue.put(next)
        self.current = next
    
    def do_history_looker_work(self):
        #if self.history_looker
        
        pass
    
    def retire(self):
        """
        This method may be called both from within the process and from outside the process.
        """
        self.message_queue.put("Retire")

