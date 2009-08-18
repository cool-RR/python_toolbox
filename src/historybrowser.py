"""
todo in the future: because historybrowser
retains a reference to a node, when the user deletes a node
we should mark it so the historybrowser will know it's dead.
"""
import state

class PseudoNode(object):
    def __init__(*args):
        thing = args[0]
        if isinstance(thing, state.Node):
            self.node = thing
            self.type_ = "Node"
            return

def get_state_clock(state): return state.clock

class HistoryBrowser(object):
    def __init__(self, cruncher, initial_node):
        self.cruncher = cruncher
        self.initial_node = initial_node

    def request_by_clock(clock, rounding="Closest"):
        return self.request_by_monotonic_function(function=get_state_clock, rounding)
    
    def request_by_monotonic_function(function, rounding="Closest"):
        """
        Returns a list.
        """
        assert rounding in ["High", "Low", "Exact", "Both", "Closest"]
        
        low = PseudoNode(initial_node.get_root())
        high = PseudoNode(
        
        
    
    
    