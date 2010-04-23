# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
Defines data structures that are used for saving simulation data.

States are used to save a single world state of the simulation. Nodes are used
to put states in chronological order inside a Tree. Paths are used to indicate
specific timelines inside a tree. Blocks, which are not as critical as the
other types of objects, are used to optimize access to long successions of
nodes.
'''


from state import State
from tree import Tree, TreeError
from path import Path, PathError, PathOutOfRangeError
from node import Node, NodeError
from block import Block, BlockError

from node_range import NodeRange
from node_selection import NodeSelection


__all__ = ['State', 'Tree', 'Path', 'Node', 'Block', 'NodeRange',
           'NodeSelection'] + \
          ['BlockError', 'PathError', 'PathOutOfRangeError', 'TreeError',
           'NodeError']