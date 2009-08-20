"""


todo:
maybe path belongs in Project and not GuiProject?


    todo: specify arguments to step function

todo: more sophisticated version of `leaves_to_crunch`.

"""

import random
import state
import misc.readwritelock as readwritelock
from simpackgrokker import SimpackGrokker
from crunchers import CruncherThread, CruncherProcess
from misc.queuetools import dump_queue
from misc.infinity import Infinity # Same as Infinity=float("inf")

PreferredCruncher = [CruncherThread, CruncherProcess][1]


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

    def __init__(self, simpack):
        
        self.simpack_grokker = SimpackGrokker(simpack)
        self.simpack = simpack

        self.tree=state.Tree()
        self.tree_lock = readwritelock.ReadWriteLock()
        #self.cruncher_mapping_lock = coolreadwritelock.CoolReadWriteLock()

        if self.simpack_grokker.history_dependent:
            self.Cruncher = CruncherThread
        else:
            self.Cruncher = PreferredCruncher

        self.workers={} #rename to crunchers
        """
        A dict that maps leaves that should be worked on to workers.
        """

        self.leaves_to_crunch={} 
        """
        A dict that maps leaves that should be worked on to a number specifying
        how many nodes should be created after them.
        """

    def make_plain_root(self,*args,**kwargs):
        """
        Creates a parent-less node, whose state is a simple plain state.
        The simulation package should define the function `make_plain_state`
        for this to work.
        Returns the node.
        """
        state=self.simpack.make_plain_state(*args,**kwargs)
        state._State__touched = True
        return self.root_this_state(state)

    def make_random_root(self,*args,**kwargs):
        """
        Creates a parent-less node, whose state is a random and messy state.
        The simulation package  should define the function `make_random_state`
        for this to work.
        Returns the node.
        """
        state=self.simpack.make_random_state(*args,**kwargs)
        state._State__touched = True
        return self.root_this_state(state)

    def root_this_state(self,state):
        """
        Takes a state, wraps it in a node and adds to the Tree without a parent.
        Returns the node.
        """
        return self.tree.add_state(state)

    def crunch_all_leaves(self,node,wanted_distance):
        """
        Orders to start crunching from all the leaves of "node",
        so that there will be a buffer whose length
        is at least "wanted_distance".
        """
        leaves=node.get_all_leaves(wanted_distance)
        for (leaf,distance) in leaves.items():
            new_distance=wanted_distance-distance
            if self.leaves_to_crunch.has_key(leaf):
                self.leaves_to_crunch[leaf]=max(new_distance,self.leaves_to_crunch[leaf])
            else:
                self.leaves_to_crunch[leaf]=new_distance


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

        with self.tree_lock.write:
            my_leaves_to_crunch=self.leaves_to_crunch.copy()
    
            if temp_infinity_node!=None:
                if self.leaves_to_crunch.has_key(temp_infinity_node):
                    had_temp_infinity_node=True
                    previous_value_of_temp_infinity_node=self.leaves_to_crunch[temp_infinity_node]
                else:
                    had_temp_infinity_node=False
                my_leaves_to_crunch[temp_infinity_node]=Infinity
    
    
            added_nodes=0
    
            for leaf in self.workers.copy():
                if not (leaf in my_leaves_to_crunch):
                    worker=self.workers[leaf]
                    result=dump_queue(worker.work_queue)
    
                    worker.retire()
    
                    current=leaf
                    for state in result:
                        current=self.tree.add_state(state,parent=current)
                    added_nodes+=len(result)
    
                    del self.workers[leaf]
                    #worker.join() # todo: sure?
    
    
    
            for (leaf,number) in my_leaves_to_crunch.items():
                if self.workers.has_key(leaf) and self.workers[leaf].is_alive():
    
                    worker=self.workers[leaf]
                    result=dump_queue(worker.work_queue)
    
                    current=leaf
                    for state in result:
                        current=self.tree.add_state(state,parent=current)
                    added_nodes+=len(result)
    
                    del my_leaves_to_crunch[leaf]
    
    
                    if number!=Infinity: # Maybe this is just a redundant dichotomy from before I had Infinity?
                        new_number=number-len(result)
                        if new_number<=0:
                            worker.retire()
                            #worker.join() # todo: sure?
                            del self.workers[leaf]
                        else:
                            my_leaves_to_crunch[current]=new_number
                            del self.workers[leaf]
                            self.workers[current]=worker
    
                    else:
                        my_leaves_to_crunch[current]=Infinity
                        del self.workers[leaf]
                        self.workers[current]=worker
    
                    if leaf==temp_infinity_node:
                        continuation_of_temp_infinity_node=current
                        progress_with_temp_infinity_node=len(result)
    
    
    
    
                else:
                    # Create worker
                    if leaf.still_in_editing==False:
                        worker=self.workers[leaf] = self.create_cruncher(leaf)
                        worker.start()
                    if leaf==temp_infinity_node:
                        continuation_of_temp_infinity_node=leaf
                        progress_with_temp_infinity_node=0
    
            if temp_infinity_node!=None:
                if had_temp_infinity_node:
                    my_leaves_to_crunch[continuation_of_temp_infinity_node]=max(previous_value_of_temp_infinity_node-progress_with_temp_infinity_node,0)
                else:
                    del my_leaves_to_crunch[continuation_of_temp_infinity_node]
    
            self.leaves_to_crunch=my_leaves_to_crunch
    
            return added_nodes
    
    def create_cruncher(self, node):
        if self.Cruncher == CruncherProcess:
            return self.Cruncher(node.state, step_function=self.simpack_grokker.step)
        else: # self.Cruncher == CruncherThread
            return self.Cruncher(node.state, self, step_function=self.simpack_grokker.step)
    
    def step(self,source_node):
        """
        Takes a node and simulates a child node from it.
        This is NOT done in the background.
        Returns the child node.
        """
        with self.tree_lock.write:
            if self.simpack_grokker.history_dependent:
                raise NotImplementedError
            else:
                new_state = self.simpack_grokker.step(source_node.state)
                return self.tree.add_state(new_state, source_node)

"""
    Removing:

    def multistep(self,source_node,steps=1):
        \"""
        Takes a node and simulates a succession of child nodes from it.
        `steps` specifies how many nodes.
        This is NOT done in the background.
        Returns the last node.
        \"""
        my_node=source_node
        for i in range(steps):
            my_node=self.step(my_node)
        return my_node
"""