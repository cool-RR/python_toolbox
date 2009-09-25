# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
The data_structures package defines data structures that are used for saving
simulation data in memory. It defines the `State`, `Node`,`Tree`,`Block`, and
`Path` classes.
States are used to save a single world state of the simulation. Nodes are used
to put states in chronological order inside a Tree. Paths are used to indicate
specific timelines inside a tree. Blocks, which are not as critical as the
other types of objects, are used to optimize access to long successions of
nodes.
"""


from state import State
from tree import Tree, TreeError
from path import Path, PathError, PathOutOfRangeError
from node import Node
from block import Block, BlockError


__all__ = ["State", "Tree", "Path", "Node", "Block"] + \
        ["BlockError", "PathError", "PathOutOfRangeError", "TreeError"]