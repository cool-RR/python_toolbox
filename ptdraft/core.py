import functools
import nib
import time

"""
TODO: in radiation style simulations, how will the simulator know
the history of the particles' movements? Two options. Either
traverse the nibtree, or have that information inside every
nib. Which one should I choose?

Or maybe give two options, one where the simulation gets the
nib and one where it gets the nibnode.
"""


class SimulationCore(object):
    """
    A SimulationCore


    """

    def step(self, *args, **kwargs):
        raise NotImplementedError

    def show(self, *args, **kwargs):
        raise NotImplementedError

    def make_plain_nib(self, *args, **kwargs):
        raise NotImplementedError

    def make_random_nib(self, *args, **kwargs):
        raise NotImplementedError

    def step(self, *args, **kwargs):
        raise NotImplementedError



class Playon(object):
    """
    initially each playon will be attached to a specific SimulationCore;
    later I'll make it able to use several SimulationCores
    """

    def __init__(self,SimulationCoreclass):
        self.SimulationCore=SimulationCoreclass()
        self.nibtree=nib.NibTree()

    def make_plain_root(self,*args,**kwargs):
        nib=self.SimulationCore.make_plain_nib(*args,**kwargs)
        nib._Nib__touched=True
        return self.root_this_nib(nib)

    def make_random_root(self,*args,**kwargs):
        nib=self.SimulationCore.make_random_nib(*args,**kwargs)
        nib._Nib__touched=True
        return self.root_this_nib(nib)

    def root_this_nib(self,nib):
        return self.nibtree.add_nib(nib)

    def step(self,sourcenibnode,t=1):
        newnib=self.SimulationCore.step(sourcenibnode.nib,t)
        return self.nibtree.add_nib(newnib,sourcenibnode)

    def multistep(self,sourcenibnode,t=1,steps=1):
        mynibnode=sourcenibnode
        for i in range(steps):
            mynibnode=self.step(mynibnode,t)
        return mynibnode











"""
class bernd(SimulationCore):
    def step(self):
        print("thing")
    pass
"""