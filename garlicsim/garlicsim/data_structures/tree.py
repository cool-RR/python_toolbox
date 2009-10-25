# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
A module that defines the Tree class and the related TreeError exception. See
their documentation for more information.
'''

import copy

from block import Block
# Note we are doing `from node import Node` in the bottom of the file.

__all__ = ["Tree", "TreeError"]

class TreeError(Exception):
    '''
    An exception related to the class Tree.
    '''
    pass

class Tree(object):
    '''
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
    '''
    def __init__(self):
        self.nodes = []
        '''List of nodes that belong to the tree.'''
        self.roots = []
        '''List of roots (parentless nodes) of the tree.'''

    def fork_to_edit(self, template_node):
        '''
        "Duplicate" the node, marking the new one as touched.
        
        The new node will have the same parent as `template_node`. This
        method is used when forking the tree by editing. The state of the new
        node is usually modified by the user after it is created.
        
        Returns the node.
        '''
        x = copy.deepcopy(template_node.state)

        parent = template_node.parent
        step_options_profile = template_node.step_options_profile
        return self.add_state(x, parent,
                              step_options_profile=step_options_profile,
                              template_node=template_node)


    def add_state(self, state, parent=None, step_options_profile=None,
                  template_node=None):
        '''
        Wrap state in node and adds to tree.
        
        Returns the node.
        '''
        touched = (parent is None) or (template_node is not None)
        
        my_node = Node(
            self,
            state,
            step_options_profile=copy.deepcopy(step_options_profile),
            touched=touched
        )
        
        self.__add_node(my_node, parent, template_node)
        return my_node


    def __add_node(self, node, parent=None, template_node=None): #todo: private?
        '''
        Add a node to the tree.
        
        It may be a natural node or a touched node. If it's a natural node you
        may not specify a template_node.
        
        Returns the node.
        '''
        if template_node is not None:
            if parent != template_node.parent:
                raise TreeError('''Parent you specified and parent of \
template_node aren't the same!''')
            if not node.touched:
                raise TreeError('''You tried adding an untouched state to a \
tree while specifying a template_node.''')
            template_node.derived_nodes.append(node)
            

        self.nodes.append(node)

        if parent:
            if not hasattr(node.state, "clock"):
                node.state.clock = parent.state.clock + 1

            node.parent = parent
            parent.children.append(node)
            
            if parent.block:
                if len(parent.children)==1:
                    if (not node.touched) and (parent.step_options_profile == \
                                               node.step_options_profile):
                        parent.block.append_node(node)
                else: # parent.children > 1
                    if not (parent is parent.block[-1]):
                        parent.block.split(parent)
            else: # parent.block is None
                if (not node.touched) and (not parent.touched) and \
                   (len(parent.children)==1) and \
                   (parent.step_options_profile == node.step_options_profile):
                    Block([parent, node])
                
                        
        else: # parent is None
            if not hasattr(node.state, "clock"):
                node.state.clock = 0
            self.roots.append(node)
            return node


    def all_possible_paths(self):
        '''
        Return all the possible paths this tree may entertain.
        '''
        result = []
        for root in self.roots:
            result += root.all_possible_paths()
        return result
    
    
    def __repr__(self):
        '''
        Get a string representation of the tree.
        
        Example output:
        TODO
        '''
        return '<%s.%s with %s roots, %s nodes and %s possible paths at %s>' % \
               (
                   self.__class__.__module__,
                   self.__class__.__name__,
                   len(self.roots),
                   len(self.nodes),
                   len(self.all_possible_paths()),
                   hex(id(self))
               )
    
from node import Node