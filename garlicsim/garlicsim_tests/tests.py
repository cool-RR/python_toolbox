import nose

import garlicsim
from garlicsim.general_misc import cute_iter_tools
import time
from garlicsim.bundled.simulation_packages import life
from garlicsim.bundled.simulation_packages import prisoner
from garlicsim.bundled.simulation_packages import _history_test
from garlicsim.bundled.simulation_packages import queue

def _is_deterministic(simpack):
    return simpack.__name__.split('.')[-1] == 'life'

def setup():
    pass

def trivial_test():
    pass

def simpack_test():
    
    simpacks = [life, prisoner, _history_test, queue]
    
    for simpack in simpacks:
        yield synchronous_crunching_check, simpack
        yield asynchronous_crunching_check, simpack

        
def synchronous_crunching_check(simpack):
    
    state = simpack.make_random_state() 
    
    new_state = garlicsim.simulate(simpack, state, 5)
    
    result = garlicsim.list_simulate(simpack, state, 5)
    
    my_simpack_grokker = garlicsim.misc.SimpackGrokker(simpack)
    
    empty_step_profile = garlicsim.misc.StepProfile()
    
    assert len(result) == 6
    
    for item in result:
        assert isinstance(item, garlicsim.data_structures.State)
        if hasattr(simpack, 'State'): # Later make mandatory
            assert isinstance(item, simpack.State)
    
    if _is_deterministic(simpack) is False:
        return
    
    assert simpack.__name__.split('.')[-1] == 'life'
    
    assert result[-1] == new_state
    
    for old, new in cute_iter_tools.pairs(result):
        assert new == my_simpack_grokker.step(old, empty_step_profile)
        

def asynchronous_crunching_check(simpack):
    
    project = garlicsim.Project(simpack)
    
    state = simpack.make_random_state()    
    
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
    
    [my_path] = paths
    
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

    
    two_paths = node_3.all_containing_paths()
    
    assert len(two_paths) == 2
    [path_1, path_2] = two_paths
    get_clock_buffer = lambda path: (path[-1].clock - node_3.clock)
    [clock_buffer_1, clock_buffer_2] = [get_clock_buffer(p) for p in two_paths]
    
    project.ensure_buffer_on_path(None, path_1, get_clock_buffer(p) * 1.2)
        
    WAS HERE YO
    
    
    plain_root = project.make_plain_root()
    
    assert len(tree.roots) == 2
    
    assert len(project.tree.all_possible_paths()) == 4
    
    
    