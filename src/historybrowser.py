"""
todo in the future: because historybrowser
retains a reference to a node, when the user deletes a node
we should mark it so the historybrowser will know it's dead.

make it easy to use hisotrybrowser's method from a separate thread,
so when waiting for a lock the Cruncher could still be productive.
"""
import threading
import state

from misc.queuegetitem import queue_get_item

class PseudoNode(object):
    def __init__(*args):
        thing = args[0]
        if isinstance(thing, state.Node):
            self.node = thing
            self.type_ = "Node"
            return

def get_state_clock(state): return state.clock

class HistoryBrowser(object):
    def __init__(self, cruncher):
        self.cruncher = cruncher
        self.project = cruncher.project
        self.tree = self.project.tree
        self.tree_lock = self.project.tree_lock
        #self.cruncher_mapping_lock = self.project.cruncher_mapping_lock

    def request_by_clock(clock, rounding="Closest"):
        return self.request_by_monotonic_function(function=get_state_clock, value=clock, rounding=rounding)
    
    def request_by_monotonic_function(function, value, rounding="Closest"):
        """
        Returns a list.
        """
        assert rounding in ["High", "Low", "Exact", "Both", "Closest"]
        current_thread = threading.currentThread()
        with self.tree_lock.read:
            our_edge = [edge for (edge, cruncher) in self.project.edges_to_crunch.items() if cruncher==current_thread][0]
            
            highest_in_tree = our_edge
            
            value_of_highest_in_tree = function(highest_in_tree.state)
            if value_of_highest_in_tree >= value:
                return self.request_by_monotonic_function_from_tree(our_edge, function, value, rounding)
            else:
                temp = self.request_by_monotonic_function_from_queue(function, value, rounding="Both")
                if len(temp) == 2:
                    # The result is entirely in the queue
                    if rounding == "Both": return temp
                    elif rounding == "Low": return temp[0]
                    elif rounding == "High": return temp[1]
                    elif rounding == "Exact": return [state for state in temp if function(state)==value)]
                    elif rounding == "Closest":
                        distances = [abs(function(state)-value) for state in temp]
                        if distances[0] <= distances[1]:
                            return temp[0]
                        else:
                            return temp[1]
                elif len(temp)==1:
                    """
                    The result is on or beyond the edge of the queue.
                    """
                    
                elif len(temp)==0:
                    #booga
                    pass     
            
        
    def request_by_monotonic_function_from_tree(our_edge, function, value, rounding="Closest"):
        get = lambda number: function(queue_get_item(queue, number))
        pass
        
    def request_by_monotonic_function_from_queue(function, value, rounding="Closest"):
        queue = self.cruncher.work_queue
        queue_size = queue.qsize()
        
        get = lambda number: function(queue_get_item(queue, number))

        low = 0
        high = queue_size - 1

        low_value, high_value = get(low), get(high)
        
        if low_value >= value:
            if rounding in ["Both", "High", "Closest"] or (low_value==value and rounding=="Exact"):
                return [queue_get_item(queue, low)]
            else: # rounding in ["Low"] or (rounding in ["Exact"] and low_value!=value)
                return []
        if high_value <= value:
            if rounding in ["Both", "Low", "Closest"] or (low_value==value and rounding=="Exact"):
                return [queue_get_item(queue, high)]
            else: # rounding in ["High"] or (rounding in ["Exact"] and low_value!=value)
                return []
            
        """
        Now we know the value is somewhere inside the queue.
        """
        
        while high - low > 1:
            medium = (low + high) // 2
            medium_value = get(medium)
            if medium_value > value:
                high = medium; high_value = medium_value
                continue
            if medium_value < value:
                low = medium; low_value = medium_value
                continue
            if medium_value == value:
                after_medium = medium + 1;
                after_medium_value = get(after_medium)
                if after_medium_value == value:
                    low = medium; low_value = medium_value
                    high = after_medium; high_value = after_medium_value
                    break
                else: # get(medium+1) > value
                    high = medium; high_value = medium_value
                    low = medium - 1; low_value = get(low)
                    break
        !!!
        return [queue_get_item(queue, number) for number in (low, high)]
                