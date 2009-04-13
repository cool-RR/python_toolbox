import wx
from multiprocessing import *
from core import *
import simulations.life.life as life
import simulations.life.lifegui as lifegui
import threading


class EdgeRenderer(Process):
    def __init__(self,*args,**kwargs):

        self.path=kwargs["path"]
        del kwargs["path"]


        Process.__init__(self,*args,**kwargs)
        self.edge=self.path[-1]
        self.message_queue=Queue() # use it for messages?
        self.work_queue=Queue()

    def run(self):
        import simulations.life.life as simulation
        import core
        import wx
        work()

    def work(self):
        current=self.edge
        while True:
            next=simulation.step(current)
            self.work_queue.put(next)
            current=next

            try:
                order=self.message_queue.get()
                #do something with order
            except:
                pass


