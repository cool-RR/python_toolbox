# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
A module that defines the Block class and the related BlockError exception. See
the documentation of Block for more information.
"""

__all__ = ["Block", "BlockError"]

class BlockError(Exception):
    """
    An exception related to the class Block.
    """
    pass

class Block(object):
    """
    A block is a device for bundling together a succession of natural nodes.
    It makes the tree more organized and easy to browse, and improves
    performance.

    When you're doing a simulation, often you'll have a succession of 1000+
    natural nodes, which were created "organically", each from its parent,
    by simulation. There is no point in displaying a 1000 nodes in the tree
    browser: Therefore they are grouped together into a block.

    Who qualifies to get wrapped in a block? A succession of untouched nodes,
    which:
    1. Is at least 2 nodes in number.
    2. All members, except the last one, must have no children except
       their successor in the block.
    3. The last node may have any kinds of children.

    If you want to check whether a certain node is in a block or not,
    check its ".block" attribute.

    """
    def __init__(self, node_list):
        """
        Constructs a block from the members of node_list.
        """
        self.__node_list = []
        self.add_node_list(node_list)

    def append_node(self, node):
        """
        Appends a single node to the block. If the block's node list is empty,
        the node will be added without any condition. If the node list contains
        some nodes, the new node must be either a child of the last node or the
        parent of the first one.
        """
        if not self.__node_list:
            # If the node list is [], let's make it [node].
            self.__node_list.append(node)
            node.block = self
            return
        
        # If the flow reached here, the block is not empty.
        last_in_block = self.__node_list[-1]
        if node.parent == last_in_block:
            # We're appending the node to the end of the block.
            self.__node_list.append(node)
            node.block = self
            return
        
        first_in_block = self.__node_list[0]
        if node == first_in_block.parent:
            # We're appending the node to the start of the block.
            self.__node_list.insert(0, node)
            node.block = self
            return
        
        raise BlockError("""Tried to add a node which is not a direct \
        successor or a direct ancestor of the block.""")
        
    def add_node_list(self, node_list):
        """
        Adds a list of nodes to the Block.
        These nodes must already be successive to each other.
        Also, one of the following conditions must be true:
            1. The first node in the list is a child of the last node in the
               block.
            2. The last node in the list is the parent of the first node in
               the block.
        """

        if not node_list:
            return
        
        if len(node_list) == 1:
            self.append_node(node_list[0])
            return
        
        # We now make sure the node_list is successive, untouched, and has no
        # unwanted children.
        for i in range(len(node_list)):
            if (i >= 1) and (node_list[i].parent != node_list[i-1]):
                raise BlockError("""Tried to add non-consecutive nodes to \
                block.""")
            if (len(node_list) - i >= 2) and (len(node_list[i].children) != 1):
                raise BlockError("""Tried to add to the block a node which \
                doesn't have exactly one child, and not as the last node in \
                the block.""")
            if node_list[i].touched:
                raise BlockError("Tried to add touched nodes to block.")
        
        if not self.__node_list:
            # If the node list is empty, our job is simple.
            self.__node_list = list(node_list)
            for node in node_list:
                node.block = self
            return
        
        if node_list[0].parent == self.__node_list[-1]:
            self.__node_list = self.__node_list + node_list
        elif self.__node_list[0].parent == node_list[-1]:
            self.__node_list = node_list + self.__node_list
        else:
            raise BlockError("""List of nodes is not adjacent to existing \
            nodes""")

        for node in node_list:
            node.block = self

    def split(self, node):
        """
        Splits block into two blocks, so `node` would be the last node of the
        first block of the two. If either of the new blocks will contain just
        one node, that block will get deleted and the single node will become
        blockless.
        """
        assert node in self
        i = self.__node_list.index(node)
        second_list = self.__node_list[i+1:]
        self.__node_list = self.__node_list[:i+1]
        if len(second_list) >= 2:
            Block(second_list)
        else:
            for node in second_list:
                node.block = None
        if len(self.__node_list) <= 1:
            self.delete()


    def delete(self):
        """
        Deletes the block, leaving all nodes without a block.
        """
        for node in self:
            node.block = None
        self.__node_list = []

    def __delitem__(self, i):
        """
        Removes a node from the block. Can only remove an edge node.
        """
        if (i == 0) or (i == -1) or (i == len(self) - 1) or (i == -len(self)):
            self.__node_list[i].block = None
            return self.__node_list.__delitem__(i)
        else:
            if -len(self) < i < len(self) - 1:
                raise NotImplementedError("""Can't remove a node from the \
                middle of a block""")
            else:
                raise IndexError("""Tried to remove a node by index, while \
                the index was bigger than the block's length.""")

    def __contains__(self, node):
        """
        Returns whether the block contains `node`.
        """
        return node.block == self

    def __iter__(self):
        return self.__node_list.__iter__()

    def __len__(self):
        """
        Returns the number of nodes in the block.
        """
        return len(self.__node_list)

    def __getitem__(self, i):
        return self.__node_list[i]

    def index(self, node):
        """
        Returns the index number of the specified node in the block.
        """
        return self.__node_list.index(node)
