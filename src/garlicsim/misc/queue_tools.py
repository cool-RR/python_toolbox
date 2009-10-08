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
    initial_size = queue.qsize()
    print("Queue has %s items initially." % initial_size)
    while True:
        try:
            thing = queue.get(block=False)
            result.append(thing)
        except Queue.Empty:
            current_size = queue.qsize()
            total_size = current_size + len(result)
            print("Dumping complete:")
            if current_size == initial_size:
                print("No items were added to the queue.")
            else:
                print("%s items were added to the queue." % \
                      (total_size - initial_size))
            print("Extracted %s items from the queue, queue has %s items left" \
                  % (len(result), current_size))
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