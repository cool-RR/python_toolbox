# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
This module defines the HistoryBrowser class. See its documentation for more
information.
"""

import garlicsim.misc.binary_search as binary_search
import garlicsim.misc.queue_tools as queue_tools
import garlicsim.history_browser_abc

__all__ = ["HistoryBrowser"]

get_state_clock = lambda state: state.clock

class HistoryBrowser(garlicsim.history_browser_abc.HistoryBrowserABC):
    """
    A history browser is a device for requesting states from the timeline of
    the simulation. It is relevant only to simulations that are
    history-dependent.
    This specific kind of history browser, defined in the synchronous_crunching
    package, is intended for synchronously-crunched simulations in which there
    are no worker processes/threads doing the crunching. Therefore, its job is
    quite simple; it recieves a path in its constructor and it handles all
    state requests from that path.
    """
    def __init__(self, path):
        self.path = path        
        """
        This is the path, from which all states will be taken when requested.
        """
     
    def get_last_state(self):
        """"
        Gets the last state in the timeline. Identical to __getitem__(-1).
        """
        return self[-1]
    
    def __getitem__(self, index):
        """
        Returns a state by its position in the timeline.
        """
        assert isinstance(index, int)
        return self.path[index].state
    
    def get_state_by_monotonic_function(self, function, value, rounding="Closest"):
        """
        Requests a state by specifying a measure function and a desired value.
        The function must be a monotonic rising function on the timeline.
        
        See documentation of garlicsim.misc.binary_search.binary_search for
        details about rounding options.
        """
        assert rounding in ["High", "Low", "Exact", "Both", "Closest"]
        
        new_function = lambda node: function(node.state)
        result_in_nodes = self.path.get_node_by_monotonic_function \
                        (new_function, value, rounding)
        
        if rounding == "Both":
            result = [(node.state if node is not None else None) \
                      for node in result_in_nodes]
        else:
            result = result_in_nodes.state if result_in_nodes is not None \
                   else None
            
        return result
    
    def __len__(self):
        """
        Returns the length of the timeline in nodes, which means the sum of:
        1. The length of the work_queue of our cruncher.
        2. The length of the path in the tree which leads to our node, up to
           our node.
        """
        return len(self.path)