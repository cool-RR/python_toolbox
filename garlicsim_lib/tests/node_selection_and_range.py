# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import copy
import nose
from garlicsim.general_misc import logic_tools

import garlicsim
from garlicsim import data_structures as ds
from garlicsim_lib.simpacks import life

def node_selection_and_range_test():
    root_state = life.State.create_root(2, 2)
    project = garlicsim.Project(life)
    tree = project.tree
    root = project.root_this_state(root_state)
    leaf1 = project.simulate(root, 10)
    temp_path = root.make_containing_path()
    middle_node = temp_path[5]
    leaf2 = project.simulate(middle_node, 10)
    
    # Now we have a tree with a fork in it, in `middle_node`
    
    path1 = leaf1.make_containing_path() # creating only after leaf2
    path2 = leaf2.make_containing_path()    
    
    range1 = ds.NodeRange(root, leaf1)
    assert path1 == range1.make_path()
    range2 = ds.NodeRange(root, leaf2)
    assert path2 == range2.make_path()
    
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
    
    all_ranges = sum((ns.ranges for ns in (ns1, ns2, ns3, ns4)), [])
    
    for range in all_ranges:
        assert range == range.clone_with_blocks_dissolved()
    
    assert len(tree.nodes) == 21
    
    #####################
    alt_tree, alt_ns1 = copy.deepcopy((tree, ns1))
    alt_tree.delete_node_selection(alt_ns1)
    assert len(alt_tree.nodes) == 0
    assert len(alt_tree.roots) == 0
    #####################

    assert len(tree.nodes) == 21
    
    middle_node_grandparent = middle_node.parent.parent    
    
    middle_node_grandchild_1 = path1.next_node(path1.next_node(middle_node))
    middle_node_grandchild_2 = path2.next_node(path2.next_node(middle_node))
    
    assert middle_node_grandchild_1 is not middle_node_grandchild_2
    
    small_range_1 = ds.NodeRange(middle_node_grandparent,
                                 middle_node_grandchild_1)
    small_range_2 = ds.NodeRange(middle_node_grandparent,
                                 middle_node_grandchild_2)
    
    assert small_range_1 != small_range_2
    
    small_ns = ds.NodeSelection((small_range_1, small_range_2))
    
    #####################
    alt_tree, alt_small_range_1 = copy.deepcopy((tree, small_range_1))
    alt_tree.delete_node_range(alt_small_range_1)
    assert len(alt_tree.roots) == 3
    assert len(alt_tree.nodes) == 16
    #####################
    
    #####################
    alt_tree, alt_small_range_2 = copy.deepcopy((tree, small_range_2))
    alt_tree.delete_node_range(alt_small_range_2)
    assert len(alt_tree.roots) == 3
    assert len(alt_tree.nodes) == 16
    #####################
    
    #####################
    alt_tree, alt_small_ns = copy.deepcopy((tree, small_ns))
    alt_tree.delete_node_selection(alt_small_ns)
    assert len(alt_tree.roots) == 3
    assert len(alt_tree.nodes) == 14
    #####################
    
    assert len(tree.nodes) == 21
    
    
    
    
    
    
    
    
    
    