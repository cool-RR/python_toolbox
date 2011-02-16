# Copyright 2009-2011 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Testing module for `garlicsim.asynchronous_crunching`.'''

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
from garlicsim.general_misc.infinity import infinity
from garlicsim.general_misc.nifty_collections import OrderedSet

import garlicsim

import test_garlicsim


def test():
    '''Test `garlicsim.asynchronous_crunching`.'''
    
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
    
    my_simpack_grokker = garlicsim.misc.SimpackGrokker(simpack)
    
    assert my_simpack_grokker is garlicsim.misc.SimpackGrokker(simpack)
    # Ensuring caching works.
    
    assert not simpack._test_settings.ENDABLE
    
    assert garlicsim.misc.simpack_grokker.step_type.StepType.get_step_type(
        my_simpack_grokker.default_step_function
    ) == simpack._test_settings.DEFAULT_STEP_FUNCTION_TYPE
    
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

    block_1, block_2 = [node.block for node in node_1.children]
    assert isinstance(block_1, garlicsim.data_structures.Block)
    assert isinstance(block_2, garlicsim.data_structures.Block)
    assert block_1.soft_get_block() is block_1
    assert block_2.soft_get_block() is block_2
    assert block_1.is_overlapping(block_1)
    assert block_2.is_overlapping(block_2)
    assert not block_1.is_overlapping(block_2)
    assert not block_2.is_overlapping(block_1)
    block_path_1 = block_1.make_containing_path()
    block_path_2 = block_2.make_containing_path()
    assert block_path_1 == block_path_1
    assert block_path_1 != block_path_2
    assert (block_1[0] in block_path_1) and (block_1[-1] in block_path_1)
    assert (block_2[0] in block_path_2) and (block_2[-1] in block_path_2)
    assert block_1.get_root() is block_2.get_root()
    
        
 
    tree_members_iterator = \
        project.tree.iterate_tree_members(include_blockful_nodes=False)
    assert tree_members_iterator.__iter__() is tree_members_iterator
    tree_members = list(tree_members_iterator)
    assert (block_1 in tree_members) and (block_2 in tree_members)
    for tree_member in tree_members:
        if isinstance(tree_member, garlicsim.data_structures.Node):
            assert tree_member.block is None
    
    tree_members_iterator_including_blockful_nodes = \
        project.tree.iterate_tree_members(include_blockful_nodes=True)
    assert tree_members_iterator_including_blockful_nodes.__iter__() is \
        tree_members_iterator_including_blockful_nodes
    tree_members_including_blockful_nodes = \
        list(tree_members_iterator_including_blockful_nodes)
    
    blockful_nodes = \
        [member for member in tree_members_including_blockful_nodes if 
         member not in tree_members]
    for blockful_node in blockful_nodes:
        assert isinstance(blockful_node, garlicsim.data_structures.Node)
        assert isinstance(blockful_node.block, garlicsim.data_structures.Block)
        assert blockful_node.block is blockful_node.soft_get_block()
    assert set(tree_members).\
        issubset(set(tree_members_including_blockful_nodes))
    
    tree_step_profiles = project.tree.get_step_profiles()
    assert isinstance(tree_step_profiles, OrderedSet)
    assert tree_step_profiles == [step_profile]
    