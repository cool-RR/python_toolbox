# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
A module that defines the `Tree` class. See its documentation for more
information.
"""

import copy

from block import Block
# Note we are doing `from node import Node` in the bottom of the file.

__all__ = ["Tree", "TreeError"]

class TreeError(Exception):
    """
    An exception related to the class Tree.
    """
    pass

class Tree(object):
    """
    A tree of nodes. Each node encapsulates a state.

    A tree is used within a project to organize everything that is happenning
    in the simulation. A tree, which may be called a time tree, is a
    generalization of a timeline.
    
    Often, when doing a simulation, the tree will be a degenerate tree, i.e. a
    straight, long succession of nodes with no more than one child each. The
    meaning of one node in the tree being another node's child is that the
    child node comes after the parent node in the timeline.
    
    Trees are useful, because they give you the ability to "split" or "fork"
    the simulation at any node you wish, allowing you to explore and analyze
    different scenarios in parallel in the same simulation.

    Each node in the tree may have a parent, or may not, in which case it will
    also be called a root and be a member of tree.roots .
    """
    def __init__(self):
        self.nodes = set() # A set for containing all the nodes in the tree.
        self.roots = set() # A set of roots. A root is a node without a parent.

    def fork_by_editing(self, template_node):
        """
        Creates a new touched state, using the state of template_node as a
        template. Wraps it in a node and adds to tree.
        Returns the node.
        """
        x = copy.deepcopy(template_node.state)

        if template_node is None:
            parent = None
        else:
            parent = template_node.parent

        return self.add_state(x, parent, template_node)


    def add_state(self, state, parent=None, template_node=None):
        """
        Wraps state in node and adds to tree.
        Returns the node.
        """
        touched = (parent is None) or (template_node is not None)    
        my_node = Node(self, state, touched=touched)
        self.add_node(my_node, parent, template_node)
        return my_node


    def add_node(self, node, parent=None, template_node=None):
        """
        Adds a node to the tree.
        
        It may be a natural node or a touched node. If it's a natural node it
        cannot have a template_node.
        
        Returns the node.
        """
        if template_node is not None:
            if parent != template_node.parent:
                raise TreeError("""Parent you specified and parent of \
                template_node aren't the same!""")
            if not node.touched:
                raise TreeError("""You tried adding an untouched state to a \
                tree while specifying a template_node.""")
            template_node.derived_nodes.append(node)
            

        self.nodes.add(node)

        if parent:
            if hasattr(node.state, "clock") is False:
                node.state.clock = parent.state.clock + 1

            node.parent = parent
            parent.children.append(node)
            
            if parent.block:
                if len(parent.children)==1:
                    if not node.touched:
                        parent.block.append_node(node)
                else: # parent.children > 1
                    if not (parent is parent.block[-1]):
                        parent.block.split(parent)
            else: # parent.block is None
                if (not node.touched) and (not parent.touched) and \
                   (len(parent.children)==1):
                    Block([parent, node])
                
                        
        else: # parent is None
            if hasattr(node.state, "clock") is False:
                node.state.clock = 0
            self.roots.add(node)
            return node


    def node_count(self):
        """
        Returns the number of nodes in the tree.
        """
        return len(self.nodes)
    
from node import Node