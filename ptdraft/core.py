import functools
import state
import time
from edgerenderer import EdgeRenderer
from misc.dumpqueue import dump_queue

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
        self.workers={} # A dict that maps edges that should be worked on to workers
        self.edges_to_render={}

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
        """
        rename/deprecate?
        """
        newstate=self.SimulationCore.step(sourcenode.state,t)
        return self.tree.add_state(newstate,sourcenode)

    def multistep(self,sourcenode,t=1,steps=1):
        """
        rename/deprecate?
        """
        mynode=sourcenode
        for i in range(steps):
            mynode=self.step(mynode,t)
        return mynode

    def get_all_edges(self,node,distance):
        """
        Can be optimized using Blocks?
        """
        if node.children==[]:
            return {node:0}
        if distance==0:
            return {}

        new_distance=distance-1 if distance!=None else None

        d={}
        for kid in node.children:
            d.update(self.get_all_edges(kid,new_distance))
        return d

    def get_edge_on_path(self,node,distance,path=None):
        if path==None:
            path=self.path
        current=node
        for i in range(distance+1):
            try:
                current=path.next_node(current)
            except IndexError:
                return {current:i}
        return {}


    def render_all_edges(self,node,wanted_distance):
        edges=self.get_all_edges(node,wanted_distance)
        for (edge,distance) in edges.items():
            new_distance=wanted_distance-distance if wanted_distance!=None else None
            if self.edges_to_render.has_key(edge):
                self.edges_to_render[edge]=max(new_distance,self.edges_to_render[edge])
            else:
                self.edges_to_render[edge]=new_distance

    def render_on_path(self,node,wanted_distance):
        edge_dict=get_edge_on_path(node,wanted_distance) # This dict may have a maximum of one item
        for (edge,distance) in edges.items():
            new_distance=wanted_distance-distance if wanted_distance!=None else None
            if self.edges_to_render.has_key(edge):
                self.edges_to_render[edge]=max(new_distance,self.edges_to_render[edge])
            else:
                self.edges_to_render[edge]=new_distance


    def manage_workers(self,*args,**kwargs):
        for edge in self.workers.copy():
            if not (edge in self.edges_to_render):
                #TAKE WORK FROM WORKER AND TERMINATE IT, ALSO DELETE FROM self.workers
                worker=self.workers[edge]
                result=dump_queue(worker.work_queue)

                worker.terminate()

                current=edge
                for state in result:
                    current=self.tree.add_state(state,parent=current)

                del self.workers[edge]
                worker.join() #sure?

        for (edge,number) in self.edges_to_render.items():
            if self.workers.has_key(edge):
                #TAKE WORK FROM WORKER, CHANGE EDGE
                #IMPLEMENT INTO TREE
                worker=self.workers[edge]
                result=dump_queue(worker.work_queue)

                current=edge
                for state in result:
                    current=self.tree.add_state(state,parent=current)

                del self.edges_to_render[edge]


                if number!=None:
                    new_number=number-len(result)
                    if new_number<=0:
                        worker.terminate()
                        worker.join() #sure?
                    else:
                        self.edges_to_render[current]=new_number
                else:
                    self.edges_to_render[current]=None


                del self.workers[edge]
                self.workers[current]=worker

            else:
                #CREATE WORKER
                worker=self.workers[edge]=EdgeRenderer(edge.state)
                worker.start()
