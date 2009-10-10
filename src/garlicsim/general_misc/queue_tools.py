# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
This module defines several functions that might be useful
when working with queues.
"""
from __future__ import with_statement

import Queue


def dump_queue(queue):
    """
    Empties all pending items in a queue and returns them in a list.
    
    Use only when no other processes/threads are reading from the queue.
    """
    result = []


    #queue.put(SecondStopper)
    
    try:
        thing = queue.get(block = False)
        result.append(thing)
    except Queue.Empty:
        pass
        
    
    #result = result[:-1]
    
            
    return result


def queue_get_item(queue, i):
    """
    Retrieves an item from a queue according to the specified index.
    Note: This was designed for Queue.Queue. Don't try to use this, for
    example, on multiprocessing.Queue.
    """
    with queue.mutex:
        return queue.queue[i]

def queue_as_list(queue):
    """
    Returns a list that contains all the items in the queue in order.
    This is without emptying the queue.
    Note: This was designed for Queue.Queue. Don't try to use this, for
    example, on multiprocessing.Queue.
    """
    with queue.mutex:
        return list(queue.queue)