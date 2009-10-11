# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
This module defines the CrunchingManager class. See its documentation for more
information.
"""

from __future__ import with_statement

import garlicsim
import garlicsim.general_misc.dict_tools
import garlicsim.general_misc.queue_tools as queue_tools
from crunchers import CruncherThread, CruncherProcess
from crunching_profile import CrunchingProfile
from garlicsim.general_misc.infinity import Infinity


PreferredCruncher = [CruncherThread, CruncherProcess][1]
# Should make a nicer way of setting that.

__all__ = ["CrunchingManager"]

def with_tree_lock(method):
    """
    A decorator used in CrunchingManager's methods to use the tree lock (in
    write mode) as a context manager when calling the method.
    
    todo: This decorator fucks up documentation, search internet
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
    which goes over all the crunchers and all the nodes of the tree that need
    to be crunched, making sure the crunchers are working on these nodes, and
    collecting work from them to implement into the tree.
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
        
        self.old_nodes_to_crunch = {}
        """
        Here we store a copy of the `.nodes_to_crunch` attribute of the
        project. This is used to tell whether the project updated its
        crunching profiles, and if so we should update the crunchers' profiles.
        """
        
    @with_tree_lock
    def sync_crunchers(self, temp_infinity_node=None):
        """
        Take work from the crunchers, and give them new instructions if needed.
        
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
        """
        tree = self.project.tree
        nodes_to_crunch = self.project.nodes_to_crunch
        
        if temp_infinity_node:
            
            had_temp_infinity_node = \
                nodes_to_crunch.has_key(temp_infinity_node)

            if had_temp_infinity_node:
                
                old_temp_infinity_node_clock_target = \
                    nodes_to_crunch[temp_infinity_node].clock_target
                
                nodes_to_crunch[temp_infinity_node].clock_target = Infinity
                
            else:
                
                nodes_to_crunch[temp_infinity_node] = \
                    CrunchingProfile(clock_target=Infinity)
            
            
        total_added_nodes = self.__sync_crunchers(temp_infinity_node)
                    
                        

        if temp_infinity_node:
            
            leaves = temp_infinity_node.get_all_leaves()
            assert len(leaves) == 1 # maybe just warn here?
            (leaf, distances) = leaves.popitem()
            clock_distance = distances["clock_distance"]
            
            if had_temp_infinity_node:    
                nodes_to_crunch[leaf].clock_target = \
                    old_temp_infinity_node_clock_target - clock_distance
            else:
                del nodes_to_crunch[leaf]

        self.__make_old_nodes_to_crunch()
                
        return total_added_nodes
        
    def __sync_crunchers(self, temp_infinity_node):
        """
        Used by sync_crunchers. Does the actual work of syncing the crunchers.
        """
        #todo: should not get temp_infinity_node!
        
        #todo: will the cruncher of a temp_infinity_node stop after finite time
        
        nodes_to_crunch = self.project.nodes_to_crunch
        
        total_added_nodes = 0

        for (node, cruncher) in self.crunchers.copy().items():
            if not (node in nodes_to_crunch):
                (added_nodes, new_leaf) = \
                    self.__add_work_to_tree(cruncher, node, retire=True)
                total_added_nodes += added_nodes
                del self.crunchers[node]


        for (node, profile) in nodes_to_crunch.copy().items():
            
            if self.crunchers.has_key(node) is False:
                self.__conditional_create_cruncher(node, profile)
                continue

            # self.crunchers.has_key(node) is True
            
            cruncher = self.crunchers[node]
            
            (added_nodes, new_leaf) = self.__add_work_to_tree(cruncher, node)
            total_added_nodes += added_nodes

            del nodes_to_crunch[node]
            del self.crunchers[node]
            
            
            if profile.state_satisfies(new_leaf.state):
                if cruncher.is_alive():
                    cruncher.retire()
                
            else:
                nodes_to_crunch[new_leaf] = profile
                if cruncher.is_alive():
                    old_profile = self.old_nodes_to_crunch.get(node, None)
                    if (old_profile != profile) and \
                       (node != temp_infinity_node):
                        cruncher.update_crunching_profile(profile)                        
                    self.crunchers[new_leaf] = cruncher
                else:
                    self.__conditional_create_cruncher(new_leaf, profile)
                    
        return total_added_nodes
    
    def __make_old_nodes_to_crunch(self):
        '''
        Make and store a copy of the .nodes_to_crunch attribute of the project.
        
        This is used to tell whether the project updated its crunching
        profiles, and if so we should update the crunchers' profiles.
        '''
        self.old_nodes_to_crunch = garlicsim.general_misc.dict_tools.deepcopy_values(
            self.project.nodes_to_crunch
        )
    
    def __conditional_create_cruncher(self, node, crunching_profile=None):
        '''
        Create a cruncher to crunch the node, unless there is reason not to.
        '''
        if node.still_in_editing is False:
            step_function = self.project.simpack_grokker.step
            if self.Cruncher == CruncherProcess:
                cruncher = self.Cruncher \
                         (node.state,
                          self.project.simpack_grokker.step_generator,
                          crunching_profile=crunching_profile)
            else: # self.Cruncher == CruncherThread
                cruncher = self.Cruncher(node.state, self.project,
                                         crunching_profile=crunching_profile)
            cruncher.start()
            self.crunchers[node] = cruncher
            return cruncher
        
    
    def __add_work_to_tree(self, cruncher, node, retire=False):
        """
        Take work from the cruncher and add to the tree at the specified node.
        
        If `retire` is set to True, retires the cruncher.
        
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