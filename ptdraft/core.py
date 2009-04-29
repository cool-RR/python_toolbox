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

todo:
maybe introduce an "Infinity" constant for when you want
to buffer an edge indefinitly? Currently we're using None.
Might simplify arithmetic too.
"""


class SimulationCore(object):
    """


    Thought: maybe instead of a SimulationCore object,
    it should just be one function?


    """

    def make_plain_state(self, *args, **kwargs):
        raise NotImplementedError

    def make_random_state(self, *args, **kwargs):
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

    """
    def old_get_all_edges(self,node,max_distance=None):
        if node.children==[]:
            return {node:0}
        if max_distance==0:
            return {}

        new_distance=max_distance-1 if max_distance!=None else None

        d={}
        for kid in node.children:
            d.update(self.get_all_edges(kid,new_distance))
        return d
    """

    def get_all_edges(self,node,max_distance=None):
        nodes={node:0}
        edges={}
        def within_max_distance(distance):
            if max_distance==None:
                return True
            else:
                return distance<=max_distance

        while len(nodes)>0:
            (node,d)=nodes.popitem()
            if within_max_distance(d)==False:
                continue
            kids=node.children
            if kids==[]:
                #We have an edge!
                edges[node]=d
                continue
            if node.block==None:
                for kid in kids:
                    nodes[kid]=d+1
                continue
            else:
                block=node.block
                index=block.list.index(node)
                rest_of_block=(len(block)-index-1)

                if rest_of_block==0: # If we hit the last node in the Block
                    for kid in kids:
                        nodes[kid]=d+1
                    continue

                if within_max_distance(rest_of_block+d):
                    for kid in block[-2].children:
                        nodes[kid]=d+rest_of_block
                    continue
        return edges





    def get_edge_on_path(self,node,max_distance,path):
        current=node
        i=0
        #for i in range(max_distance+1):
        while max_distance==None or i<max_distance+1:
            try:
                current=path.next_node(current)
            except IndexError:
                return {current:i}
            i+=1
        return {}


    def render_all_edges(self,node,wanted_distance):
        edges=self.get_all_edges(node,wanted_distance)
        for (edge,distance) in edges.items():
            new_distance=wanted_distance-distance if wanted_distance!=None else None
            if self.edges_to_render.has_key(edge):
                self.edges_to_render[edge]=max(new_distance,self.edges_to_render[edge])
            else:
                self.edges_to_render[edge]=new_distance

    def render_on_path(self,node,wanted_distance,path=None):
        if path==None:
            path=self.path
        edge_dict=get_edge_on_path(node,wanted_distance) # This dict may have a maximum of one item
        for (edge,distance) in edges.items():
            new_distance=wanted_distance-distance if wanted_distance!=None else None
            if self.edges_to_render.has_key(edge):
                self.edges_to_render[edge]=max(new_distance,self.edges_to_render[edge])
            else:
                self.edges_to_render[edge]=new_distance


    def manage_workers(self,*args,**kwargs):
        """
        Rename to sync_workers
        """
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
                        del self.workers[edge]
                    else:
                        self.edges_to_render[current]=new_number
                        del self.workers[edge]
                        self.workers[current]=worker

                else:
                    self.edges_to_render[current]=None
                    del self.workers[edge]
                    self.workers[current]=worker




            else:
                #CREATE WORKER
                worker=self.workers[edge]=EdgeRenderer(edge.state)
                worker.start()
