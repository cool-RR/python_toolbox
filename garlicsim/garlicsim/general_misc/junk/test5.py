import time
import garlicsim
from garlicsim.bundled.simulation_packages import life
from garlicsim.bundled.simulation_packages import prisoner

simpack = life

if __name__ == '__main__':
    
    state = simpack.make_random_state(10, 10)
    
    
    print(state)
    
    
    new_state = garlicsim.simulate(simpack, state, 10)
    
    print(new_state)
    
    result = garlicsim.list_simulate(simpack, state, 10)
    
    assert result[-1] == new_state
    
    
    project = garlicsim.Project(simpack)
    
    project.crunching_manager.Cruncher = \
        garlicsim.asynchronous_crunching.crunchers_warehouse.crunchers['CruncherProcess']
    
    root = project.root_this_state(state)
    

    project.begin_crunching(root, 500)
    
    print(project.sync_crunchers())
    
    time.sleep(2.0)
    print(project.sync_crunchers())
    path = project.tree.all_possible_paths()[0]
    node = path[len(path)//2]
    new_node = project.simulate(node, 20)
    
    count = 0
    while True:
        time.sleep(0.05)
        j = project.sync_crunchers()
        print(j)
        if not project.crunching_manager.jobs:
            break
    
    
    print(root.get_all_leaves().popitem()[0].state)
    print(garlicsim.data_structures.State.__repr__(root.get_all_leaves().popitem()[0].state))