# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

import abc

class HistoryBrowserABC(object):
    """
    HistoryBrowserABC is an abstract base class for history browsers, created
    with the abc module from Python's standard library. See abc's documentation
    for more information.
    All history browsers should be based on this class.
    A history browser is a device for requesting states from the timeline of
    the simulation. It is relevant only to simulations that are
    history-dependent.
    """
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def get_last_state(self):
        """
        Gets the last state in the timeline. Identical to __getitem__(-1).
        """
        pass
    
    @abc.abstractmethod
    def __getitem__(self):
        """
        Returns a state by its position in the timeline.
        """
        pass
    
    @abc.abstractmethod
    def get_state_by_clock(self):
        """
        Requests a state by specifying desired clock time.
        
        See documentation of garlicsim.misc.binary_search.binary_search for
        details about rounding options.
        """
        pass
    
    @abc.abstractmethod
    def get_state_by_monotonic_function(self):
        """
        Requests a state by specifying a measure function and a desired value.
        The function must be a monotonic rising function on the timeline.
        
        See documentation of garlicsim.misc.binary_search.binary_search for
        details about rounding options.
        """
        pass
    
    @abc.abstractmethod
    def __len__(self):
        """
        Returns the length of the timeline in nodes, which means the sum of:
        1. The length of the work_queue of our cruncher.
        2. The length of the path in the tree which leads to our node, up to
           our node.
        """
        pass
    
    