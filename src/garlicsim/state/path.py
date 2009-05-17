"""
A module that defines the `Path` class. See
its documentation for more information.

todo: path's methods should all optimized using Blocks!
"""

import warnings
from tree import *
from node import *
from block import *

class Path(object):
    """
    A path symbolizes a line of nodes in a tree.
    A tree may be a complex tree with many junctions,
    but a path is a direct line. Therefore, a path object contains
    information about which child to choose when going through
    a node which has multiple children.


    todo:
    beware case when there is a decision to go to a node which was deleted
    """
    def __init__(self,tree,start=None,decisions={}):
        #tree.path+=[self]
        self.tree=tree

        self.start=start # The starting node

        self.decisions=decisions.copy()
        """
        The decisions dict says which fork of the road the path chooses.
        It's of the form {parent_node:child_node,...}
        Note: child_node is always a node, but I'm currently not negating the
        possibilty that parent_node will actually be a block.
        """


    def __len__(self):
        if self.start==None:
            raise StandardError("Tried to get len of path which has no start node")

        result=0
        for j in self.iterate_blockwise():
            result+=len(j)

        return result

    def __iter__(self):
        if self.start==None:
            raise StopIteration
        yield self.start
        current=self.start
        while True:
            try:
                current=self.next_node(current)
                yield current
            except IndexError:
                raise StopIteration("Ran out of tree")

    def iterate_blockwise(self,starting_at=None):
        """
        Iterates on the Path, returning Blocks when possible.
        You are allowed to specify a node/block from
        which to start iterating, using the parameter `starting_at`.
        """
        if starting_at is None:
            if self.start==None:
                raise StopIteration
            current=self.start.soft_get_block()
        else:
            current=starting_at.soft_get_block()

        yield current

        while True:
            try:
                current=self.next_node(current).soft_get_block()
                yield current
            except IndexError:
                raise StopIteration("Ran out of tree")

    def __contains__(self,thing):
        """
        Returns whether the path contains `thing`.
        `thing` may be a Node or a Block.
        """
        assert isinstance(thing,Node) or isinstance(thing,Block)

        for x in self.iterate_blockwise():
            if x is thing:
                return True
            elif isinstance(x,Block) and thing in x:
                return True

        return False


    def next_node(self,thing):
        """
        Returns the next node on the path.
        """
        if self.decisions.has_key(thing):
            next=self.decisions[thing]
            assert isinstance(next,Node)
            return self.decisions[thing]
        if isinstance(thing,Block):
            if self.decisions.has_key(thing[-1]):
                return self.decisions[thing[-1]]

        else:
            if isinstance(thing,Block):
                kids=thing[-1].children
            else:
                kids=thing.children
            if len(kids)>0:
                if len(kids)>1:
                    warnings.warn("This path has come across a junction for which it has no information! Guessing.")
                    raise StandardError("This path has come across a junction for which it has no information!")
                    # Can comment out the error when not being too strict
                return kids[0]

        raise IndexError("Ran out of tree")


    def __getitem__(self,i):
        """
        Gets node by number.
        """

        if isinstance(i,int)==True:
            if i<0:
                if i==-1:
                    return self.get_last()
                i=len(self)+i #todo: something more optimized here?
                if i<0: raise IndexError


            index=-1
            for j in self.iterate_blockwise():
                index+=len(j)
                if index>=i:
                    if isinstance(j,Block):
                        return j[-(index-i)-1]
                    else:
                        assert index==i
                        return j

        elif isinstance(i,slice)==True:
            raise NotImplementedError
        else:
            return StandardError


    def get_last(self,starting_at=None):
        """
        Returns the last node in the path.
        Optionally, you are allowed to specify a node from
        which to start searching.
        """
        for thing in self.iterate_blockwise(starting_at=starting_at):
            pass

        if isinstance(thing,Block):
            return thing[-1]
        else:
            return thing

    def get_node_by_time(self,time):
        """
        Gets the node in path which "occupies" the timepoint "time".
        This means that, if there is a node which is right after "time", it
        returns the node immediately before it (if there is one). Otherwise, returns None.

        """
        low=self.start
        if time<low.state.clock:
            return None

        while True:
            try:
                new=self.next_node(low)
                if new.block is None:
                    if new.state.clock>time:
                        return low
                    low=new
                    continue
                else:
                    block=new.block
                    if block[0].state.clock>time:
                        return low
                    elif block[-1].state.clock<=time:
                        low=block[-1]
                        continue
                    else: # our man is in the block!

                        left=0
                        right=len(block)-1

                        while right-left>1:
                            middle=(left+right)//2
                            if block[middle].state.clock>time:
                                right=middle
                            else:
                                left=middle

                        return block[left]

            except StopIteration:
                return None
            except IndexError:
                return None



    def distance_between_nodes(self,start,end):
        """
        Returns the distance, in nodes, between the two nodes:
        `start` and `end`.
        """
        # Optimize this with blocks
        assert isinstance(start,Node)
        assert isinstance(end,Node)

        dist=0
        for thing in self.iterate_blockwise(start):
            if end is thing:
                return dist
            elif isinstance(thing,Block) and end in thing:
                dist+=thing.index(end)
                return dist
            else:
                dist+=len(thing)

        raise StandardError("The end node was not found")

    def get_existing_time_segment(self,start_time,end_time):
        """
        Between timepoints "start_time" and "end_time", returns the segment of nodes that
        exists in the Path.
        Returns the segment like so: [start,end]
        Example: In the path the first node's clock reading is 3.2, the last is 7.6.
        start_time is 2 and end_time is 5. The function will return [3.2,5]
        """

        foogi=self.get_node_by_time(start_time)
        if foogi==None:
            if start_time<self.start.state.clock<=end_time:
                myseg=[self.start.state.clock,None]
            else:
                return None
        else:
            myseg=[start_time,None]

        last=self[-1]
        myseg[1]=min(last.state.clock,end_time)


        return myseg

