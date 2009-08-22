"""
This module defines a class Project. See this class's documentation
for more info
"""

import state
import simpackgrokker
from crunchers import CruncherThread, CruncherProcess

import misc.readwritelock as readwritelock
import misc.queuetools as queuetools
from misc.infinity import Infinity # Same as Infinity=float("inf")

PreferredCruncher = [CruncherThread, CruncherProcess][1]
# Should be a nicer way of setting that.

__all__ = ["Project"]

class Project(object):
    """
    `Project` is the main class that the garlicsim package defines.
    When you want to do a simulation, you create a Project. All your
    work is done within this Project.

    A Project encapsulates a Tree.

    A Project, among other things, takes care of background
    crunching of the simulation, using threads and/or processes.
    A Project employs "crunchers", which are either threads or processes,
    and which crunch the simulation in the background.
    The Project is responsible for coordinating the crunchers. The method
    sync_crunchers makes the Project review the work done by the crunchers,
    implement it into the Tree, and retire/employ them as necessary.

    The Project class does not require wxPython or any other
    GUI package: It can be used entirely from the Python command-line.
    """

    def __init__(self, simpack):
        
        self.simpack_grokker = simpackgrokker.SimpackGrokker(simpack)
        self.simpack = simpack

        self.tree=state.Tree()
        
        self.tree_lock = readwritelock.ReadWriteLock()
        """
        The tree_lock is a read-write lock that guards access to the tree.
        We need such a thing because some simulations are history-dependent
        and require reading from the tree in the same time that sync_crunchers
        could potentially be writing to it.
        """
        

        if self.simpack_grokker.history_dependent:
            self.Cruncher = CruncherThread
        else:
            self.Cruncher = PreferredCruncher

        self.crunchers = {}
        """
        A dict that maps leaves that should be worked on to crunchers.
        """

        self.leaves_to_crunch = {} 
        """
        A dict that maps leaves that should be worked on to a number specifying
        how many nodes should be created after them.
        """

    def make_plain_root(self, *args, **kwargs):
        """
        Creates a parent-less node, whose state is a simple plain state.
        The simulation package should define the function `make_plain_state`
        for this to work.
        Returns the node.
        """
        state = self.simpack.make_plain_state(*args,**kwargs)
        state._State__touched = True
        return self.root_this_state(state)

    def make_random_root(self, *args, **kwargs):
        """
        Creates a parent-less node, whose state is a random and messy state.
        The simulation package should define the function `make_random_state`
        for this to work.
        Returns the node.
        """
        state = self.simpack.make_random_state(*args,**kwargs)
        state._State__touched = True
        return self.root_this_state(state)

    def root_this_state(self, state):
        """
        Takes a state, wraps it in a node and adds to the Tree without
        a parent.
        Returns the node.
        """
        return self.tree.add_state(state)

    def crunch_all_leaves(self, node, wanted_distance):
        """
        Orders to start crunching from all the leaves of `node`,
        so that there will be a buffer whose length
        is at least `wanted_distance`.
        """
        leaves = node.get_all_leaves(wanted_distance)
        for (leaf, distance) in leaves.items():
            new_distance = wanted_distance - distance
            if self.leaves_to_crunch.has_key(leaf):
                self.leaves_to_crunch[leaf] = \
                    max(new_distance, self.leaves_to_crunch[leaf])
            else:
                self.leaves_to_crunch[leaf] = new_distance


    def sync_crunchers(self, temp_infinity_node=None):
        """
        Talks with all the crunchers, takes work from them for
        implementing into the Tree, terminates crunchers or creates
        new crunchers if necessary.
        You can pass a node as `temp_infinity_node`. That will cause this
        function to temporarily treat this node as if it should be crunched
        indefinitely.

        Returns the total amount of nodes that were added to the tree.
        """

        with self.tree_lock.write:
            my_leaves_to_crunch = self.leaves_to_crunch.copy()
    
            if temp_infinity_node:
                if self.leaves_to_crunch.has_key(temp_infinity_node):
                    had_temp_infinity_node = True
                    previous_value_of_temp_infinity_node = \
                            self.leaves_to_crunch[temp_infinity_node]
                else:
                    had_temp_infinity_node = False
                my_leaves_to_crunch[temp_infinity_node] = Infinity
    
    
            added_nodes = 0
    
            for leaf in self.crunchers.copy():
                if not (leaf in my_leaves_to_crunch):
                    cruncher = self.crunchers[leaf]
                    result = queuetools.dump_queue(cruncher.work_queue)
    
                    cruncher.retire()
    
                    current = leaf
                    for state in result:
                        current = self.tree.add_state(state, parent=current)
                    added_nodes += len(result)
    
                    del self.crunchers[leaf]
                    #cruncher.join() # todo: sure?
    
    
    
            for (leaf, number) in my_leaves_to_crunch.items():
                if self.crunchers.has_key(leaf) and self.crunchers[leaf].is_alive():
    
                    cruncher = self.crunchers[leaf]
                    result = queuetools.dump_queue(cruncher.work_queue)
    
                    current = leaf
                    for state in result:
                        current = self.tree.add_state(state, parent=current)
                    added_nodes += len(result)
    
                    del my_leaves_to_crunch[leaf]
    
    
                    if number != Infinity: # Maybe this is just a redundant dichotomy from before I had Infinity?
                        new_number = number - len(result)
                        if new_number <= 0:
                            cruncher.retire()
                            #cruncher.join() # todo: sure?
                            del self.crunchers[leaf]
                        else:
                            my_leaves_to_crunch[current] = new_number
                            del self.crunchers[leaf]
                            self.crunchers[current] = cruncher
    
                    else:
                        my_leaves_to_crunch[current] = Infinity
                        del self.crunchers[leaf]
                        self.crunchers[current] = cruncher
    
                    if leaf == temp_infinity_node:
                        continuation_of_temp_infinity_node = current
                        progress_with_temp_infinity_node = len(result)
    
    
    
    
                else:
                    # Create cruncher
                    if leaf.still_in_editing is False:
                        cruncher=self.crunchers[leaf] = self.create_cruncher(leaf)
                    if leaf == temp_infinity_node:
                        continuation_of_temp_infinity_node = leaf
                        progress_with_temp_infinity_node = 0
    
            if temp_infinity_node:
                if had_temp_infinity_node:
                    my_leaves_to_crunch[continuation_of_temp_infinity_node]=max(previous_value_of_temp_infinity_node-progress_with_temp_infinity_node,0)
                else:
                    del my_leaves_to_crunch[continuation_of_temp_infinity_node]
    
            self.leaves_to_crunch=my_leaves_to_crunch
    
            return added_nodes
    
    def create_cruncher(self, node):
        """
        Creates a cruncher and tells it to start working on `node`.
        """
        if self.Cruncher == CruncherProcess:
            cruncher = self.Cruncher(node.state,
                                     step_function=self.simpack_grokker.step)
        
        else: # self.Cruncher == CruncherThread
            cruncher = self.Cruncher(node.state, self,
                                    step_function=self.simpack_grokker.step)
        cruncher.start()
        return cruncher
    
    

"""
    Removing:
    
    def step(self,source_node):
        \"""
        Takes a node and simulates a child node from it.
        This is NOT done in the background.
        Returns the child node.
        \"""
        with self.tree_lock.write:
            if self.simpack_grokker.history_dependent:
                raise NotImplementedError
            else:
                new_state = self.simpack_grokker.step(source_node.state)
                return self.tree.add_state(new_state, source_node)
                
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