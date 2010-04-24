# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines the NodeSelection class.

See its documentation for more info.
'''

from garlicsim.misc import GarlicSimException
from garlicsim.general_misc import cute_iter_tools

from node import Node
from node_range import NodeRange

__all__ = ['NodeSelection']


class CompletelyCompact(GarlicSimException):
    '''The NodeSelection is already completely compact.'''
    

class NodeSelection(object):
    '''
    A selection of nodes.
    
    A NodeSelection could be described as a "set" of nodes, though the nodes are
    not specified one by one, but as a collection of node ranges.
    '''
    def __init__(self, ranges=()):
        '''
        Construct the NodeSelection.
        
        `ranges` is a list of node ranges that this selection will be made of.
        '''
        self.ranges = [ranges] if isinstance(ranges, NodeRange) else \
                      list(ranges)
        
    def compact(self):
        '''
        Compact the NodeSelection.
        
        This'll make it use the minimum number of node ranges while still
        containing exactly the same nodes.
        '''
        for node_range in self.ranges:
            node_range._sanity_check()
        
        try:
            while True:
                self.__partially_compact()
        except CompletelyCompact:
            return
            
    def __partially_compact(self):
        '''Try to make the NodeSelection a bit more compact.'''
        # todo: consider defining a canonic decomposition of a node selection to
        # node ranges. This will make a few things easier, like checking
        # equality.
        first, second = None, None
        for (r1, r2) in cute_iter_tools.orderless_combinations(self.ranges, 2):
            if r1.start in r2:
                second, first = r1, r2
                break
            elif r2.start in r1:
                first, second = r1, r2
                break
            else:
                pass
        if first is not None and second is not None:
            if second.end in first:
                pass
            else: # second.end not in first
                for current in second:
                    if current not in first:
                        break
                if current.parent is first.end:
                    self.ranges.remove(first)
                    new_range = NodeRange(start=first.start, end=second.end)
                else:
                    new_range = NodeRange(start=current, end=second.end)
                self.ranges.append(new_range)
              
            self.ranges.remove(second)
            return
        else:
            raise CompletelyCompact
    
    def __iter__(self):
        '''Iterate over the nodes that are members of this NodeSelection.'''
        for node_range in self.ranges:
            for node in node_range:
                yield node
    
    def __or__(self, other):
        '''Perform a union between two NodeSelections and return the result.'''
        assert isinstance(other, NodeSelection)
        return NodeSelection(self.ranges + other.ranges)
    
    def __ror__(self, other):
        return self.__or__(other)
    
    def __eq__(self, other):
        # Currently horribly inefficient
        if not isinstance(other, NodeSelection):
            return False # todo: should be NotImplemented?
        return set(self) == set(other)
        
    def __req__(self, other):
        return self.__eq__(other)
    
    def copy(self):
        '''Shallow-copy the NodeSelection.'''
        klass = type(self)
        return klass((node_range.copy() for node_range in self.ranges))
    
    
    __copy__ = copy
    
    