"""
A module that defines the `Path` class. See
its documentation for more information.

todo: path's methods should all optimized using Blocks!
are they already?
"""

import warnings
from tree import *
from node import *
from block import *

def get_state_clock(): return state.clock # misc this

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


    def __getitem__(self, i):
        """
        Gets node by number.
        """

        if isinstance(i,int)==True:
            if i<0:
                if i==-1:
                    return self.get_last()
                else: # i < -1
                    i=len(self) + i #todo: something more optimized here?

            index = -1
            for j in self.iterate_blockwise():
                index += len(j)
                if index >= i:
                    if isinstance(j,Block):
                        return j[-(index-i)-1]
                    else:
                        assert index==i
                        return j
            raise IndexError

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
    
    def request_node_by_clock(self, clock, rounding="Closest"):
        return self.request_by_monotonic_function(function=get_state_clock, value=clock, rounding=rounding)    
        
    def request_node_by_monotonic_function(self, function, value, rounding="Closest"):
        assert rounding in ["High", "Low", "Exact", "Both", "Closest"]        
        
        get = lambda item: function(item[1].state)
        
        low = [0, self.start]
        high = [len(self)-1, self[-1]]
        
        low_value, high_value = get(low), get(high)
        
        if low_value >= value:
            if rounding == "Both":
                return [None, low[1]]
            if rounding in ["High", "Closest"] or (low_value==value and rounding=="Exact"):
                return low[1]
            else: # rounding == "Low" or (rounding == "Exact" and low_value!=value)
                return None
        if high_value <= value:
            if rounding == "Both":
                return [high[1], None]
            if rounding in ["Low", "Closest"] or (low_value==value and rounding=="Exact"):
                return high[1]
            else: # rounding == "High" or (rounding == "Exact" and low_value!=value)
                return None
        
        """
        Now we know the value is somewhere inside the path.
        """
        
        while high[0] - low[0] > 1: # Not sure this section is efficient, since we're doing lots of getitem
            medium_index = (low[0] + high[0]) // 2
            medium = [medium_index, self[medium_index]]
            medium_value = get(medium)
            if medium_value > value:
                high = medium; high_value = medium_value
                continue
            if medium_value < value:
                low = medium; low_value = medium_value
                continue
            if medium_value == value:
                after_medium = [medium[0]+1, self[medium[0]+1]]
                after_medium_value = get(after_medium)
                before_medium = [medium[0]-1, self[medium[0]-1]]
                if get(after_medium) == value:
                    low = medium; low_value = medium_value
                    high = after_medium; high_value = after_medium_value
                    break
                else: # get(after_medium) > value
                    high = medium; high_value = medium_value
                    low = before_medium; low_value = get(before_medium)
                    break
                
        both = [node for [number, node] in (low, high)]
        
        return make_both_data_into_preferred_rounding(both, function, value, rounding)
        
        

    def get_node_by_time(self, time):
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

def make_both_data_into_preferred_rounding(both, function, value, rounding):
    if rounding == "Both": return both
    elif rounding == "Low": return both[0]
    elif rounding == "High": return both[1]
    elif rounding == "Exact": return [state for state in both if (state is not None and function(state)==value)][0]
    elif rounding == "Closest":
        if both[0] is None: return both[1]
        if both[1] is None: return both[0]
        distances = [abs(function(state)-value) for state in both]
        if distances[0] <= distances[1]:
            return both[0]
        else:
            return both[1]
    