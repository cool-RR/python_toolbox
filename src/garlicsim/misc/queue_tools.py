# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

"""
This module defines several functions that might be useful
when working with queues.
"""

import Queue


def dump_queue(queue):
    """
    Empties all pending items in a queue
    and returns them in a list.
    """
    result = []

    while True:
        try:
            thing = queue.get(block=False)
            result.append(thing)
        except Queue.Empty:
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