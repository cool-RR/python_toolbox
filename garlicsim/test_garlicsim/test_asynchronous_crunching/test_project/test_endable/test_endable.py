# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.


from __future__ import division

import os
import types
import time
import itertools
import cPickle, pickle

import nose

from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc import math_tools
from garlicsim.general_misc import path_tools
from garlicsim.general_misc import import_tools
from garlicsim.general_misc.infinity import Infinity

import garlicsim

#from .shared import MustachedThreadCruncher

FUZZ = 0.0001
'''Fuzziness of floats.'''



def test_endable():
    
    from . import sample_endable_simpacks
    
    # Collecting all the test simpacks:
    simpacks = import_tools.import_all(sample_endable_simpacks).values()
    
    # Making sure that we didn't miss any simpack by counting the number of
    # sub-folders in the `sample_simpacks` folders:
    sample_endable_simpacks_dir = \
        os.path.dirname(sample_endable_simpacks.__file__)
    assert len(path_tools.list_sub_folders(sample_endable_simpacks_dir)) == \
           len(simpacks)
    
    cruncher_types = [
        garlicsim.asynchronous_crunching.crunchers.ThreadCruncher,
        
        # Until multiprocessing shit is solved, this is commented-out:
        #garlicsim.asynchronous_crunching.crunchers.ProcessCruncher
    ]
    
    
    for simpack, cruncher_type in \
        cute_iter_tools.product(simpacks, cruncher_types):
        
        yield check, simpack, cruncher_type

        
