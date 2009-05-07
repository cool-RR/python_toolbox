import functools
import state
import time
from edgecruncher import EdgeCruncher
from misc.dumpqueue import dump_queue
from misc.infinity import Infinity

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
    A SimulationCore is meant to be subclassed. A subclass of
    SimulationCore has to define a function "step(self,source_state)"
    that describes how to advance from one state to the next.
    It should also define a few more functions: Currently those are
    "make_plain_state" and "make_random_state".


    todo Thought: maybe instead of a SimulationCore object,
    it should just be one function?
    """

    def make_plain_state(self, *args, **kwargs):
        raise NotImplementedError

    def make_random_state(self, *args, **kwargs):
        raise NotImplementedError



class Project(object):
    """
    A Project encapsulates a Tree and a SimulationCore.

    A Project, among other things, takes care of background
    crunching of the simulation, using the "multiprocessing" module. A
    Project employs "workers", actually instances of the EdgeCruncher
    class, a subclass of multiprocessing.Process.
    The Project is responsible for coordinating the workers. The method
    sync_workers makes the Project review the work done by the workers,
    implement it into the Tree, and gives them new instructions if necessary.

    It is important to note that the Project class does not
    require wxPython or any other GUI package: It can be used entirely from
    the Python command-line.

    todo: initially each Project will be attached to a specific SimulationCore;
    later I'll make it able to use several SimulationCores
    """

    def __init__(self,specific_simulation_package):
        """
        That "SimulationCoreclass" should be the class that you have created
        by subclassing SimulationCore.
        """
        self.specific_simulation_package=specific_simulation_package
        self.tree=state.Tree()

        self.workers={} # A dict that maps edges that should be worked on to workers

        self.edges_to_crunch={}
        """
        A dict that maps edges that should be worked on to a number specifying
        how many nodes should be created after them.
        """

    """
    def load_specific_simulation_package(self,specific_simulation_package):
        self.specific_simulation_package=specific_simulation_package
    """

    def make_plain_root(self,*args,**kwargs):
        """
        Creates a parent-less node, whose state is a simple plain state.
        The SimulationCore subclass should define the function "make_plain_state"
        for this to work.
        Returns the node.
        """
        state=self.specific_simulation_package.make_plain_state(*args,**kwargs)
        state._State__touched=True
        return self.root_this_state(state)

    def make_random_root(self,*args,**kwargs):
        """
        Creates a parent-less node, whose state is a random and messy state.
        The SimulationCore subclass should define the function "make_random_state"
        for this to work.
        Returns the node.
        """
        state=self.specific_simulation_package.make_random_state(*args,**kwargs)
        state._State__touched=True
        return self.root_this_state(state)

    def root_this_state(self,state):
        """
        Takes a state, wraps it in a node and adds to the Tree without a parent.
        Returns the node.
        """
        return self.tree.add_state(state)

    def step(self,sourcenode,t=1):
        """
        Takes a node and simulates a child node from it.
        This is NOT done in the background.
        Returns the child node.
        """
        newstate=self.specific_simulation_package.step(sourcenode.state,t)
        return self.tree.add_state(newstate,sourcenode)

    def multistep(self,sourcenode,t=1,steps=1):
        """
        Takes a node and simulates a succession of child nodes from it.
        "steps" specifies how many nodes.
        This is NOT done in the background.
        Returns the last node.
        """
        mynode=sourcenode
        for i in range(steps):
            mynode=self.step(mynode,t)
        return mynode

    def get_all_edges(self,node,max_distance=Infinity):
        """
        Given a node, finds all edges that are its descendents.
        Only edges with a distance of at most max_distance are returned.
        Returns a dict of the form {node1:distance1, node2:distance2, ...}
        """
        nodes={node:0}
        edges={}


        while len(nodes)>0:
            (node,d)=nodes.popitem()
            if d>max_distance:
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

                if rest_of_block+d<=max_distance:
                    for kid in block[-2].children:
                        nodes[kid]=d+rest_of_block
                    continue
        return edges



    def get_edge_on_path(self,node,path,max_distance=Infinity):
        """
        Given a node, finds the edge that is a descendant of it and is on "path".
        Only an edge with a distance of at most max_distance is returned.
        Returns a dict of the form {node:distance}
        """
        current=node
        i=0
        while i<max_distance+1:
            try:
                current=path.next_node(current)
            except IndexError:
                return {current:i}
            i+=1
        return {}


    def crunch_all_edges(self,node,wanted_distance):
        """
        Orders to start crunching from all the edges of "node",
        so that there will be a buffer whose length is at least "wanted_distance".
        """
        edges=self.get_all_edges(node,wanted_distance)
        for (edge,distance) in edges.items():
            new_distance=wanted_distance-distance
            if self.edges_to_crunch.has_key(edge):
                self.edges_to_crunch[edge]=max(new_distance,self.edges_to_crunch[edge])
            else:
                self.edges_to_crunch[edge]=new_distance

    def crunch_on_path(self,node,wanted_distance,path):
        """
        Orders to start crunching from the edge of the path on which "node" lies,
        so that there will be a buffer whose length is at least "wanted_distance".
        """
        edge_dict=get_edge_on_path(node,wanted_distance) # This dict may have a maximum of one item
        for (edge,distance) in edges.items():
            new_distance=wanted_distance-distance
            if self.edges_to_crunch.has_key(edge):
                self.edges_to_crunch[edge]=max(new_distance,self.edges_to_crunch[edge])
            else:
                self.edges_to_crunch[edge]=new_distance


    def sync_workers(self,*args,**kwargs):
        """
        Talks with all the workers, takes work from them for
        implementing into the Tree, terminates workers or creates
        new workers if necessary.
        """
        for edge in self.workers.copy():
            if not (edge in self.edges_to_crunch):
                worker=self.workers[edge]
                result=dump_queue(worker.work_queue)

                worker.terminate()

                current=edge
                for state in result:
                    current=self.tree.add_state(state,parent=current)

                del self.workers[edge]
                worker.join() # todo: sure?

        for (edge,number) in self.edges_to_crunch.items():
            if self.workers.has_key(edge) and self.workers[edge].is_alive():

                worker=self.workers[edge]
                result=dump_queue(worker.work_queue)

                current=edge
                for state in result:
                    current=self.tree.add_state(state,parent=current)

                del self.edges_to_crunch[edge]


                if number!=Infinity:
                    new_number=number-len(result)
                    if new_number<=0:
                        worker.terminate()
                        worker.join() # todo: sure?
                        del self.workers[edge]
                    else:
                        self.edges_to_crunch[current]=new_number
                        del self.workers[edge]
                        self.workers[current]=worker

                else:
                    self.edges_to_crunch[current]=Infinity
                    del self.workers[edge]
                    self.workers[current]=worker




            else:
                # Create worker
                if edge.still_in_editing==False:
                    worker=self.workers[edge]=EdgeCruncher(edge.state,step_function=self.specific_simulation_package.step)
                    worker.start()
