"""

In the future, we may want the EdgeRenderer to receive a
copy of the SimulationCore object. We will have to implement
a copy() method on SimulationCore and pass it on to the new process.

"""


import wx
from multiprocessing import *
from core import *
import simulations.life.life as life
import simulations.life.lifegui as lifegui
import threading
from misc.processpriority import set_process_priority

class EdgeRenderer(Process):
    def __init__(self,starter,*args,**kwargs):
        Process.__init__(self,*args,**kwargs)
        self.set_priority(0)
        self.starter=starter
        self.daemon=True

        self.message_queue=Queue()
        self.work_queue=Queue()

    def set_priority(self,priority):
        assert priority in range(6)
        set_process_priority(self.pid,priority)

    def run(self):

        """
        import simulations.life.life as simulation
        import core
        import wx
        """
        mylife=life.Life()

        current=self.starter.nib
        order=None
        while True:
            next=mylife.step(current)
            self.work_queue.put(next)
            current=next

            try:
                order=self.message_queue.get(block=Flase)
                #do something with order
                if order=="Terminate":
                    break
                order=None
            except:
                pass

