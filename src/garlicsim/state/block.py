"""
A module that defines the `Block` class. See
its documentation for more information.
"""

__all__ = ["Block"]

class Block(object):
    """
    A Block is a device for bundling together a succession of natural
    nodes. It makes the tree more organized and easy to browse,
    and improves performance.

    When you're doing a simulation, often you'll have a succession of 1000+
    natural nodes, which were created "organically", each from its parent,
    by simulation. There is no point in displaying a 1000 nodes in the
    tree browser: Therefore they are grouped together into a Block.

    Who qualifies to get wrapped in a block? A succession of untouched nodes,
    which:
    1. Is at least 2 nodes in number
    2. All members, except the last one, must have no children except
       their successor in the block.
    3. The last node may have any kinds of children.

    If you want to check whether a certain node is in a block or not,
    check its ".block" attribute.

    """
    def __init__(self, node_list):
        """
        Constructs a Block from the members of node_list.
        """
        self.list = []

        self.add(node_list)

    def add(self, node_list):
        """
        Adds a list of nodes to the Block.
        These nodes must already be successive.
        They must come right before the block or right after it. (Unless
        the block is empty)
        """
        if self.list:
            if node_list[0].parent == self.list[-1]:
                self.list = self.list + node_list
            elif self.node_list[0].parent == node_list[-1]:
                self.list = node_list + self.list
            else:
                raise StandardError("List of nodes is not adjacent to existing nodes")
        else:
            self.list = node_list[:]

        for i in range(len(node_list)):
            if i >= 1:
                if node_list[i].parent != node_list[i-1]:
                    raise StandardError("Tried to add non-consecutive nodes to block")
            if node_list[i].is_touched():
                raise StandardError("Tried to add touched nodes to block")
            node_list[i].block = self

    def split(self, node):
        """
        Splits block into two blocks, where `node` is the first
        node of the second block of the two.
        If either of the new blocks is too small to be a block,
        it gets deleted, and its nodes will be block-less.
        """
        i = self.list.index(node)
        second_list = self.list[i:]
        self.list = self.list[:i]
        if len(second_list) >= 2:
            Block(second_list)
        else:
            for node in second_list:
                node.block = None
        if len(self.list) <= 2:
            self.delete()


    def delete(self):
        """
        Deletes the block, leaving all nodes without a block.
        """
        for node in self:
            node.block = None

    def __delitem__(self, item):
        """
        Removes a node from the Block. Can only remove
        an edge node.
        """
        if item == 0 or item == -1 or item == len(self) - 1: #is edge?
            self.list[item].block = None
            return self.list.__delitem__(item)
        else:
            return StandardError("Can't remove a node from the middle of a block")

    def __contains__(self, node):
        """
        Returns whether the block contains `node`
        """
        return node.block == self

    def __iter__(self):
        return self.list.__iter__()

    def __len__(self):
        """
        Returns the number of nodes in the block.
        """
        return len(self.list)

    def __getitem__(self, i):
        return self.list[i]

    def index(self, *args, **kwargs):
        return self.list.index(*args,**kwargs)
