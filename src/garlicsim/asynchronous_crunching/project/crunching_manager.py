# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
This module defines the CrunchingManager class. See its documentation for more
information.
"""

import garlicsim.misc.queue_tools as queue_tools
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
        
        todo: should rethink how this entire operation works.
        """
        tree = self.project.tree
        my_nodes_to_crunch = self.project.nodes_to_crunch.copy()

        if temp_infinity_node:
            if self.project.nodes_to_crunch.has_key(temp_infinity_node):
                had_temp_infinity_node = True
                previous_value_of_temp_infinity_node = \
                        self.project.nodes_to_crunch[temp_infinity_node]
            else:
                had_temp_infinity_node = False
            my_nodes_to_crunch[temp_infinity_node] = Infinity

        total_added_nodes = 0

        for leaf in self.crunchers.copy():
            if not (leaf in my_nodes_to_crunch):
                cruncher = self.crunchers[leaf]
                (added_nodes, new_leaf) = self.__add_work_to_tree(cruncher, leaf, retire=True)
                total_added_nodes += added_nodes
                
                del self.crunchers[leaf]



        for (leaf, number) in my_nodes_to_crunch.items():
            if self.crunchers.has_key(leaf) and self.crunchers[leaf].is_alive():

                cruncher = self.crunchers[leaf]
                
                (added_nodes, new_leaf) = self.__add_work_to_tree(cruncher, leaf)
                total_added_nodes += added_nodes
                del my_nodes_to_crunch[leaf]


                new_number = number - added_nodes
                if new_number <= 0:
                    cruncher.retire()
                    #cruncher.join() # todo: sure?
                    del self.crunchers[leaf]
                else:
                    my_nodes_to_crunch[new_leaf] = new_number
                    del self.crunchers[leaf]
                    self.crunchers[new_leaf] = cruncher

                if leaf == temp_infinity_node:
                    continuation_of_temp_infinity_node = new_leaf
                    progress_with_temp_infinity_node = added_nodes


            else:
                # Create cruncher
                if leaf.still_in_editing is False:
                    cruncher = self.crunchers[leaf] = \
                             self.__create_cruncher(leaf)
                if leaf == temp_infinity_node:
                    continuation_of_temp_infinity_node = leaf
                    progress_with_temp_infinity_node = 0

        if temp_infinity_node:
            if had_temp_infinity_node:
                temp = max(previous_value_of_temp_infinity_node - \
                           progress_with_temp_infinity_node, 0)
                
                my_nodes_to_crunch[continuation_of_temp_infinity_node] = temp
                                   
            else:
                del my_nodes_to_crunch[continuation_of_temp_infinity_node]

        self.project.nodes_to_crunch = my_nodes_to_crunch

        return total_added_nodes
        
    def __create_cruncher(self, node):
        """
        Creates a cruncher and tells it to start working on `node`.
        """
        step_function = self.project.simpack_grokker.step
        
        if self.Cruncher == CruncherProcess:
            cruncher = self.Cruncher \
                     (node.state, self.project.simpack_grokker.step_generator)
        
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