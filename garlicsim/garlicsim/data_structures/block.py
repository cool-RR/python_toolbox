# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
A module that defines the Block class and the related BlockError exception.

See the documentation of Block for more information.
'''

from garlicsim.general_misc import logic_tools
from garlicsim.general_misc import misc_tools

from garlicsim.misc import GarlicSimException

from tree_member import TreeMember
# We are doing `from node import Node` in the bottom of the file.

__all__ = ["Block", "BlockError"]


class BlockError(GarlicSimException):
    '''Block-related exception.'''

    
class Block(TreeMember):
    '''
    Succession of similar natural nodes in the tree.
    
    Blocks make the tree more organized and easy to browse, and improve
    performance.

    When you're doing a simulation, often you'll have a succession of 1000+
    natural nodes, which were created "organically", each from its parent,
    by simulation. Having a block to group these nodes together imporves
    efficiency.

    Who qualifies to get wrapped in a block? A succession of untouched nodes,
    which:
        1. Is at least 2 nodes in number.
        2. All members, except the last one, must have no ends, and no
           children except their successor in the block.
        3. The last node may have any kinds of children and ends.
        4. All members share the same step_profile.

    If you want to check whether a certain node is in a block or not,
    check its ".block" attribute.

    '''
    def __init__(self, node_list):
        '''Construct a block from the members of node_list.'''
        self.alive = True
        self.__node_list = []
        self.add_node_list(node_list)

    def soft_get_block(self):
        return self
    
    def append_node(self, node):
        '''
        Append a single node to the block.
        
        If the block's node list is empty, the node will be added
        unconditionally. If the node list contains some nodes, the new node
        must be either a child of the last node or the parent of the first one.
        '''
        
        assert self.alive
        
        if not self.__node_list:
            # If the node list is [], let's make it [node].
            self.__node_list.append(node)
            node.block = self
            return
        
        if node.step_profile != self.get_step_profile():
            raise BlockError('''Tried to add node which has a different
step_profile.''')
            
        
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
        
        raise BlockError('''Tried to add a node which is not a direct \
