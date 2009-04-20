"""
todo: path should be able to skip on n3blocks!
"""

import warnings
from tree import *

class Path(object):
    """
    A path symbolizes a line of nodes in a tree.
    A tree may be a complex tree with many junctions,
    but a path is a direct line. Therefore, a path object contains
    information about which child to choose when going through
    a node which has multiple children.

    Question: Assume you have a path defined, and now the
    tree is having some nodes added to it, making
    new decisions for the path necessary. what should the
    path do?
    should there be an automatic thing that will alert the path to it?
    maybe in the tree method for adding nodes?

    Question:
    in the decisions dict, will it be allowed that a key or value will be a Block?

    todo:
    beware case when there is a decision to go to a node which was deleted
    """
    def __init__(self,tree,start=None,decisions={}):
        #tree.path+=[self]
        self.tree=tree
        self.start=start
        self.decisions=decisions.copy()


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


    def next_node(self,i):
        if self.decisions.has_key(i):
            return self.decisions[i]
        else:
            if isinstance(i,Block):
                kids=i[-1].children
            else:
                kids=i.children
            if len(kids)>0:
                if len(kids)>1:
                    warnings.warn("This path has come across a junction for which it has no information! Guessing.")
                return kids[0]

        raise IndexError("Ran out of tree")


    def __getitem__(self,i):

        if isinstance(i,int)==True:
            if i<0:
                i=len(self)+i #todo: something more optimized here?

            index=-1
            for j in self:
                index+=len(j)
                if index>=i:
                    if isinstance(j,Block):
                        return j[index-i]
                    else:
                        return j

        elif isinstance(i,slice)==True:
            raise NotImplementedError #todo
        else:
            return StandardError

    def cut_off_first(self):
        try:
            second=self.next_node(self.start)
        except IndexError,StopIteration:
            second=None
        return Path(self.tree,second,self.decisions)

    def get_node_by_time(self,time):
        """
        Gets the node in path which "occupies" the timepoint "time".
        This means that, if there is a node which is after "time", it
        returns the node immediately before it (if there is one). Otherwise, returns None.
        """
        low=self.start
        if time<low.state.clock:
            #raise StandardError("You looked for a node with a clock reading of "+str(time)+", while the earliest node had a clock reading of "+str(self.start.state.clock))
            return None
        """
        second=self[self.start]
        guessedrate=second.nib.time-self.start.nib.time

        try:
            new=round((time-self.start.nib.clock)/float(guessedrate))+2
            if
        except:
            high=self[-1]
        """
        while True:
            try:
                new=self.next_node(low)
                if new.state.clock>time:
                    return low
                low=new
            except StopIteration:
                return None
            except IndexError:
                return None


    def get_rendered_segments(self,starttime,endtime):
        """
        Assuming it's only one segment for now
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


    """
    def leads_to_same_edge(self,path):
        #todo maybe
        return False
    """


