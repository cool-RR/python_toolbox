# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
A module that defines the Node class and the related NodeError exception.

See documentation of Node for more information.
'''

from garlicsim.general_misc.infinity import Infinity
from garlicsim.general_misc import misc_tools

from garlicsim.misc import GarlicSimException

from state import State
from tree_member import TreeMember
# We are doing `from block import Block` in the bottom of the file.
# We are doing `from path import Path` in the bottom of the file.


__all__ = ["Node", "NodeError"]


class NodeError(GarlicSimException):
    '''Node-related Exception.'''

class NodeLookupError(NodeError, LookupError):
    '''A node-related lookup was requested but no result was found.'''
    
    
class Node(TreeMember):
    '''
    Nodes are used to organize states in a tree.
    
    A node encapsulates a state with the attribute `.state`. 
    
    Most nodes are untouched, a.k.a. natural, but some nodes are touched.
    A touched node is a node whose state was not formed naturally by a
    simulation step: It was created by the user, either from scratch or based
    on another state.
    '''
    # todo: Maybe node should not reference tree?
    
    def __init__(self, tree, state, parent=None, step_profile=None,
                 touched=False):
        '''
        Construct the node.
        
        `tree` is the tree in which this node resides. `state` is the state it
        should contain. `parent` is its parent node in the tree, which may be
        None for a root. `step_profile` is the step profile with which the state
        was crunched, which may be None for a state that was created from
        scratch. `touched` is whether the state was modified/created from
        scratch, in contrast to having been produced by crunching.
        '''
        
        self.tree = tree
        '''The tree in which this node resides.'''
        
        self.state = state
        '''The state contained in the node.'''
        
        self.parent = parent
        '''The parent node of this node.'''
        
        self.step_profile = step_profile
        '''
        The step options profile with which the contained state was created.
        
        For an untouched node, this must be a real StepProfile, even an empty
        one. Only a touched node which was created from scratch should have
        None for its step profile.
        '''
        
        self.touched = touched
        '''Says whether the node is a touched node.'''
        
        self.block = None
        '''
        A node may be a member of a block. See class Block for more details.
        '''

        self.children = []
        '''
        A list of:
            1. Nodes whose states were produced by simulation from this node.
            2. Nodes who were "created by editing" from one of the nodes in the
            aforementioned set.
        '''

        self.derived_nodes = []
        '''
        List of nodes who were created by editing from this node.
        
        These nodes should have the same parent as this node.
        '''

        self.still_in_editing = False
        '''
        A flag that is raised for a node which is "still in editing".
        
        This means that its state is still being edited and was not yet
        finalized, thus no crunching should be made from the node until it is
        finalized.
        '''
        
        self.ends = []
        '''
        The ends whose parent is this node.
        
        This means, world ends that were arrived to on a timeline terminating
        with this node.
        '''
  
        
    def __len__(self):
        '''Just return 1. This is useful because of blocks.'''
        return 1

    
    def finalize(self):
        '''
        Finalize the node, assuming it's in currectly in editing mode.
        
        Before an edited node is finalized, it cannot be crunched from and
        cannot have children. (i.e. nodes that follow it in time.) After getting
        finalized, it may be crunched from and be assigned children.
        '''
        if self.still_in_editing is False:
            if self.touched:
                message = '''You tried to finalize a touched node, but it has \
already been finalized.'''
            else: # self.touched is False
                message = '''You tried to finalize an untouched node. \
