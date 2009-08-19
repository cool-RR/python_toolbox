"""
todo in the future: because historybrowser
retains a reference to a node, when the user deletes a node
we should mark it so the historybrowser will know it's dead.

make it easy to use hisotrybrowser's method from a separate thread,
so when waiting for a lock the Cruncher could still be productive.


maybe I've exaggerated in using @with_self in so many places?
"""
import threading
import state
import crunchers

from misc.queuegetitem import queue_get_item
from state import make_both_data_into_preferred_rounding

def get_state_clock(state): return state.clock

def with_self(method):
    """
    Maybe we will want to check whether we own the lock
    """
    def fixed(self, *args, **kwargs):
        with self:
            return method(self, *args, **kwargs)
    return fixed

class HistoryBrowser(object):
    def __init__(self, cruncher):
        self.cruncher = cruncher
        self.project = cruncher.project
        self.tree = self.project.tree
        self.tree_lock = self.project.tree_lock
        #self.cruncher_mapping_lock = self.project.cruncher_mapping_lock
    
    def __enter__(self, *args, **kwargs):
        self.tree_lock.acquireRead()
    
    def __exit__(self, *args, **kwargs):
        self.tree_lock.release()
     
    @with_self
    def get_last_state(self):
        return self[-1]
    
    @with_self
    def __getitem__(self, index):
        """
        Returns a state by its position.
        """
        assert isinstance(index, int)
        if index < 1:
            return self.__get_item_negative(index)
        else: # index >= 0
            return self.__get_item_positive(index)
    
    @with_self
    def __get_item_negative(self, index):
        try:
            return self.__get_item_from_queue(index)
        except IndexError:
            # The requested state is in the tree
            queue_size = self.cruncher.work_queue.qsize()
            new_index = index + queue_size
            our_leaf = self.__get_our_leaf()
            path = our_leaf.make_containing_path()            
            return path[new_index].state
    
    @with_self
    def __get_item_positive(self, index):
        our_leaf = self.__get_our_leaf()
        path = our_leaf.make_containing_path()
        try:
            return path[index].state
        except IndexError:
            path_length = len(path)
            assert path_length-1 < index
            try:
                return self.__get_item_from_queue(index - path_length)
            except IndexError:
                raise IndexError("The path and the cruncher's work_queue together hold " +
                               str(path_length + self.cruncher.work_queue.qsize()) +
                               " states, and you asked for state number " + str(index) +
                               ".")
            
    
    @with_self
    def __get_item_from_queue(self, index):
        return queue_get_item(self.cruncher.work_queue, index)
    
    @with_self
    def request_state_by_clock(self, clock, rounding="Closest"):
        return self.request_state_by_monotonic_function(function=get_state_clock, value=clock, rounding=rounding)
    
    @with_self
    def request_state_by_monotonic_function(self, function, value, rounding="Closest"):
 
        assert rounding in ["High", "Low", "Exact", "Both", "Closest"]
        our_leaf = self.__get_our_leaf()
        
        
        tree_result = self.request_state_by_monotonic_function_from_tree(our_leaf, function, value, rounding="Both")
        if tree_result[1] is not None:
            # Then there is no need to check the queue even.
            return make_both_data_into_preferred_rounding(tree_result, function, value, rounding)
        
        else:
            queue_result = self.request_state_by_monotonic_function_from_queue(function, value, rounding="Both")
            none_count = queue_result.count(None)
            if none_count == 0:
                # The result is entirely in the queue
                return make_both_data_into_preferred_rounding(queue_result, function, value, rounding)
            elif none_count == 1:
                """
                The result is on or beyond the edge of the queue.
                """
                if queue_result[1] == None:
                    # The result is either the most recent state in the queue or "after" it
                    return make_both_data_into_preferred_rounding(queue_result, function, value, rounding)
                else: # queue_result[0] == None
                    """
                    Getting tricky: The result is somewhere in the middle between
                    the queue and the tree.
                    """
                    combined_result = [tree_result[0], queue_result[1]]
                    return make_both_data_into_preferred_rounding(combined_result, function, value, rounding)
    
            elif none_count == 2:
                """
                The queue is just totally empty.
                """
                return make_both_data_into_preferred_rounding(tree_result, function, value, rounding)
            
    @with_self   
    def request_state_by_monotonic_function_from_tree(self, our_leaf, function, value, rounding="Closest"):
        path = our_leaf.make_containing_path()
        result_in_nodes = path.request_node_by_monotonic_function(function, value, rounding)
        result = [(node.state if node is not None else None) for node in result_in_nodes]
        return result
    
    @with_self
    def request_state_by_monotonic_function_from_queue(self, function, value, rounding="Closest"):
        queue = self.cruncher.work_queue
        queue_size = queue.qsize()
        with queue.mutex:
            queue_as_list = list(queue.queue) # Probably inefficient, should access them one by one
        
        
        get = lambda number: function(queue_as_list[number])

        low = 0
        high = queue_size - 1

        low_value, high_value = get(low), get(high)
        
        if low_value >= value:
            if rounding == "Both":
                return [None, queue_as_list[low]]
            if rounding in ["High", "Closest"] or (low_value==value and rounding=="Exact"):
                return queue_as_list[low]
            else: # rounding == "Low" or (rounding == "Exact" and low_value!=value)
                return None
        if high_value <= value:
            if rounding == "Both":
                return [queue_as_list[high], None]
            if rounding in ["Low", "Closest"] or (low_value==value and rounding=="Exact"):
                return queue_as_list[high]
            else: # rounding == "High" or (rounding == "Exact" and low_value!=value)
                return None
            
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
        
        both = [queue_as_list[number] for number in (low, high)]
        
        return make_both_data_into_preferred_rounding(both, function, value, rounding)
    
    @with_self
    def __get_our_leaf(self):
        current_thread = threading.currentThread()    
        leaves_that_are_us = [leaf for (leaf, cruncher) in self.project.workers.items() if cruncher==current_thread]
        num = len(leaves_that_are_us)
        assert num <= 1
        if num == 1:
            our_leaf = leaves_that_are_us[0]
        else: # num == 0
            raise crunchers.ObsoleteCruncherError
        return our_leaf
    
    
    