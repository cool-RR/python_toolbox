"""
A module that defines the `Tree` class. See
its documentation for more information.
"""

import copy

from block import Block
# Note we are doing `from node import Node` in the bottom of the file
# to avoid problems with circular imports.

__all__ = ["Tree"]


class Tree(object):
    """
    A tree of nodes. Each node encapsulates a state.

    A tree is used within a Project to organize everything that
    is happenning in the simulation. Often, when doing a simulation,
    this tree will be a "degenerate" tree, i.e. a straight, long
    succession of nodes with no more than one child each.
    The meaning of one node in the tree being another node's child is
    that the child node comes after the parent node in the timeline.
    Trees are useful, because they give you the ability
    to "split" or "fork" the simulation at any node you wish,
    allowing you to explore and analyze different "scenarios"
    in parallel in the same simulation.


    How does the tree work?
    There is a list of nodes. Each node has the properties:
    ".parent", ".children" and ".dervied_nodes" within it,
    which refer to its relatives.

    Each node may have a parent, or may not, in which case it
    will also be called a root.
    """
    def __init__(self):
        self.nodes = [] # A list for containing all the nodes in the tree.
        self.roots = [] # A list of roots. Root = node without parent.


    def new_touched_state(self, template_node=None):
        """
        Creates a new touched state, using the state of
        template_node as a template. Wraps it in a node
        and adds to tree.
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
        mynode = Node(self, state, touched=touched)
        self.add_node(mynode, parent, template_node)
        return mynode


    def add_node(self, node, parent=None, template_node=None):
        """
        Adds a node to the tree.
        The state inside the added node may be a natural state or a touched state.
        If it's a natural state it cannot have a template_node.
        Returns the node.
        """

        if (not node.is_touched()) and (template_node is not None):
            raise StandardError("You tried adding an untouched state to a \
                                 tree while specifying a template_node.")

        if template_node is not None:
            if parent != template_node.parent:
                raise StandardError("Parent you specified and parent of \
                                     template_node aren't the same!")
                # todo: Do something about this shit

        self.nodes.append(node)

        if parent is None:

            if hasattr(node.state, "clock") is False:
                node.state.clock = 0

            self.roots.append(node)
            if node.is_touched():
                if template_node is not None:
                    template_node.derived_nodes.append(node)

        else:
            if hasattr(node.state, "clock") is False:
                node.state.clock = parent.state.clock + 1

            node.parent = parent
            parent.children.append(node)

            if node.is_touched():
                if template_node is not None:
                    template_node.derived_nodes.append(node)
                if parent.block is not None:
                    if parent != parent.block[-1]:
                        parent.block.split(parent.children[0])
            else:
                if parent.block is not None:
                    ind = parent.block.index(parent)
                    number = len(parent.block) - ind
                    if number == 1:
                        if len(parent.children) == 1:
                            parent.block.add([node])
                    else:
                        parent.block.split(parent.block[ind+1])

                else:
                    if len(parent.children) == 1 and parent.is_touched() is False:
                        Block([parent,node])
        return node


    def node_count(self):
        return len(self.nodes)
    
from node import Node