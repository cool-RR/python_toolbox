# Copyright 2009-2011 Ram Rachum.
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
from garlicsim.general_misc.infinity import infinity
from garlicsim.general_misc.nifty_collections import OrderedSet

import garlicsim

import test_garlicsim

from ..shared import MustachedThreadCruncher


def non_ending_inplace_step(state):
    '''A no-op inplace step that doesn't end the simulation.'''
    pass


def non_ending_history_step(history_browser):
    '''A minimal history step that doesn't end the simulation.'''
    old_state = history_browser[-1]
    new_state = garlicsim.misc.state_deepcopy.state_deepcopy(old_state)
    new_state.clock += 1
    return new_state


def test_endable():
    '''
    Test handling of endable simpacks.
    
    All simpacks end when they get a world-state with clock reading of 4 or
    more.
    '''
    
    from . import simpacks as simpacks_package
    
    # Collecting all the test simpacks:
    simpacks = import_tools.import_all(simpacks_package).values()
    
    # Making sure that we didn't miss any simpack by counting the number of
    # sub-folders in the `simpacks` folder:
    simpacks_dir = \
        os.path.dirname(simpacks_package.__file__)
    assert len(path_tools.list_sub_folders(simpacks_dir)) == \
           len(simpacks)
    
    for simpack in simpacks:

        test_garlicsim.verify_simpack_settings(simpack)
        
        cruncher_types = \
            garlicsim.misc.SimpackGrokker(simpack).available_cruncher_types
        
        for cruncher_type in cruncher_types:
            yield check, simpack, cruncher_type

        
