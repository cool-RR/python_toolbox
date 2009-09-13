"""

todo: maybe implement history_browser.__len__() ?
"""


import garlicsim.misc.binary_search as binary_search
import garlicsim.misc.queue_tools as queue_tools

__all__ = ["HistoryBrowser"]

get_state_clock = lambda state: state.clock


class HistoryBrowser(object):
    """
    
    """
    def __init__(self, path):
        self.path = path
     
    def get_last_state(self):
        """
        Syntactic sugar for getting the last state in the timeline.
        """
        return self[-1]
    
    
    def __getitem__(self, index):
        """
        Returns a state by its position in the timeline.
        """
        assert isinstance(index, int)
        return self.path[index].state
    
    
    def request_state_by_clock(self, clock, rounding="Closest"):
        """
        Requests a state by specifying desired clock time.
        
        See documentation of garlicsim.misc.binary_search.binary_search for
        details about rounding options.
        """
        assert rounding in ["High", "Low", "Exact", "Both", "Closest"]
        return self.request_state_by_monotonic_function\
               (function=get_state_clock, value=clock, rounding=rounding)
    
    
    def request_state_by_monotonic_function(self, function, value, rounding="Closest"):
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
    
    
    
