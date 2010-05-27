# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Test module for garlicsim.

I'm just starting to learn testing, so go easy on me.
'''

from __future__ import division

import nose
import time
import itertools

import garlicsim
from garlicsim.general_misc import cute_iter_tools

from garlicsim_lib.simpacks import life
from garlicsim_lib.simpacks import prisoner
from garlicsim_lib.simpacks import _history_test
from garlicsim_lib.simpacks import queue


def _is_deterministic(simpack):
    return simpack.__name__.split('.')[-1] == 'life'

def setup():
    pass

def trivial_test():
    pass

def simpack_test():
    
    simpacks = [life, prisoner, _history_test, queue]
    
    crunchers = \
        [garlicsim.asynchronous_crunching.crunchers.CruncherThread,
         garlicsim.asynchronous_crunching.crunchers.CruncherProcess]
    
    crunchers = [garlicsim.asynchronous_crunching.crunchers.CruncherThread]
    # Until multiprocessing shit is solved
    
    for simpack, cruncher in cute_iter_tools.product(simpacks, crunchers):
        yield simpack_check, simpack, cruncher

        
def simpack_check(simpack, cruncher):
    
    state = simpack.State.create_messy_root() if \
          simpack.State.create_messy_root else \
          simpack.State.create_root()
    
    new_state = garlicsim.simulate(state, 5)
    
    result = garlicsim.list_simulate(state, 5)
    
    my_simpack_grokker = garlicsim.misc.SimpackGrokker(simpack)
    
    empty_step_profile = garlicsim.misc.StepProfile()
    
    assert len(result) == 6
    
    for item in result:
        assert isinstance(item, garlicsim.data_structures.State)
        if hasattr(simpack, 'State'): # Later make mandatory
            assert isinstance(item, simpack.State)
    
    if _is_deterministic(simpack):
        
        assert result[-1] == new_state
        
        for old, new in cute_iter_tools.consecutive_pairs(result):
            assert new == my_simpack_grokker.step(old, empty_step_profile)
    
    project = garlicsim.Project(simpack)
    
    project.crunching_manager.Cruncher = cruncher
    
    root = project.root_this_state(state)
    
    project.begin_crunching(root, 20)

    total_nodes_added = 0    
    while project.crunching_manager.jobs:
        time.sleep(0.1)
        total_nodes_added += project.sync_crunchers()
        
    x = total_nodes_added
    assert len(project.tree.nodes) == x + 1
    assert len(project.tree.roots) == 1
    
    paths = project.tree.all_possible_paths()
    
    assert len(paths) == 1
    
    (my_path,) = paths
    
    if _is_deterministic(simpack):
        assert my_path[5].state == new_state
        
    assert len(my_path) == x + 1
    
    node_1 = my_path[-3]
    
    node_2 = project.simulate(node_1, 5)
    
    assert len(project.tree.nodes) == x + 6
    assert len(project.tree.roots) == 1
    
    assert len(project.tree.all_possible_paths()) == 2
    
    node_3 = my_path.next_node(node_1)
    
    project.begin_crunching(node_3, 5)
    
    total_nodes_added = 0
    while project.crunching_manager.jobs:
        time.sleep(0.1)
        total_nodes_added += project.sync_crunchers()
    
    y = total_nodes_added
    assert len(project.tree.nodes) == x + y + 6
    
    paths = project.tree.all_possible_paths()
    assert len(paths) == 3
    
    assert set(len(p) for p in paths) == set([x + 1, x + 4, x + y])
    
    
    project.ensure_buffer(node_3, 3)

    total_nodes_added = 0
    while project.crunching_manager.jobs:
        time.sleep(0.1)
        total_nodes_added += project.sync_crunchers()
    
    assert len(project.tree.nodes) == x + y + 6 + total_nodes_added
    assert len(project.tree.all_possible_paths()) == 3

    
    two_paths = node_3.all_possible_paths()
    
    assert len(two_paths) == 2
    (path_1, path_2) = two_paths
    get_clock_buffer = lambda path: (path[-1].state.clock - node_3.state.clock)
    (clock_buffer_1, clock_buffer_2) = [get_clock_buffer(p) for p in two_paths]
    
    project.ensure_buffer_on_path(node_3, path_1, get_clock_buffer(path_1) * 1.2)
    
    total_nodes_added = 0
    while project.crunching_manager.jobs:
        time.sleep(0.1)
        total_nodes_added += project.sync_crunchers()
    
    (old_clock_buffer_1, old_clock_buffer_2) = (clock_buffer_1, clock_buffer_2)
    (clock_buffer_1, clock_buffer_2) = [get_clock_buffer(p) for p in two_paths]
    
    assert clock_buffer_1 / old_clock_buffer_1 >= 1.2
    assert clock_buffer_2 == old_clock_buffer_2
    
    project.ensure_buffer_on_path(node_3, path_2, get_clock_buffer(path_2) * 1.3)
    
    total_nodes_added = 0
    while project.crunching_manager.jobs:
        time.sleep(0.1)
        total_nodes_added += project.sync_crunchers()
    
    (old_clock_buffer_1, old_clock_buffer_2) = (clock_buffer_1, clock_buffer_2)
    (clock_buffer_1, clock_buffer_2) = [get_clock_buffer(p) for p in two_paths]
    
    assert clock_buffer_1 == old_clock_buffer_1
    assert clock_buffer_2 / old_clock_buffer_2 >= 1.3
    
    
    
    plain_root = project.create_root()
    
    assert len(project.tree.roots) == 2
    
    assert len(project.tree.all_possible_paths()) == 4
    
    
    