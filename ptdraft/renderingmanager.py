"""
Make it a daemon?
"""

import time


import wx
from threading import *
from core import *
import simulations.life.life as life
import simulations.life.lifegui as lifegui
import warnings
from edgerenderer import *

class RenderingManager(Thread):
    def __init__(self,*args,**kwargs):
        try:
            kwargs["name"]
        except:
            kwargs["name"]="Rendering Manager"

        self.niftylock=kwargs["niftylock"]
        del kwargs["niftylock"]


        Thread.__init__(self,*args,**kwargs)
        """
        Supposed to create a pool of processes here, right?
        """
        self.paths={}
        self.start()

    def run(self):
        while True:
            time.sleep(0.1)


        for path in self.paths:
            pass

    def add_path(self,newpath):
        #Checking if path is already taken care of:
        for path in self.paths:
            if path.leads_to_same_edge(newpath)==True:
                warnings.warn("Path leading to same edge already present")
                return False
        edge=newpath[-1]
        self.niftylock.acquire(edge)
        self.paths[newpath]=EdgeRenderer(path=newpath)
        self.paths[newpath].start()

