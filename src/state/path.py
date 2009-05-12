"""
todo: path's methods should all optimized using Blocks!
"""
import math
import warnings
from tree import *

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

    def iterate_blockwise(self):
        """
        Iterates on the Path, returning Blocks when possible.
        """
        if self.start==None:
            raise StopIteration
        yield self.start.soft_get_block()
        current=self.start.soft_get_block()
        while True:
            try:
                current=self.next_node(current).soft_get_block()
                yield current
            except IndexError:
                raise StopIteration("Ran out of tree")


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
                    raise StandardError("This path has come across a junction for which it has no information! Guessing.")
                    # Can comment out the error when not being too strict
                return kids[0]

        raise IndexError("Ran out of tree")


    def __getitem__(self,i):
        """
        Gets node by number.
        """

        if isinstance(i,int)==True:
            if i<0:
                i=len(self)+i #todo: something more optimized here?
                assert i>=0

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
            raise NotImplementedError #todo
        else:
            return StandardError



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
                if new.block==None:
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


    def get_existing_segments(self,starttime,endtime):
        """
        (Assuming it's only one segment for now)
        Between timepoints "starttime" and "endtime", returns the segment of nodes that
        exists in the Path.
        Returns the segment like so: [[start,end]]
        Example: In the path the first node's clock reading is 3.2, the last is 7.6.
        starttime is 2 and endtime is 5. The function will return [[3.2,5]]
        """
        segs=[]
        foogi=self.get_node_by_time(starttime)
        if foogi==None:
            if starttime<self.start.state.clock<=endtime:
                myseg=[self.start.state.clock,None]
            else:
                return []
        else:
            myseg=[starttime,None]

        last=self[-1]
        myseg[1]=min(last.state.clock,endtime)

        segs+=[myseg]
        return segs

    def distance_between_nodes(self,start,end):
        """
        Returns the distance, in nodes, between "start" and "end"
        """
        # Optimize this with blocks
        assert isinstance(start,Node)
        assert isinstance(end,Node)

        current=start
        dist=0
        while current!=end:
            try:
                current=self.next_node(current)
            except IndexError:
                raise StandardError("The end node was not found")
            dist+=1
        return dist


    """
    Junk:

    def leads_to_same_edge(self,path):
        #todo maybe
        return False

    def cut_off_first(self):
        try:
            second=self.next_node(self.start)
        except IndexError,StopIteration:
            second=None
        return Path(self.tree,second,self.decisions)
    """