def check(simpack, cruncher_type):
    
    assert simpack._test_settings.ENDABLE is True
    assert simpack._test_settings.CONSTANT_CLOCK_INTERVAL == 1
    
    my_simpack_grokker = garlicsim.misc.SimpackGrokker(simpack)
    
    assert my_simpack_grokker is garlicsim.misc.SimpackGrokker(simpack)
    # Ensuring caching works.
    
    assert garlicsim.misc.simpack_grokker.step_type.StepType.get_step_type(
        my_simpack_grokker.default_step_function
    ) == simpack._test_settings.DEFAULT_STEP_FUNCTION_TYPE
    
    step_profile = my_simpack_grokker.build_step_profile()
    deterministic = \
        my_simpack_grokker.settings.DETERMINISM_FUNCTION(step_profile)
    
    state = simpack.State.create_root()
    
    ### Running for short periods synchronically so it doesn't end: ###########
    #                                                                         #
    
    # Whether we run the simulation for one, two, three, or four iterations,
    # the simulation doesn't end.
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
    ### Done running for short periods synchronically so it doesn't end. ######
    
    ### Now, let's run it for longer periods synchronically to make it end: ###
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
    ### Done running for longer periods synchronically to make it end. ########
    
    ### Setting up a project to run asynchronous tests:
    
    project = garlicsim.Project(simpack) 
        
    project.crunching_manager.cruncher_type = cruncher_type
    
    assert project.tree.lock._ReadWriteLock__writer is None
    
    root = project.root_this_state(state)
    
    def get_all_ends():
        return [member for member in project.tree.iterate_tree_members() if 
                isinstance(member, garlicsim.data_structures.End)]
    
    assert len(get_all_ends()) == 0
    
    ### Running for short periods asynchronically so it doesn't end: ##########
    #                                                                         #
    
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
    
    assert len(get_all_ends()) == 0
    
    #                                                                         #
    ### Done running for short periods asynchronically so it doesn't end. #####
    
    ### Now, let's run it for longer periods asynchronically to make it end: ##
    #                                                                         #
    
    node_3 = my_path.next_node(node_1)
    assert node_3.state.clock == 2
    project.begin_crunching(node_3, 3)
    
    total_nodes_added = 0
    while project.crunching_manager.jobs:
        time.sleep(0.1)
        total_nodes_added += project.sync_crunchers()
    assert total_nodes_added == 2 # Would have been 3 without the end!
    
    assert len(get_all_ends()) == 1
    
    # So now `node_3`'s newer path has an end:
    ended_path = node_3.all_possible_paths()[1]
    isinstance(ended_path, garlicsim.data_structures.Path)
    (end,) = ended_path.get_ends_of_last_node() # (Asserting there's one end.)
    assert isinstance(end, garlicsim.data_structures.End)
    
    assert len(project.tree.nodes) == 10
    
    paths = project.tree.all_possible_paths()
    assert len(paths) == 3
    
    assert [len(p) for p in paths] == [5, 5, 5]
    
    
    # Ensuring buffer on `ended_path` from `node_3` won't cause a new job to be
    # created since we have a path to an existing end:
    project.ensure_buffer_on_path(node_3, ended_path, 10)
    project.ensure_buffer_on_path(node_3, ended_path, 1000)
    project.ensure_buffer_on_path(node_3, ended_path, infinity)
    total_nodes_added = 0    
    assert not project.crunching_manager.jobs
    assert len(project.tree.nodes) == 10
    
    # These `ensure_buffer_on_path` calls shouldn't have added any ends:
    assert len(get_all_ends()) == 1
    
    # But `node_3` has the older path coming out of it which goes all the way to
    # clock 4 but doesn't terminate in an `End`:
    other_path = node_3.all_possible_paths()[0]
    assert other_path.get_ends_of_last_node() == []
    
    # And when we `ensure_buffer` from `node_3`, it will ensure a buffer on that
    # path also, and cause an `End` to be created there:
    project.ensure_buffer(node_3, 1000)
    total_nodes_added = 0    
    while project.crunching_manager.jobs:
        time.sleep(0.1)
        total_nodes_added += project.sync_crunchers()
    assert len(project.tree.nodes) == 10
    assert len(get_all_ends()) == 2
    
    
    plain_root = project.create_root()
    
    assert len(project.tree.roots) == 2
    assert len(project.tree.all_possible_paths()) == 4
    assert len(project.tree.nodes) == 11
    
    iterator = project.iter_simulate(node_1, 10)
    new_node = iterator.next()
    assert new_node is node_1
    assert len(project.tree.nodes) == 11
    
    assert project.tree.lock._ReadWriteLock__writer is None
    
    new_node = iterator.next()
    assert new_node is not node_1
    assert new_node.parent is node_1
    assert len(project.tree.nodes) == 12
    
    bunch_of_new_nodes = tuple(iterator)
    consecutive_pairs = cute_iter_tools.consecutive_pairs(bunch_of_new_nodes)
    for parent_node, kid_node in consecutive_pairs:
        assert project.tree.lock._ReadWriteLock__writer is None
        assert isinstance(parent_node, garlicsim.data_structures.Node)
        assert isinstance(kid_node, garlicsim.data_structures.Node)
        assert parent_node.children == [kid_node]
        assert kid_node.parent is parent_node
        
    assert len(project.tree.nodes) == 14

    assert len(get_all_ends()) == 3
    
        
    tree_members_iterator = \
        project.tree.iterate_tree_members(include_blockful_nodes=False)
    assert tree_members_iterator.__iter__() is tree_members_iterator
    tree_members = list(tree_members_iterator)
    for tree_member in tree_members:
        if isinstance(tree_member, garlicsim.data_structures.Node):
            assert tree_member.block is None
            
    tree_members_iterator_including_blockful_nodes = \
        project.tree.iterate_tree_members()
    assert tree_members_iterator_including_blockful_nodes.__iter__() is \
        tree_members_iterator_including_blockful_nodes
    tree_members_including_blockful_nodes = \
        list(tree_members_iterator_including_blockful_nodes)
    
    
    blockful_nodes = \
        [member for member in tree_members_including_blockful_nodes if 
         member not in tree_members]
    assert len(blockful_nodes) >= 1
    for blockful_node in blockful_nodes:
        assert isinstance(blockful_node, garlicsim.data_structures.Node)
        assert isinstance(blockful_node.block, garlicsim.data_structures.Block)
        assert blockful_node.block is blockful_node.soft_get_block()
    assert set(tree_members).\
        issubset(set(tree_members_including_blockful_nodes))
    
    tree_step_profiles = project.tree.get_step_profiles()
    assert isinstance(tree_step_profiles, OrderedSet)
    assert tree_step_profiles == [step_profile]
    
    ends = [member for member in tree_members if 
            isinstance(member, garlicsim.data_structures.End)]
    assert len(ends) == 3
    for end in ends:
        assert end in tree_members_including_blockful_nodes
        
    ### Testing `Project.simulate`: ###########################################
    #                                                                         #
    
    project.simulate(root, 4)
    assert len(get_all_ends()) == 3
    
    project.simulate(root, 5)
    assert len(get_all_ends()) == 4
    
    #                                                                         #
    ### Finished testing `Project.simulate`. ##################################
    
    ### Testing end creation in middle of block: ##############################
    #                                                                         #
    
    my_non_ending_step = non_ending_history_step if \
        my_simpack_grokker.history_dependent else non_ending_inplace_step
    
    nodes_in_tree = len(project.tree.nodes)
    nodes = list(project.iter_simulate(root, 8, my_non_ending_step))
    assert len(project.tree.nodes) == nodes_in_tree + 8
    
    middle_node = nodes[-4]
    assert middle_node.state.clock == 5
    assert nodes[1].block == middle_node.block == nodes[-1].block
    assert len(middle_node.block) == 8
    

    project.begin_crunching(middle_node, infinity, step_profile)
    total_nodes_added = 0
    assert project.crunching_manager.jobs
    while project.crunching_manager.jobs:
        time.sleep(0.1)
        total_nodes_added += project.sync_crunchers()
    assert total_nodes_added == 0
    
    assert len(middle_node.ends) == 1
    assert middle_node.block is not nodes[-1].block
    assert len(middle_node.block) == 5
    assert len(nodes[-1].block) == 3
        
    #                                                                         #
    ### Finished testing end creation in middle of block. #####################
    
    
    