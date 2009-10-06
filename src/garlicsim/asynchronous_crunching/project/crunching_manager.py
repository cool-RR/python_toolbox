# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
This module defines the CrunchingManager class. See its documentation for more
information.
"""

import garlicsim
import garlicsim.misc.queue_tools as queue_tools
from garlicsim.misc.infinity import FunnyInfinity
from crunchers import CruncherThread, CruncherProcess
from garlicsim.misc.infinity import Infinity

PreferredCruncher = [CruncherThread, CruncherProcess][1]
# Should make a nicer way of setting that.

__all__ = ["CrunchingManager"]

def with_tree_lock(method):
    """
    A decorator used in CrunchingManager's methods to use the tree lock (in
    write mode) as a context manager when calling the method.
    """
    def fixed(self, *args, **kwargs):
        with self.project.tree_lock.write:
            return method(self, *args, **kwargs)
    return fixed

class CrunchingManager(object):
    """
    A crunching manager manages the background crunching for a project.
    Every project creates a crunching manager. The job of the crunching manager
    is to coordinate the crunchers, creating and retiring them as necessary.
    The main use of a crunching manager is through its sync_workers methods,
    which goes over all the crunchers and all the leaves of the tree that need
    to be crunched, making sure the crunchers are working exactly on these
    leaves, and collecting work from them to implement into the tree.
    """
    def __init__(self, project):        
        self.project = project
        
        if project.simpack_grokker.history_dependent:
            self.Cruncher = CruncherThread
        else:
            self.Cruncher = PreferredCruncher
        
        self.crunchers = {}
        """
        A dict that maps nodes that should be worked on to crunchers.
        """
        
    @with_tree_lock
    def sync_crunchers(self, temp_infinity_node=None):
        """
        Talks with all the crunchers, takes work from them for implementing
        into the tree, retiring crunchers or recruiting new crunchers as
        necessary.
        You can specify a node to be a `temp_infinity_node`. That will cause
        sync_crunchers to temporarily treat this node as if it should be crunched
        indefinitely. This is useful when the simulation is playing back on
        a path that leads to this node, and we want to have as big a buffer
        as possible on that path.

        Returns the total amount of nodes that were added to the tree in the
        process.
        
        todo: maybe only the cruncher will be responsible for stopping when
        it's done? It's no dumb drone no more.
        """
        tree = self.project.tree
        nodes_to_crunch = self.project.nodes_to_crunch
        
        if temp_infinity_node:            
            temp_infinity_profile = nodes_to_crunch.setdefault(
                temp_infinity_node,
                garlicsim.CrunchingProfile()
            )
            temp_infinity_profile.nodes_distance += FunnyInfinity
            temp_infinity_profile.clock_distance += FunnyInfinity
            
        total_added_nodes = 0

        for (leaf, cruncher) in self.crunchers.copy().items():
            if not (leaf in nodes_to_crunch):
                (added_nodes, new_leaf) = \
                    self.__add_work_to_tree(cruncher, leaf, retire=True)
                total_added_nodes += added_nodes
                del self.crunchers[leaf]


        for (leaf, profile) in nodes_to_crunch.copy().items():
            if self.crunchers.has_key(leaf) and self.crunchers[leaf].is_alive():

                cruncher = self.crunchers[leaf]
                
                (added_nodes, new_leaf) = self.__add_work_to_tree(cruncher, leaf)
                total_added_nodes += added_nodes
                del nodes_to_crunch[leaf]

                profile.nodes_distance -= added_nodes
                profile.clock_distance -= (new_leaf.state.clock - leaf.state.clock)
                
                if profile.clock_distance <= 0 and profile.nodes_distance <= 0:
                    cruncher.retire()
                    #cruncher.join() # todo: sure?
                    del self.crunchers[leaf]
                else:
                    nodes_to_crunch[new_leaf] = profile
                    
                    del self.crunchers[leaf]
                    self.crunchers[new_leaf] = cruncher

            else:
                # Create cruncher
                if leaf.still_in_editing is False:
                    cruncher = self.crunchers[leaf] = \
                             self.__create_cruncher(leaf, profile)

        if temp_infinity_node:
            temp_infinity_profile.nodes_distance -= FunnyInfinity
            temp_infinity_profile.clock_distance -= FunnyInfinity

        return total_added_nodes
        
    def __create_cruncher(self, node, crunching_profile=None):
        """
        Creates a cruncher and tells it to start working on `node`. TODO
        """
        step_function = self.project.simpack_grokker.step
        
        if self.Cruncher == CruncherProcess:
            cruncher = self.Cruncher \
                     (node.state, self.project.simpack_grokker.step_generator,
                      crunching_profile=crunching_profile)
        
        else: # self.Cruncher == CruncherThread
            cruncher = self.Cruncher(node.state, self.project)
            
        cruncher.start()
        return cruncher
    
    def __add_work_to_tree(self, cruncher, node, retire=False):
        """
        Takes work from the cruncher and adds to the tree at the specified
        node. If `retire` is set to True, retires the cruncher.
        
        Returns (number, leaf), where `number` is the number of nodes that
        were added, and `leaf` is the last node that was added.
        """
        tree = self.project.tree
        states = queue_tools.dump_queue(cruncher.work_queue)
        if retire:
            cruncher.retire()
        current = node
        for state in states:
            current = tree.add_state(state, parent=current)
        return (len(states), current)