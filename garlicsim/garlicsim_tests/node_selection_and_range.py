import nose
from garlicsim.general_misc import logic_tools

import garlicsim
from garlicsim import data_structures as ds
from garlicsim.bundled.simulation_packages import life

def node_selection_and_range_test():
    root_state = life.make_plain_state(2, 2)
    project = garlicsim.Project(life)
    tree = project.tree
    root = project.root_this_state(root_state)
    leaf1 = project.simulate(root, 10)
    path = leaf1.make_containing_path()
    assert root in path
    middle_node = path[5]
    leaf2 = project.simulate(middle_node, 10)
    
    # Now we have a tree with a fork in it, in `middle_node`
    
    range1 = ds.NodeRange(root, leaf1)
    range2 = ds.NodeRange(root, leaf2)
    ns1 = ds.NodeSelection([range1, range2])
    ns2 = ns1.copy()
    assert ns1 == ns2
    
    ns2.compact()
    assert ns1 == ns2
    
    range1blocky = ds.NodeRange(root, leaf1.block)
    range2blocky = ds.NodeRange(root, leaf2.block)
    ns3 = ds.NodeSelection([range1blocky, range2blocky])
    
    ns4 = ns3.copy()
    ns4.compact()
    
    logic_tools.all_equal((ns1, ns2, ns3, ns4), exhaustive=True)
    
    
    
    
    
    