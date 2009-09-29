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

    def get_all_leaves(self, max_distance=Infinity):
        """
        Finds all leaves that are descendents of this node. Only leaves with a
        distance of at most max_distance are returned. (Distance is specified
        in nodes.)
        
        Returns a dict of the form {node1: distance1, node2: distance2, ...}
        """
        nodes = {self: 0}
        leaves = {}


        while len(nodes) > 0:
            (node, d) = nodes.popitem()
            if d > max_distance:
                continue
            kids = node.children
            if not kids:
                # We have a leaf!
                leaves[node] = d
                continue
            if node.block is None:
                for kid in kids:
                    nodes[kid] = d + 1
                continue
            else:
                block = node.block
                index = block.index(node)
                rest_of_block = (len(block) - index - 1)

                if rest_of_block == 0: # If we hit the last node in the Block
                    for kid in kids:
                        nodes[kid] = d + 1
                    continue

                if rest_of_block + d <= max_distance:
                    for kid in block[-2].children:
                        nodes[kid] = d + rest_of_block
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

from path import Path