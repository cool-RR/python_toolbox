# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
This module defines the Project class. See its documentation for more
information.
"""

import garlicsim.data_structures
import garlicsim.misc.simpack_grokker
import crunching_manager

import garlicsim.general_misc.read_write_lock as read_write_lock
from garlicsim.general_misc.infinity import Infinity
import garlicsim.general_misc.module_wrapper
import garlicsim.general_misc.third_party.decorator

__all__ = ["Project"]


@garlicsim.general_misc.third_party.decorator.decorator
def with_tree_lock(method, *args, **kwargs):
    """
    A decorator used in Project's methods to use the tree lock (in write mode)
    as a context manager when calling the method.
    """
    self = args[0]
    with self.tree_lock.write:
        return method(*args, **kwargs)
        
    
class Project(object):
    """
    You create a project when you want to do a simulation which will crunch
    in the background with worker threads or worker processes.

    A project contains within it a tree.
        
    The crunching is taken care of by the CrunchingManager which is a part of
    every project. The CrunchingManager employs CruncherThreads and/or
    CruncherProcesses to get the work done. To make the CrunchingManager take
    work from the crunchers and coordinate them, call the sync_crunchers method
    of the project.
    
    What the crunching manager's sync_crunchers method will do is check the
    attribute .nodes_to_crunch of the project. This attribute is a dict 
    which maps nodes that should be crunched to a TODO. The crunching manager will
    then coordinate the crunchers in order to do this work. It will update the
    .nodes_to_crunch attribute when the crunchers have completed some of the
    work.
    """

    def __init__(self, simpack):
        
        wrapped_simpack = \
            garlicsim.general_misc.module_wrapper.module_wrapper_factory \
            (simpack)
        
        self.simpack = wrapped_simpack
        
        self.simpack_grokker = \
            garlicsim.misc.simpack_grokker.SimpackGrokker(wrapped_simpack)        

        self.tree = garlicsim.data_structures.Tree()
        
        self.crunching_manager = crunching_manager.CrunchingManager(self)
        
        self.tree_lock = read_write_lock.ReadWriteLock()
        """
        The tree_lock is a read-write lock that guards access to the tree.
        We need such a thing because some simulations are history-dependent
        and require reading from the tree in the same time that sync_crunchers
        could potentially be writing to it.
        """

        self.nodes_to_crunch = {}
        """
        A dict that maps leaves that should be worked on to a crunching
        profile.
        """

    def make_plain_root(self, *args, **kwargs):
        """
        Create a parentless node whose state is a simple plain state.
        
        The simulation package has to define the function `make_plain_state`
        for this to work.
        
        Returns the node.
        """
        state = self.simpack.make_plain_state(*args, **kwargs)
        return self.root_this_state(state)

    def make_random_root(self, *args, **kwargs):
        """
        Creates a parentless node whose state is a random and messy state.
        
        The simulation package has to define the function `make_random_state`
        for this to work.
        
        Returns the node.
        """
        state = self.simpack.make_random_state(*args, **kwargs)
        return self.root_this_state(state)

    def root_this_state(self, state):
        """
        Take a state, wrap it in a node and add to the tree without a parent.
        
        Returns the node.
        """
        return self.tree.add_state(state)

    def crunch_all_leaves(self, node, wanted_clock_distance=0): #todo: specify profile
        """
        Crunch all the leaves of `node`.
        
        The leaves of `node` will be crunched to the point where there's a
        buffer of `wanted_clock_distance` between `node` and each of its
        leaves.
        """
        leaves = node.get_all_leaves(max_clock_distance=wanted_clock_distance)
        new_clock_target = node.state.clock + wanted_clock_distance
        for item in leaves.items():
            
            leaf = item[0]
            
            crunching_profile = \
                self.nodes_to_crunch.setdefault(
                    leaf,
                    garlicsim.asynchronous_crunching.CrunchingProfile()
                )
            
            crunching_profile.clock_target = max(
                crunching_profile.clock_target,
                new_clock_target
            )
                

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
        return self.crunching_manager.sync_crunchers \
               (temp_infinity_node=temp_infinity_node)
    
    @with_tree_lock
    def simulate(self, node, iterations=1, *args, **kwargs):
        """
        Simulates from the given node for the given number of iterations.
        
        The results are implemented the results into the tree. Note that the
        crunching for this is done synchronously, i.e. in the currrent thread.
        
        Any extraneous parameters will be passed to the step function.
        
        Returns the final node.
        """
        
        if self.simpack_grokker.history_dependent:
            return self.__history_dependent_simulate(node, iterations,
                                                     *args, **kwargs)
        else:
            return self.__non_history_dependent_simulate(node, iterations,
                                                         *args, **kwargs)
        
    def __history_dependent_simulate(self, node, iterations=1,
                                     *args, **kwargs):
        """
        For history-dependent simulations only:
        
        Simulates from the given node for the given number of iterations.
        
        The results are implemented the results into the tree. Note that the
        crunching for this is done synchronously, i.e. in the currrent thread.
        
        Any extraneous parameters will be passed to the step function.
        
        Returns the final node.
        """
        
        path = node.make_containing_path()
        history_browser = garlicsim.synchronous_crunching.\
                        history_browser.HistoryBrowser(path)
        current_node = node
        state = node.state
        for i in range(iterations):
            state = self.simpack_grokker.step(history_browser,
                                              *args, **kwargs)
            current_node = self.tree.add_state(state, parent=current_node)
            
        return current_node
    
    def __non_history_dependent_simulate(self, node, iterations=1,
                                         *args, **kwargs):
        """
        For non-history-dependent simulations only:
        
        Simulates from the given node for the given number of iterations.
        
        The results are implemented the results into the tree. Note that the
        crunching for this is done synchronously, i.e. in the currrent thread.
        
        Any extraneous parameters will be passed to the step function.
        
        Returns the final node.
        """
        
        current_node = node
        state = node.state
        for i in range(iterations):
            state = self.simpack_grokker.step(state, *args, **kwargs)
            current_node = self.tree.add_state(state, parent=current_node)
            
        return current_node
    
    def __getstate__(self):
        my_dict = dict(self.__dict__)
        
        del my_dict["tree_lock"]
        del my_dict["crunching_manager"]
        
        return my_dict
    
    def __setstate__(self, pickled_project):
        self.__init__(pickled_project["simpack"])
        self.__dict__.update(pickled_project)
        
        
        
        
        
        