def check(simpack, cruncher_type):
    
    # tododoc: note somewhere visible: all simpacks end when they see a
    # world-state with clock reading of 4 or more.
    
    my_simpack_grokker = garlicsim.misc.SimpackGrokker(simpack)
    
    assert my_simpack_grokker is garlicsim.misc.SimpackGrokker(simpack)
    # Ensuring caching works.
    
    step_profile = my_simpack_grokker.build_step_profile()
    deterministic = \
        my_simpack_grokker.settings.DETERMINISM_FUNCTION(step_profile)
    
    state = simpack.State.create_root()
    
    ### First, let's run for short periods so it doesn't end: #################
    #                                                                         #
    
    # Whether we run the simulation for one, two, three, or four iterations, the
    # simulation doesn't end.
    prev_state = state
    for i in [1, 2, 3, 4]:
        new_state = garlicsim.simulate(state, i)
        assert new_state.clock >= getattr(prev_state, 'clock', 0)
        prev_state = new_state
    
    result = garlicsim.list_simulate(state, 4)
    for item in result:
        assert isinstance(item, garlicsim.data_structures.State)
        assert isinstance(item, simpack.State)
    
    assert isinstance(result, list)
    assert len(result) == 5
        
    
    iter_result = garlicsim.iter_simulate(state, 4)
        
    assert not hasattr(iter_result, '__getitem__')
    assert hasattr(iter_result, '__iter__')
    iter_result_in_list = list(iter_result)
    del iter_result
    assert len(iter_result_in_list) == len(result) == 5
    
    #                                                                         #
    ### Done running for short periods so it doesn't end. #####################
    
    ### Now, let's run it for longer periods to make it end: ##################
    #                                                                         #
    
    for i in [5, 6, 7]:
        new_state = garlicsim.simulate(state, i)
        assert new_state.clock == 4
    
    result = garlicsim.list_simulate(state, 7)
    
    assert isinstance(result, list)
    assert len(result) == 5
        
    
    iter_result = garlicsim.iter_simulate(state, 7)
        
    assert not hasattr(iter_result, '__getitem__')
    assert hasattr(iter_result, '__iter__')
    iter_result_in_list = list(iter_result)
    del iter_result
    assert len(iter_result_in_list) == len(result) == 5
        
    #                                                                         #
    ### Done running for longer periods to make it end. #######################
    
    #project = garlicsim.Project(simpack)
    
    ## Ensure that `Project.__init__` can take simpack grokker:
    #alterante_project = garlicsim.Project(my_simpack_grokker)
    #project.simpack is alterante_project.simpack
    #project.simpack_grokker is alterante_project.simpack_grokker
    
    
    #project.crunching_manager.cruncher_type = cruncher_type
    
    #assert project.tree.lock._ReadWriteLock__writer is None
    
    #root = project.root_this_state(state)
    
    #project.begin_crunching(root, 4)

    #total_nodes_added = 0    
    #while project.crunching_manager.jobs:
        #time.sleep(0.1)
        #total_nodes_added += project.sync_crunchers()
        
    #x = total_nodes_added
    
    #if x < 4:
        ## For simpacks with long time intervals, we make sure at least 4 nodes
        ## were created.
        #path = root.make_containing_path()
        #leaf = path[-1]
        #project.simulate(
            #leaf,
            #math_tools.round_to_int(4 - x, up=True)
        #)
        #x += path.__len__(start=path.next_node(leaf))
            
    #assert len(project.tree.nodes) == x + 1
    #assert len(project.tree.roots) == 1
    
    #paths = project.tree.all_possible_paths()
    
    #assert len(paths) == 1
    
    #(my_path,) = paths
        
    #assert len(my_path) == x + 1
    
    #node_1 = my_path[1]
    
    #node_2 = project.simulate(node_1, 3)
    
    #assert len(project.tree.nodes) == x + 1 + 3
    #assert len(project.tree.roots) == 1
    
    #assert len(project.tree.all_possible_paths()) == 2
    
    #try:
        #pickled_project = pickle.dumps(project, protocol=2)
    #except RuntimeError as runtime_error:
        #assert 'maximum recursion' in runtime_error.message
    #else:
        #unpickled_project = cPickle.loads(pickled_project)
        #path_pairs = itertools.izip(project.tree.all_possible_paths(),
                                    #unpickled_project.tree.all_possible_paths())
        
        #if isinstance(
            #simpack.State.__eq__,
            #(types.FunctionType, types.MethodType, types.UnboundMethodType)
        #):
            
            #for path_of_original, path_of_duplicate in path_pairs:
                
                #state_pairs = itertools.izip(path_of_original.states(),
                                             #path_of_duplicate.states())
                #for state_of_original, state_of_duplicate in state_pairs:
                    
                    #assert state_of_original == state_of_duplicate
            
    
    
    #node_3 = my_path.next_node(node_1)
    
    #project.begin_crunching(node_3, 3)
    
    #total_nodes_added = 0
    #while project.crunching_manager.jobs:
        #time.sleep(0.1)
        #total_nodes_added += project.sync_crunchers()
    #y = total_nodes_added
        
    #if y < 3:
        ## For simpacks with long time intervals, we make sure at least 3 nodes
        ## were created.
        #path = node_3.make_containing_path()
        #leaf = path[-1]
        #project.simulate(
            #leaf,
            #math_tools.round_to_int(3 - y, up=True)
        #)
        #y += path.__len__(start=path.next_node(leaf))
    
    
    #assert len(project.tree.nodes) == x + y + 4
    
    #paths = project.tree.all_possible_paths()
    #assert len(paths) == 3
    
    #assert set(len(p) for p in paths) == set([5, x + 1, 3 + y])
    
    
    #project.ensure_buffer(node_3, 3)

    #total_nodes_added = 0
    #while project.crunching_manager.jobs:
        #time.sleep(0.1)
        #total_nodes_added += project.sync_crunchers()
    
    #assert len(project.tree.nodes) == x + y + 4 + total_nodes_added
    #assert len(project.tree.all_possible_paths()) == 3
    
    #assert project.tree.lock._ReadWriteLock__writer is None
    
    #two_paths = node_3.all_possible_paths()
    
    #assert len(two_paths) == 2
    #(path_1, path_2) = two_paths
    #get_clock_buffer = lambda path: (path[-1].state.clock - node_3.state.clock)
    #(clock_buffer_1, clock_buffer_2) = [get_clock_buffer(p) for p in two_paths]
    
    #project.ensure_buffer_on_path(node_3, path_1, get_clock_buffer(path_1) * 1.2)
    
    #total_nodes_added = 0
    #while project.crunching_manager.jobs:
        #time.sleep(0.1)
        #total_nodes_added += project.sync_crunchers()
    
    #(old_clock_buffer_1, old_clock_buffer_2) = (clock_buffer_1, clock_buffer_2)
    #(clock_buffer_1, clock_buffer_2) = [get_clock_buffer(p) for p in two_paths]
    
    #assert clock_buffer_1 / old_clock_buffer_1 >= 1.2 - FUZZ
    #assert clock_buffer_2 == old_clock_buffer_2
    
    #project.ensure_buffer_on_path(node_3, path_2, get_clock_buffer(path_2) * 1.3)
    
    #total_nodes_added = 0
    #while project.crunching_manager.jobs:
        #time.sleep(0.1)
        #total_nodes_added += project.sync_crunchers()
    
    #(old_clock_buffer_1, old_clock_buffer_2) = (clock_buffer_1, clock_buffer_2)
    #(clock_buffer_1, clock_buffer_2) = [get_clock_buffer(p) for p in two_paths]
    
    #assert clock_buffer_1 == old_clock_buffer_1
    #assert clock_buffer_2 / old_clock_buffer_2 >= 1.3 - FUZZ
    
    
    
    #plain_root = project.create_root()
    
    #assert len(project.tree.roots) == 2
    
    #assert len(project.tree.all_possible_paths()) == 4
    
    
    
    #assert project.tree.lock._ReadWriteLock__writer is None
    
    #number_of_nodes = len(project.tree.nodes)
    #iterator = project.iter_simulate(node_1, 10)
    
    #assert project.tree.lock._ReadWriteLock__writer is None
    
    #new_node = iterator.next()
    #assert new_node is node_1
    #assert len(project.tree.nodes) == number_of_nodes
    
    #assert project.tree.lock._ReadWriteLock__writer is None
    
    #new_node = iterator.next()
    #assert new_node is not node_1
    #assert new_node.parent is node_1
    #assert len(project.tree.nodes) == number_of_nodes + 1
    
    #bunch_of_new_nodes = tuple(iterator)
    #for parent_node, kid_node in cute_iter_tools.consecutive_pairs(bunch_of_new_nodes):
        #assert project.tree.lock._ReadWriteLock__writer is None
        #assert isinstance(parent_node, garlicsim.data_structures.Node)
        #assert isinstance(kid_node, garlicsim.data_structures.Node)
        #assert parent_node.children == [kid_node]
        #assert kid_node.parent is parent_node
        
    #assert len(project.tree.nodes) == number_of_nodes + 10
    
    #### Testing cruncher type switching: ######################################
    
    #job_1 = project.begin_crunching(root, clock_buffer=Infinity)
    #job_2 = project.begin_crunching(root, clock_buffer=Infinity)
    
    #assert len(project.crunching_manager.crunchers) == 0
    #assert project.sync_crunchers() == 0
    #assert len(project.crunching_manager.crunchers) == 2
    #(cruncher_1, cruncher_2) = project.crunching_manager.crunchers.values()
    #assert type(cruncher_1) is cruncher_type
    #assert type(cruncher_2) is cruncher_type
    
    #time.sleep(0.2) # Letting the crunchers start working
    
    #project.crunching_manager.cruncher_type = MustachedThreadCruncher
    #project.sync_crunchers()
    #assert len(project.crunching_manager.crunchers) == 2
    #(cruncher_1, cruncher_2) = project.crunching_manager.crunchers.values()
    #assert type(cruncher_1) is MustachedThreadCruncher
    #assert type(cruncher_2) is MustachedThreadCruncher
    
    #project.crunching_manager.cruncher_type = cruncher_type
    #project.sync_crunchers()
    #assert len(project.crunching_manager.crunchers) == 2
    #(cruncher_1, cruncher_2) = project.crunching_manager.crunchers.values()
    #assert type(cruncher_1) is cruncher_type
    #assert type(cruncher_2) is cruncher_type
    
    #### Finished testing cruncher type switching. #############################
    
    
    
        
    
    
    