Untouched nodes can't be edited, so they have no concept of being finalized.'''
            raise NodeError(message)
        
        self.still_in_editing = False

        
    def soft_get_block(self):
        '''
        If this node is a member of a block, return the block.
        
        Otherwise, return the node itself.
        '''
        return self.block or self

    
    def make_containing_path(self):
        '''
        Create a path that contains this node.
        
        There may be multiple different paths that contain this node. This will
        return the one which points to the newest possible forks.
        Returns the path.
        '''
        
        path = self.make_past_path()
        
        path.get_last_node()
        # Calling that will make the path choose the newest forks.
        
        return path
    
        
    def all_possible_paths(self):
        '''
        Get a list of all possible paths that contain this node.
        
        Note: There may be paths that contain this node which will not be
        identical to one of the paths given here, because these other paths
        may specify decisions that are not even on the same root as these
        paths.
        '''
        #todo: possibly add `reversed` option
        past_path = self.make_past_path()
        paths = []
        fork = None
        for thing in past_path.iterate_blockwise(start=self):
            real_thing = thing[-1] if isinstance(thing, Block) else thing
            if len(real_thing.children):
                fork = real_thing
                break
        
        if fork:
            for kid in fork.children:
                paths += kid.all_possible_paths()
            return paths
        else: # fork is None and real_thing is the final node of the path
            # In this case there are no forks after our node, we just return
            # the past_path which we have driven to its end. (Not that it has
            # any forks to decide on anyway.)
            return [past_path]
    
    def make_past_path(self):
        '''
        Create a path that contains this node.
        
        There may be multiple different paths that contain this node. This will
        return a path that doesn't specify any decisions after this node.
        '''
        path = Path(self.tree)

        current = self
        while True:
            if current.block is not None:
                current = current.block[0]
            parent = current.parent
            if parent is None:
                path.root = current
                break
            if len(parent.children) > 1:
                path.decisions[parent] = current
            current = parent

        return path

    def get_all_leaves(self, max_nodes_distance=None, max_clock_distance=None):
        '''
        Get all leaves that are descendents of this node.
        
        Only leaves with a distance of at most `max_nodes_distance` in nodes or
        `max_clock_distance` in clock are returned. (Note this is an OR
        relation between the two condintions)
        
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
        if max_nodes_distance is None:
            max_nodes_distance = Infinity
        if max_clock_distance is None:
            max_clock_distance = Infinity
                    
        nodes = {self: {"nodes_distance": 0, "clock_distance": 0}}
        leaves = {}

        while nodes:
            item = nodes.popitem()
            node = item[0]
            nodes_distance = item[1]["nodes_distance"]
            clock_distance = item[1]["clock_distance"]
            
            if nodes_distance > max_nodes_distance and \
               clock_distance > max_clock_distance:
                continue
            
            kids = node.children
            
            if not kids:
                # We have a leaf!
                leaves[node] = {
                    "nodes_distance": nodes_distance,
                    "clock_distance": clock_distance,
                }
                continue
            
            if (node.block is None) or node.is_last_on_block():
                for kid in kids:
                    nodes[kid] = {
                        "nodes_distance": nodes_distance + 1,
                        "clock_distance": kid.state.clock - self.state.clock,
                    }
                continue
            else:
                block = node.block
                index = block.index(node)
                rest_of_block = (len(block) - index - 1)
                
                # We know the node isn't the last on the block, because we
                # checked for that before.

                last = block[-1]
                nodes[last] = {
                    "nodes_distance": nodes_distance + rest_of_block,
                    "clock_distance": last.state.clock - self.state.clock,
                }
                continue
            
        return leaves

    
    def get_ancestor(self, generations=1, round=False):
        '''
        Get an ancestor of this node.
        
        `generations` specifies the number of generation that the returned
        ancestor should be above the current node. `round` determines how this
        method will behave if it was asked for too many generations back, and
        not enough existed. If `round` is True, it will return the root. If
        `round` is False, it will raise a LookupError.
        '''

        assert generations >= 0
        if generations == 0:
            return self
        if generations == 1:
            if self.parent:
                return self.parent
            else: # self.parent is None
                if round:
                    return self
                else: # round is False
                    raise NodeLookupError('''You asked for the node's parent, \
but it's a root.''')                
                
        block = self.block
        if block:
            our_index = block.index(self)
            wanted_index = our_index - generations
            if wanted_index >= 0:
                return block[wanted_index]
            else: # wanted index < 0
                first_node = block[0]
                parent_of_first = first_node.parent
                if parent_of_first is None:
                    if round:
                        return first_node
                    else: # round is False
                        raise NodeLookupError('''You asked for too many \
generations back. This node's ancestry line doesn't go back that far.''')
                
                return parent_of_first.get_ancestor(- wanted_index - 1, round=round)
        
        assert self.block is None
        if self.parent:
            return self.parent.get_ancestor(generations - 1, round)
        else:
            if round:
                return self
            else: # round is False
                raise NodeLookupError('''You asked for too many generations \
back. This node's ancestry line doesn't go back that far.''')

            
    def get_root(self):
        '''
        Get the root of this node.
        
        This means the node which is the parent of the parent of the parent
        of... the parent of this node.
        '''
        lowest = self.block[0] if self.block else self
        while lowest.parent is not None:
            lowest = lowest.parent
            if lowest.block:
                lowest = lowest.block[0]
        return lowest
    
    def is_last_on_block(self):
        '''Return whether the node the last one on its block.'''
        return self.block and (self.block.index(self) == len(self.block) - 1)
    
    def is_first_on_block(self):
        '''Return whether the node the first one on its block.'''
        return self.block and (self.block.index(self) == 0)
    
    def is_overlapping(self, tree_member):
        '''
        Return whether this node overlaps with the given tree_member.
        
        `tree_member` may be a node, in which case overlapping means being the
        same node. `tree_member` can also be a block, in which case overlapping
        means this node is contained in the block.
        '''
        if tree_member is None: return False
        if isinstance(tree_member, Node):
            return (self is tree_member)
        else:
            assert isinstance(tree_member, Block)
            return (self in tree_member)
    
    def __repr__(self):
        '''
        Get a string representation of the node.
        
        Example output:        
        <garlicsim.data_structures.Node with clock 6.5, untouched, belongs to a
        block, crunched with StepProfile(t=0.1), at 0x1ffde70>
        '''
        return '<%s%s, %s%s%s, %s, %sat %s>' % \
            (
                misc_tools.shorten_class_address(
                    self.__class__.__module__,
                    self.__class__.__name__
                    ),
                ' with clock %s' % self.state.clock if hasattr(self.state, 'clock') else '',
                'root, ' if (self.parent is None) else '',
                'leaf, ' if (len(self.children) == 0) else '',
                'touched' if self.touched else 'untouched',
                'belongs to a block' if self.block else 'blockless',
                'crunched with %s, ' % self.step_profile if self.step_profile else '',
                hex(id(self))
            )

from path import Path
from block import Block


