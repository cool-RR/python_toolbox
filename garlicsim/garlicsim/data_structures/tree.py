# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
A module that defines the Tree class and the related TreeError exception.

See their documentation for more information.
'''

import copy

import garlicsim

# `from block import Block` in the bottom of the file.
# `from node import Node` in the bottom of the file.

__all__ = ["Tree", "TreeError"]

class TreeError(Exception):
    '''An exception related to the Tree class.'''
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
    also be called a root and be a member of tree.roots.
    '''
    def __init__(self):
        
        self.nodes = []
        '''List of nodes that belong to the tree.'''
        
        self.roots = []
        '''List of roots (parentless nodes) of the tree.'''
        
        self.lock = garlicsim.general_misc.read_write_lock.ReadWriteLock()
        '''
        A read-write lock that guards access to the tree.
        
        We need such a thing because some simulations are history-dependent and
        require reading from the tree in the same time that sync_crunchers could
        potentially be writing to it.
        '''

        
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
        step_profile = copy.copy(template_node.step_profile)
        return self.add_state(x, parent,
                              step_profile=step_profile,
                              template_node=template_node)


    def add_state(self, state, parent=None, step_profile=None,
                  template_node=None):
        '''
        Wrap state in node and adds to tree.
        
        Returns the node.
        '''
        touched = (parent is None) or (template_node is not None)
        
        my_node = Node(
            self,
            state,
            step_profile=copy.copy(step_profile),
            touched=touched
        )
        
        self.__add_node(my_node, parent, template_node)
        return my_node


    def __add_node(self, node, parent=None, template_node=None):
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
                    if (not node.touched) and (parent.step_profile == \
                                               node.step_profile):
                        parent.block.append_node(node)
                else: # parent.children > 1
                    if not (parent is parent.block[-1]):
                        parent.block.split(parent)
            else: # parent.block is None
                if (not node.touched) and (not parent.touched) and \
                   (len(parent.children)==1) and \
                   (parent.step_profile == node.step_profile):
                    Block([parent, node])
                
                        
        else: # parent is None
            if not hasattr(node.state, "clock"):
                node.state.clock = 0
            self.roots.append(node)
            return node


    def all_possible_paths(self):
        '''Return all the possible paths this tree may entertain.'''
        result = []
        for root in self.roots:
            result += root.all_possible_paths()
        return result
    
    def delete_node_selection(self, node_selection, stitch=False):#tododoc
        node_selection.compact()
        for node_range in node_selection.ranges:
            self.delete_node_range(node_range, stitch=stitch)
    
    def delete_node_range(self, node_range, stitch=False):#tododoc
        
        start_node = node_range.start if isinstance(node_range.start, Node) \
                     else node_range.start[0]
        
        end_node = node_range.end if isinstance(node_range.end, Node) \
                     else node_range.end[-1]
        
        if start_node in self.roots:
            self.roots.remove(start_node)
                        
        big_parent = start_node.parent
        if big_parent is not None:
            big_parent.children.remove(start_node)
        
        outside_children = node_range.get_outside_children()
            
        for node in node_range:
            self.nodes.remove(node)

        current_block = None
        last_block_change = None
        for node in node_range:
            if node.block is not current_block:
                if current_block is not None:
                    del current_block[current_block.index(last_block_change) :
                                      current_block.index(node)]
                current_block = node.block
                last_block_change = node
                
        if current_block is not None:
            del current_block[current_block.index(last_block_change) :
                              current_block.index(end_node)]
                    
            
        parent_to_use = big_parent if (stitch is True) else None
        for node in outside_children:
            node.parent = parent_to_use
            if parent_to_use is None:
                self.roots.append(node)
            
        
    
    def __repr__(self):
        '''
        Get a string representation of the tree.
        
        Example output:
        <garlicsim.data_structures.tree.Tree with 1 roots, 233 nodes and 3
        possible paths at 0x1f6ae70>
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
    
    
    def __getstate__(self):
        my_dict = dict(self.__dict__)
        del my_dict['lock']
        return my_dict
    
    
    def __setstate__(self, pickled_tree):
        self.__init__()
        self.__dict__.update(pickled_tree)
        
        
    
from node import Node
from block import Block

