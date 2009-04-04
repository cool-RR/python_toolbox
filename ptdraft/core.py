import functools
import nib
import time

"""
TODO: in radiation style simulations, how will the simulator know
the history of the particles' movements? Two options. Either
traverse the nibtree, or have that information inside every
nib. Which one should I choose?

Or maybe give two options, one where the simulations gets the
nib and one where it gets the nibleaf.
"""


class Simulation(object):
    """
    This is a general class for simulations.
    Bernd-style simulations will inherit from this class.
    Life-Style simulations will also inherit from this class.
    Therefore, this class will be quite general.
    """

    def step(self, *args, **kwargs):
        raise NotImplementedError

    def show(self, *args, **kwargs):
        raise NotImplementedError

    def makeplainnib(self, *args, **kwargs):
        raise NotImplementedError

    def makerandomnib(self, *args, **kwargs):
        raise NotImplementedError

    def step(self, *args, **kwargs):
        raise NotImplementedError

    def compareclockreadings(self,*args,**kwargs):
        raise NotImplementedError #Maybe return None here?


class Playon(object):
    """
    initially each playon will be attached to a specific "simulation";
    later I'll make it able to use several simulations
    """

    def __init__(self,simulationclass):
        self.simulation=simulationclass()
        self.nibtree=nib.NibTree()

    def makeplainroot(self,*args,**kwargs):
        nib=self.simulation.makeplainnib(*args,**kwargs)
        nib.maketouched()
        return self.rootthisnib(nib)

    def makerandomroot(self,*args,**kwargs):
        nib=self.simulation.makerandomnib(*args,**kwargs)
        nib.maketouched()
        return self.rootthisnib(nib)

    def rootthisnib(self,nib):
        return self.nibtree.addnib(nib)

    def step(self,sourcenibleaf,t=1):
        newnib=self.simulation.step(sourcenibleaf.nib,t)
        return self.nibtree.addnib(newnib,sourcenibleaf)

    def multistep(self,sourcenibleaf,t=1,steps=1):
        mynibleaf=sourcenibleaf
        for i in range(steps):
            mynibleaf=self.step(mynibleaf,t)
        return mynibleaf











"""
class bernd(simulation):
    def step(self):
        print("thing")
    pass
"""