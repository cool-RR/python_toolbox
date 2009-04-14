import wx
from multiprocessing import *
from core import *
import simulations.life.life as life
import simulations.life.lifegui as lifegui
import threading

class EdgeRenderer(Process):
    def __init__(self,starter,*args,**kwargs):

        self.starter=starter

        Process.__init__(self,*args,**kwargs)
        self.daemon=True


        self.message_queue=Queue() # use it for messages?
        self.work_queue=Queue()



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

