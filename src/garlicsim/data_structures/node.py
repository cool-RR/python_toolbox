# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
A module that defines the `Node` class. See its documentation for more
information.
"""

from state import State
# Note we are doing `from path import Path` in the bottom of the file.
from garlicsim.misc.infinity import Infinity

__all__ = ["Node"]

class Node(object):
    """
    A node encapsulates a State with the attribute ".state". Nodes are used to
    organize states in a Tree.
    
    Most nodes are untouched, a.k.a. natural, but some nodes are touched.
    A touched node is a node whose state was not formed naturally by a
    simulation step: It was created by the user, either from scratch or based
    on another state.
    
    todo: Maybe node should not reference tree?
    """
    def __init__(self, tree, state, parent=None, touched=False):
        
        self.state = state
        self.parent = parent
        self.tree = tree
        
        self.touched = touched
        """
        Says whether the node is a touched node.
        """
        
        self.block = None
        """
        A node may be a member of a block. See class Block for more details.
        """

        self.children = []
        """
        A list of:
        1. Nodes whose states were produced by simulation from this node.
        2. Nodes who were "created by editing" from one of the nodes in the
        aforementioned set.
        """

        self.derived_nodes = []
        """
        A list of nodes who were created by editing from this node.
        These nodes should have the same parent as this node.
        """

        self.still_in_editing = False
        """
        A flag that is raised for a node which is "still in editing", meaning
        that its state is still being edited and was not yet finalized, thus no
        crunching should be made from the node until it is finalized.
        """
        
    def __len__(self):
        """
        Just returns 1. This is useful because of blocks.
        """
        return 1

    def soft_get_block(self):
        """
        If this node is a member of a Block, returns the Block.
        Otherwise, returns the node itself.
        """
        if self.block is not None:
            return self.block
        else:
            return self

    def make_containing_path(self):
        """
        Creates a path that contains this node.
        """
        path = Path(self.tree)

        current = self
        while True:
            if current.block is not None:
                current = current.block[0]
            parent = current.parent
            if parent is None:
                path.root = current
                break
            if len(parent.children) > 1:
                path.decisions[parent] = current
            current = parent

        return path

    def get_all_leaves(self, max_nodes_distance=None, max_clock_distance=None):
        """
        Finds all leaves that are descendents of this node. Only leaves with a
        distance of at most TODO (IT'S `OR`ED) are returned.
        
        Returns a dict of the form TODO
        """
        if max_nodes_distance is None:
            max_nodes_distance = Infinity
        if max_clock_distance is None:
            max_clock_distance = Infinity
                    
        nodes = {self: {"nodes_distance": 0, "clock_distance": 0}}
        leaves = {}

        while nodes:
            item = nodes.popitem()
            node = item[0]
            nodes_distance = item[1]["nodes_distance"]
            clock_distance = item[1]["clock_distance"]
            
            if nodes_distance > max_nodes_distance or \
               clock_distance > max_clock_distance:
                continue
            
            kids = node.children
            
            if not kids:
                # We have a leaf!
                leaves[node] = {
                    "nodes_distance": nodes_distance,
                    "clock_distance": clock_distance,
                }
                continue
            
            if (node.block is None) or node.is_last_on_block():
                for kid in kids:
                    nodes[kid] = {
                        "nodes_distance": nodes_distance + 1,
                        "clock_distance": kid.state.clock - self.state.clock,
                    }
                continue
            else:
                block = node.block
                index = block.index(node)
                rest_of_block = (len(block) - index - 1)
                
                # We know the node isn't the last on the block, because we
                # checked for that before.

                last = block[-1]
                nodes[last] = {
                    "nodes_distance": nodes_distance + rest_of_block,
                    "clock_distance": last.state.clock - self.state.clock,
                }
                continue
            
        return leaves
    
    def get_root(self):
        """
        Gets the root of this node, i.e. the node which is the parent of
        the parent of the parent of... the parent of this node.
        """
        lowest = self.block[0] if self.block else self
        while lowest.parent is not None:
            lowest = lowest.parent
            if lowest.block:
                lowest = lowest.block[0]
        return lowest
    
    def is_last_on_block(self):
        return self.block and (self.block.index(self) == len(self.block) - 1)
    
    def is_first_on_block(self):
        return self.block and (self.block.index(self) == 0)

from path import Path