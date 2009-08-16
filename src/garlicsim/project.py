"""
TODO: in radiation style simulations, how will the simulator know
the history of the particles' movements? Two options. Either
traverse the tree, or have that information inside every
state. Which one should I choose?

Or maybe give two options, one where the simulation gets the
state and one where it gets the node.

todo:
maybe path belongs in Project and not GuiProject?


    todo: specify arguments to step function

todo: more sophisticated version of `edges_to_crunch`.

"""

import random
import state
from crunchers import CruncherThread, CruncherProcess
from misc.dumpqueue import dump_queue
from misc.infinity import Infinity # Same as Infinity=float("inf")

PreferredCruncher = CruncherProcess


class Project(object):
    """
    `Project` is the main class that the garlicsim package defines.
    When you want to do a simulation, you create a Project. All your
    work is done within this Project.

    A Project encapsulates a Tree.

    A Project, among other things, takes care of background
    crunching of the simulation, using the `multiprocessing` module. A
    Project employs "workers", actually instances of the EdgeCruncher
    class, a subclass of multiprocessing.Process.
    The Project is responsible for coordinating the workers. The method
    sync_workers makes the Project review the work done by the workers,
    implement it into the Tree, and gives them new instructions if necessary.

    The Project class does not require wxPython or any other
    GUI package: It can be used entirely from the Python command-line.
    """

    def __init__(self,simulation_package):

        self.init_simulation_package(simulation_package)

        self.tree=state.Tree()

        if self.history_looker:
            self.Cruncher = CruncherThread
        else:
            self.Cruncher = PreferredCruncher

        self.workers={}
        """
        A dict that maps edges that should be worked on to workers.
        """

        self.edges_to_crunch={}
        """
        A dict that maps edges that should be worked on to a number specifying
        how many nodes should be created after them.
        """

    def init_simulation_package(self, simulation_package):

        self.simulation_package = simulation_package

        step_defined = hasattr(simulation_package, "step")
        history_step_defined = hasattr(simulation_package, "history_step")

        if step_defined and history_step_defined:
            raise StandardError("The simulation package is defining both a\
                                 step and a history_step - That's forbidden!")

        self.history_looker = history_step_defined


    def make_plain_root(self,*args,**kwargs):
        """
        Creates a parent-less node, whose state is a simple plain state.
        The simulation package should define the function `make_plain_state`
        for this to work.
        Returns the node.
        """
        state=self.simulation_package.make_plain_state(*args,**kwargs)
        state._State__touched=True
        return self.root_this_state(state)

    def make_random_root(self,*args,**kwargs):
        """
        Creates a parent-less node, whose state is a random and messy state.
        The simulation package  should define the function `make_random_state`
        for this to work.
        Returns the node.
        """
        state=self.simulation_package.make_random_state(*args,**kwargs)
        state._State__touched=True
        return self.root_this_state(state)

    def root_this_state(self,state):
        """
        Takes a state, wraps it in a node and adds to the Tree without a parent.
        Returns the node.
        """
        return self.tree.add_state(state)

    def step(self,source_node):
        """
        Takes a node and simulates a child node from it.
        This is NOT done in the background.
        Returns the child node.
        """
        new_state=self.simulation_package.step(source_node.state)
        return self.tree.add_state(new_state,source_node)

    def multistep(self,source_node,steps=1):
        """
        Takes a node and simulates a succession of child nodes from it.
        `steps` specifies how many nodes.
        This is NOT done in the background.
        Returns the last node.
        """
        my_node=source_node
        for i in range(steps):
            my_node=self.step(my_node)
        return my_node


    def crunch_all_edges(self,node,wanted_distance):
        """
        Orders to start crunching from all the edges of "node",
        so that there will be a buffer whose length
        is at least "wanted_distance".
        """
        edges=node.get_all_edges(wanted_distance)
        for (edge,distance) in edges.items():
            new_distance=wanted_distance-distance
            if self.edges_to_crunch.has_key(edge):
                self.edges_to_crunch[edge]=max(new_distance,self.edges_to_crunch[edge])
            else:
                self.edges_to_crunch[edge]=new_distance


    def sync_workers(self,temp_infinity_node=None):
        """
        Talks with all the workers, takes work from them for
        implementing into the Tree, terminates workers or creates
        new workers if necessary.
        You can pass a node as `temp_infinity_node`. That will cause this
        function to temporarily treat this node as if it should be crunched
        indefinitely.

        Returns the total amount of nodes that were added to the tree.
        """


        my_edges_to_crunch=self.edges_to_crunch.copy()

        if temp_infinity_node!=None:
            if self.edges_to_crunch.has_key(temp_infinity_node):
                had_temp_infinity_node=True
                previous_value_of_temp_infinity_node=self.edges_to_crunch[temp_infinity_node]
            else:
                had_temp_infinity_node=False
            my_edges_to_crunch[temp_infinity_node]=Infinity


        added_nodes=0

        for edge in self.workers.copy():
            if not (edge in my_edges_to_crunch):
                worker=self.workers[edge]
                result=dump_queue(worker.work_queue)

                worker.terminate()

                current=edge
                for state in result:
                    current=self.tree.add_state(state,parent=current)
                added_nodes+=len(result)

                del self.workers[edge]
                worker.join() # todo: sure?



        for (edge,number) in my_edges_to_crunch.items():
            if self.workers.has_key(edge) and self.workers[edge].is_alive():

                worker=self.workers[edge]
                result=dump_queue(worker.work_queue)

                current=edge
                for state in result:
                    current=self.tree.add_state(state,parent=current)
                added_nodes+=len(result)

                del my_edges_to_crunch[edge]


                if number!=Infinity: # Maybe this is just a redundant dichotomy from before I had Infinity?
                    new_number=number-len(result)
                    if new_number<=0:
                        worker.terminate()
                        worker.join() # todo: sure?
                        del self.workers[edge]
                    else:
                        my_edges_to_crunch[current]=new_number
                        del self.workers[edge]
                        self.workers[current]=worker

                else:
                    my_edges_to_crunch[current]=Infinity
                    del self.workers[edge]
                    self.workers[current]=worker

                if edge==temp_infinity_node:
                    continuation_of_temp_infinity_node=current
                    progress_with_temp_infinity_node=len(result)




            else:
                # Create worker
                if edge.still_in_editing==False:
                    worker=self.workers[edge]=self.Cruncher(edge.state,step_function=self.simulation_package.step)
                    worker.start()
                if edge==temp_infinity_node:
                    continuation_of_temp_infinity_node=edge
                    progress_with_temp_infinity_node=0

        if temp_infinity_node!=None:
            if had_temp_infinity_node:
                my_edges_to_crunch[continuation_of_temp_infinity_node]=max(previous_value_of_temp_infinity_node-progress_with_temp_infinity_node,0)
            else:
                del my_edges_to_crunch[continuation_of_temp_infinity_node]

        self.edges_to_crunch=my_edges_to_crunch

        return added_nodes
"""
    Removing:

    def get_edge_on_path(self,node,path,max_distance=Infinity):
        \"""
        Given a node, finds the edge that is a descendant of it and is on "path".
        Only an edge with a distance of at most max_distance is returned.
        Returns a dict of the form {node:distance}
        \"""
        current=node
        i=0
        while i<max_distance+1:
            try:
                current=path.next_node(current)
            except IndexError:
                return {current:i}
            i+=1
        return {}

    def crunch_on_path(self,node,wanted_distance,path):
        \"""
        Orders to start crunching from the edge of the path on which "node" lies,
        so that there will be a buffer whose length is at least "wanted_distance".
        \"""
        edge_dict=get_edge_on_path(node,wanted_distance) # This dict may have a maximum of one item
        for (edge,distance) in edges.items():
            new_distance=wanted_distance-distance
            if self.edges_to_crunch.has_key(edge):
                self.edges_to_crunch[edge]=max(new_distance,self.edges_to_crunch[edge])
            else:
                self.edges_to_crunch[edge]=new_distance
"""