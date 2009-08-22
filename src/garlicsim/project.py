"""
This module defines a class Project. See this class's documentation
for more info
"""

import state
import simpackgrokker
import crunchingmanager

import misc.readwritelock as readwritelock
from misc.infinity import Infinity # Same as Infinity=float("inf")


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
        
        self.crunching_manager = crunchingmanager.CrunchingManager(self)
        
        self.tree_lock = readwritelock.ReadWriteLock()
        """
        The tree_lock is a read-write lock that guards access to the tree.
        We need such a thing because some simulations are history-dependent
        and require reading from the tree in the same time that sync_crunchers
        could potentially be writing to it.
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
        state = self.simpack.make_plain_state(*args, **kwargs)
        state._State__touched = True
        return self.root_this_state(state)

    def make_random_root(self, *args, **kwargs):
        """
        Creates a parent-less node, whose state is a random and messy state.
        The simulation package should define the function `make_random_state`
        for this to work.
        Returns the node.
        """
        state = self.simpack.make_random_state(*args, **kwargs)
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
        
        return self.crunching_manager.sync_crunchers(temp_infinity_node=temp_infinity_node)
    

    
    

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