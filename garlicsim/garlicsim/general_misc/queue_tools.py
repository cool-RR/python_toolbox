# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines several functions that may be useful when working with queues.'''

from __future__ import with_statement

import Queue

def dump(queue):
    '''
    Empty all pending items in a queue and return them in a list.
    
    Use only when no other processes/threads are reading from the queue.
    '''
    return list(iterate(queue))


def iterate(queue, block=False):
    '''Iterate over the items in the queue.'''
    
    while True:
        try:
            yield queue.get(block=block)
        except Queue.Empty:
            raise StopIteration


def get_item(queue, i):
    '''
    Get an item from the queue by index number without removing any items.
    
    Note: This was designed for Queue.Queue. Don't try to use this, for
    example, on multiprocessing.Queue.
    '''
    with queue.mutex:
        return queue.queue[i]

def queue_as_list(queue):
    '''
    Get all the items in the queue as a list without removing them.
    
    Note: This was designed for Queue.Queue. Don't try to use this, for
    example, on multiprocessing.Queue.
    '''
    with queue.mutex:
        return list(queue.queue)