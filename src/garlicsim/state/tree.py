"""
A module that defines the `Tree` class. See
its documentation for more information.
"""

import copy as _copy

from node import *
from block import *

__all__=["Tree"]


class Tree(object):
    """
    A tree of nodes. Each node encapsulates a state.

    A tree is used within a Project to organize everything that
    is happenning in the simulation. Often, when doing a simulation,
    this tree will be a "degenerate" tree, i.e. a straight, long
    succession of nodes with no more than one child each.
    However, trees are useful, because they give you the ability
    to "split" or "fork" the simulation at any node you wish,
    allowing you to explore and analyze different "scenarios"
    in parallel in the same simulation.


    How does the tree work?
    There is a list of nodes. Each node has the properties:
    ".parent", ".children" and ".dervied_nodes" within it,
    which refer to its relatives.

    Each node may have a parent, or may not, in which case it will also be called a root.

    maybe todo: make method fastaddstate (or fastaddnode)

    """
    def __init__(self):
        self.nodes=[] # A list for containing all the nodes in the tree.
        self.roots=[] # A list of roots. Root = node without parent.


    def new_touched_state(self,template_node=None):
        """
        Creates a new touched state, using the state of
        template_node as a template. Wraps it in a node
        and adds to tree.
        Returns the node.
        """

        x=_copy.deepcopy(template_node.state)
        x._State__touched=True

        if template_node==None:
            parent=None
        else:
            parent=template_node.parent

        return self.add_state(x,parent,template_node)


    def add_state(self,state,parent=None,template_node=None):
        """
        Wraps state in node and adds to tree.
        Returns the node.
        """
        mynode=Node(self,state)
        self.add_node(mynode,parent,template_node)
        return mynode


    def add_node(self,node,parent=None,template_node=None):
        """
        Adds a node to the tree.
        The state inside the added node may be a natural state or a touched state.
        If it's a natural state it cannot have a template_node.
        Returns the node.

        todo: organize?
        """

        mystate=node.state
        if mystate.is_touched() is False and template_node is not None:
            raise StandardError("You tried adding an untouched state to a tree while specifying a template_node.")

        if template_node is not None:
            if parent!=template_node.parent:
                raise StandardError("parent you specified and parent of template_node aren't the same!") # todo: Do something about this shit

        self.nodes.append(node)

        if parent is None:

            if hasattr(node.state,"clock") is False:
                node.state.clock=0

            self.roots.append(node)
            if mystate.is_touched():
                if template_node is not None:
                    template_node.derived_nodes.append(node)

        else:
            if hasattr(node.state,"clock") is False:
                node.state.clock=parent.state.clock+1

            node.parent=parent
            parent.children.append(node)

            if mystate.is_touched():
                if template_node is not None:
                    template_node.derived_nodes.append(node)
                if parent.block is not None:
                    if parent!=parent.block[-1]:
                        parent.block.split(parent.children[0])
            else:
                if parent.block is not None:
                    ind=parent.block.index(parent)
                    number=len(parent.block)-ind
                    if number==1:
                        if len(parent.children)==1:
                            parent.block.add([node])
                    else:
                        parent.block.split(parent.block[ind+1])

                else:
                    if len(parent.children)==1 and parent.state.is_touched() is False:
                        Block([parent,node])
        return node


    def node_count(self):
        return len(self.nodes)


    """
    Removing:

    def new_natural_state(self,parent):
        \"""
        Creates a new natural State, wraps in node and adds to tree.
        Returns the node.
        \"""
        x=State(touched=False)
        return self.add_state(x,parent)
    """