successor or a direct ancestor of the block.''')

    
    def add_node_list(self, node_list):
        '''
        Add a list of nodes to the block.
        
        These nodes must already be successive to each other.
        Also, one of the following conditions must be true:
            1. The first node in the list is a child of the last node in the
               block.
            2. The last node in the list is the parent of the first node in
               the block.
        '''
        
        assert self.alive
        
        if not node_list:
            return
        
        if len(node_list) == 1:
            self.append_node(node_list[0])
            return
        
        if not logic_tools.all_equal((node.step_profile for node
                                      in node_list)):
            raise BlockError('''Tried to add node list that doesn't share the \
same step options profile.''')
        
        sample_step_profile = node_list[0].step_profile
        
        if self.__node_list and \
           sample_step_profile != self.get_step_profile():
            raise BlockError('''Tried to add nodelist which contains node \
that has a different step_profile.''')
        
        # We now make sure the node_list is successive, untouched, and has no
        # unwanted children.
        for i in xrange(len(node_list)):
            if (i >= 1) and (node_list[i].parent != node_list[i-1]):
                raise BlockError('Tried to add non-consecutive nodes to block.')
            if (len(node_list) - i >= 2) and (len(node_list[i].children) != 1):
                raise BlockError('''Tried to add to the block a node which \
doesn't have exactly one child, and not as the last node in the block.''')
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
            raise BlockError('List of nodes is not adjacent to existing nodes.')

        for node in node_list:
            node.block = self

            
    def split(self, node):
        '''
        Split the block into two blocks.
        
        `node` would be the last node of the first block of the two. If either
        of the new blocks will contain just one node, that block will get
        deleted and the single node will become blockless.
        '''
        assert self.alive
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
        '''Delete the block, leaving all its nodes without a block.'''
        assert self.alive
        for node in self:
            node.block = None
        self.__node_list = []
        self.alive = False

        
    def __delitem__(self, i):
        '''
        Remove a node or a slice of nodes from the block.
        
        Nodes are specified by index number, whether you're removing a single
        node or a slice of them.
        
        When removing a single node, only an edge node can be removed.
        
        Can only remove an edge node.        
        '''
        # todo: allow removing nodes from middle
        # todo: change argument name `i` and seperate to two methods.
        # todo: allow specifying by nodes instead of numbers, both in slices
        # and in single.
        assert self.alive
        
        if isinstance(i, int):
            if (i == 0) or (i == -1) or \
               (i == len(self) - 1) or (i == -len(self)):
                self.__node_list[i].block = None
                return self.__node_list.__delitem__(i)
            elif (-len(self) < i < len(self) - 1):
                    raise BlockError('''Can't remove a node from the \
middle of a block''')
            else:
                raise IndexError('''Tried to remove a node by index, \
while the index was bigger than the block's length.''')
        
        elif isinstance(i, slice):
            if i.start < 0:
                i.start += len(self)
            if i.stop < 0:
                i.stop += len(self)
            
            assert 0 <= i.start <= i.stop < len(self)
            
            start_node, end_node = [self[index] for index in (i.start, i.stop)]
            
            self.split(end_node)

            if self.alive is False:                
                return
            
            if i.start >= 1:                
                self.split(start_node.parent)
                
            if start_node.block is not None:
                start_node.block.delete()
            
        else:
            raise NotImplementedError

    
    def __contains__(self, thing):
        '''Return whether `thing` is a node which this block contains.'''
        # The argument is called `thing` and not `node` because we want to let
        # people put a block in, and we'll just give them False. Saves them
        # checking themselves if what they got is a node.
        assert self.alive
        return isinstance(thing, Node) and thing.block is self

    
    def __iter__(self):
        '''Iterate over the nodes in the block.'''
        assert self.alive
        return self.__node_list.__iter__()

    
    def __len__(self):
        '''Return the number of nodes in the block.'''
        assert self.alive
        return len(self.__node_list)

    
    def __getitem__(self, index):
        '''Get a node by index number from the block'''
        assert self.alive
        return self.__node_list.__getitem__(index)
    
    
    # def __getslice__(self, *args, **kwargs): #todo: can drop because of getitem?
    #     return self.__node_list.__getslice__(*args, **kwargs)

    
    def index(self, node):
        '''Get the index number of the specified node in the block.'''
        assert self.alive
        return self.__node_list.index(node)
    
    
    def get_step_profile(self):
        '''
        Get the step profile of the nodes in this block.
        
        The same profile is used in all of the nodes in the block.
        '''
        assert self.alive
        return self.__node_list[0].step_profile
     
    def is_overlapping(self, tree_member):
        '''
        Return whether this block overlaps with the given tree member.
        
        `tree_member` may be a block, in which case overlapping means being the
        same block. `tree_member` can also be a node, in which case overlapping
        means the node is contained in this block.
        '''
        assert self.alive
        
        if tree_member is None: return False
        if isinstance(tree_member, Block):
            return (self is tree_member)
        else:
            assert isinstance(tree_member, Node)
            return (self in tree_member)
    
    
    def make_containing_path(self):
        '''
        Create a path that contains this block.
        
        There may be multiple different paths that contain this block. This will
        return the one which points to the newest possible forks.
        
        Returns the path.
        '''
        return self[0].make_containing_path()
        
    
    
    def all_possible_paths(self):
        '''
        Get a list of all possible paths that contain this block.
        
        Note: There may be paths that contain this node which will not be
        identical to one of the paths given here, because these other paths may
        specify decisions that are not even on the same root as these paths.
        '''
        return self[0].all_possible_paths()
    
    
    
    def make_past_path(self):
        '''
        Create a path that contains this block.
        
        There may be multiple different paths that contain this node. This will
        return a path that doesn't specify any decisions after this node.
        '''
        return self[0].make_past_path()


    
    def get_all_leaves(self, max_nodes_distance=None, max_clock_distance=None):
        '''
        Get all leaves that are descendents of this block.
        
        Only leaves with a distance of at most `max_nodes_distance` in nodes or
        `max_clock_distance` in clock are returned. (Note this is an OR relation
        between the two condintions)
        
        Returns a dict of the form:
        
        {
            leaf1: {
                'nodes_distance': nodes_distance1,
                'clock_distance': clock_distance1,
            },            
            leaf2: {
                'nodes_distance': nodes_distance2,
                'clock_distance': clock_distance2,
            },
            # ...
        }
            
        '''
        return self[-1].make_containing_path(max_nodes_distance,
                                             max_clock_distance)

    
    
    def get_ancestor(self, generations=1, round=False):
        '''
        Get an ancestor of this block.
        
        `generations` specifies the number of generation that the returned
        ancestor should be above the current block. `round` determines how this
        method will behave if it was asked for too many generations back, and
        not enough existed. If `round` is True, it will return the root. If
        `round` is False, it will raise a LookupError.
        '''
        return self[0].get_ancestor(generations, round)

    
    
    def get_root(self):
        '''
        Get the root of this block.
        
        This means the node which is the parent of the parent of the parent
        of... the parent of this block.
        '''
        return self[0].get_root()

    
    def __repr__(self):
        '''
        Get a string representation of the block.
        
        Example output:
        <garlicsim.data_structures.Block of length 40 crunched with
        StepProfile(t=0.1) at 0x1c84d70>
        '''
        assert self.alive # todo: say "Dead block"
        return '<%s of length %s, crunched with %s at %s>' % \
               (
                   misc_tools.shorten_class_address(
                       self.__class__.__module__,
                       self.__class__.__name__
                   ),
                   len(self),
                   self.get_step_profile(),
                   hex(id(self))
               )
        
from node import Node