# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''Defines several functions that may be useful when working with queues.'''

from __future__ import with_statement

import Queue


class _Sentinel(object):
    pass


def dump(queue):
    '''
    Empty all pending items in a queue and return them in a list.
    
    Use only when no other processes/threads are reading from the queue.
    '''
    return list(iterate(queue))


def iterate(queue, block=False, limit_to_original_size=False):
    '''
    Iterate over the items in the queue.
    
    `limit_to_original_size` uses a sentinel, which can be a problem for queues
    with a finite size which may get full, or if other code is `get`ting items
    from the queue while we iterate.    
    '''
    if limit_to_original_size:
        queue.put(_Sentinel)
    while True:
        try:
            thing = queue.get(block=block)
            if thing is _Sentinel:
                assert limit_to_original_size
                raise StopIteration
            yield thing
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