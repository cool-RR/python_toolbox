import functools
import state
import time

"""
TODO: in radiation style simulations, how will the simulator know
the history of the particles' movements? Two options. Either
traverse the tree, or have that information inside every
state. Which one should I choose?

Or maybe give two options, one where the simulation gets the
state and one where it gets the node.
"""


class SimulationCore(object):
    """
    A SimulationCore


    """

    def step(self, *args, **kwargs):
        raise NotImplementedError

    def show(self, *args, **kwargs):
        raise NotImplementedError

    def make_plain_state(self, *args, **kwargs):
        raise NotImplementedError

    def make_random_state(self, *args, **kwargs):
        raise NotImplementedError

    def step(self, *args, **kwargs):
        raise NotImplementedError



class Project(object):
    """
    initially each playon will be attached to a specific SimulationCore;
    later I'll make it able to use several SimulationCores
    """

    def __init__(self,SimulationCoreclass):
        self.SimulationCore=SimulationCoreclass()
        self.tree=state.Tree()

    def make_plain_root(self,*args,**kwargs):
        state=self.SimulationCore.make_plain_state(*args,**kwargs)
        state._State__touched=True
        return self.root_this_state(state)

    def make_random_root(self,*args,**kwargs):
        state=self.SimulationCore.make_random_state(*args,**kwargs)
        state._State__touched=True
        return self.root_this_state(state)

    def root_this_state(self,state):
        return self.tree.add_state(state)

    def step(self,sourcenode,t=1):
        newstate=self.SimulationCore.step(sourcenode.state,t)
        return self.tree.add_state(newstate,sourcenode)

    def multistep(self,sourcenode,t=1,steps=1):
        mynode=sourcenode
        for i in range(steps):
            mynode=self.step(mynode,t)
        return mynode











"""
class bernd(SimulationCore):
    def step(self):
        print("thing")
    pass
"""