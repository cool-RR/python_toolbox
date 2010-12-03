# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Test module for garlicsim.

I'm just starting to learn testing, so go easy on me.
'''

from __future__ import division

import os
import types
import time
import itertools

import nose

from garlicsim.general_misc import cute_iter_tools
from garlicsim.general_misc import math_tools
from garlicsim.general_misc import path_tools
from garlicsim.general_misc import import_tools
from garlicsim.general_misc.infinity import Infinity

import garlicsim

from .shared import MustachedThreadCruncher

FUZZ = 0.0001
'''Fuzziness of floats.'''


def test():
    
    from . import sample_simpacks
    
    # Collecting all the test simpacks:
    simpacks = import_tools.import_all(sample_simpacks).values()
    
    # Making sure that we didn't miss any simpack by counting the number of
    # sub-folders in the `sample_simpacks` folders:
    sample_simpacks_dir = \
        os.path.dirname(sample_simpacks.__file__)
    assert len(path_tools.list_sub_folders(sample_simpacks_dir)) == \
           len(simpacks)
    
    cruncher_types = [
        garlicsim.asynchronous_crunching.crunchers.ThreadCruncher,
        
        # Until multiprocessing shit is solved, this is commented-out:
        #garlicsim.asynchronous_crunching.crunchers.ProcessCruncher
    ]
    
    
    for simpack, cruncher_type in \
        cute_iter_tools.product(simpacks, cruncher_types):
        
        # Making `_settings_for_testing` available:
        import_tools.import_all(simpack)
        
        yield check, simpack, cruncher_type


        
def check(simpack, cruncher_type):
    
    my_simpack_grokker = garlicsim.misc.SimpackGrokker(simpack)
    
    assert my_simpack_grokker is garlicsim.misc.SimpackGrokker(simpack)
    # Ensuring caching works.
    
    assert not simpack._settings_for_testing.ENDABLE
    
    assert garlicsim.misc.simpack_grokker.get_step_type(
        my_simpack_grokker.default_step_function
    ) == simpack._settings_for_testing.STEP_FUNCTION_TYPE
    
    step_profile = my_simpack_grokker.build_step_profile()
    deterministic = \
        my_simpack_grokker.settings.DETERMINISM_FUNCTION(step_profile)
    
    
    state = simpack.State.create_root()
    
    
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

    
    ### Setting up a project to run asynchronous tests:
    
    project = garlicsim.Project(simpack)
        
    project.crunching_manager.cruncher_type = cruncher_type
    
    assert project.tree.lock._ReadWriteLock__writer is None
    
    root = project.root_this_state(state)
    
    
    project.begin_crunching(root, 4)

    total_nodes_added = 0    
    while project.crunching_manager.jobs:
        time.sleep(0.1)
        total_nodes_added += project.sync_crunchers()
        
    assert total_nodes_added == 4
    
    assert len(project.tree.nodes) == 5
    assert len(project.tree.roots) == 1
    
    paths = project.tree.all_possible_paths()
    
    assert len(paths) == 1
    
    (my_path,) = paths
        
    assert len(my_path) == 5
    
    node_1 = my_path[1]
    assert node_1.state.clock == 1
    
    node_2 = project.simulate(node_1, 3)
    
    assert len(project.tree.nodes) == 8
    assert len(project.tree.roots) == 1
    
    assert len(project.tree.all_possible_paths()) == 2
    
    node_3 = my_path.next_node(node_1)
    
    ### Test changing step profile on the fly: ################################
    #                                                                         #
    
    # For simpacks providing more than one step function, we'll test changing
    # between them. This will exercise crunchers' ability to receieve a
    # `CrunchingProfile` and react appropriately.
    #if simpack._settings_for_testing.N_STEP_FUNCTIONS >= 2:        
        #default_step_function, alternate_step_function = \
            #my_simpack_grokker.all_step_functions[:2]
    
    #                                                                         #
    ### Finished testing changing step profile on the fly: ####################
    
    ### Testing cruncher type switching: ######################################
    #                                                                         #
    
    job_1 = project.begin_crunching(root, clock_buffer=Infinity)
    job_2 = project.begin_crunching(root, clock_buffer=Infinity)
    
    assert len(project.crunching_manager.crunchers) == 0
    assert project.sync_crunchers() == 0
    assert len(project.crunching_manager.crunchers) == 2
    (cruncher_1, cruncher_2) = project.crunching_manager.crunchers.values()
    assert type(cruncher_1) is cruncher_type
    assert type(cruncher_2) is cruncher_type
    
    time.sleep(0.2) # Letting the crunchers start working
    
    project.crunching_manager.cruncher_type = MustachedThreadCruncher
    project.sync_crunchers()
    assert len(project.crunching_manager.crunchers) == 2
    (cruncher_1, cruncher_2) = project.crunching_manager.crunchers.values()
    assert type(cruncher_1) is MustachedThreadCruncher
    assert type(cruncher_2) is MustachedThreadCruncher
    
    project.crunching_manager.cruncher_type = cruncher_type
    project.sync_crunchers()
    assert len(project.crunching_manager.crunchers) == 2
    (cruncher_1, cruncher_2) = project.crunching_manager.crunchers.values()
    assert type(cruncher_1) is cruncher_type
    assert type(cruncher_2) is cruncher_type
    
    # Deleting jobs so the crunchers will stop:
    del project.crunching_manager.jobs[:]
    project.sync_crunchers()
    
    #                                                                         #
    ### Finished testing cruncher type switching. #############################
    
    
    
        
    
    
    
    
    
    
    
    
    
    
    
            