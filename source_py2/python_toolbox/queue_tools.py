# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.

'''Defines various functions for working with queues.'''


import Queue as queue_module
import sys

from python_toolbox import caching
from python_toolbox import import_tools


def is_multiprocessing_queue(queue):
    '''Return whether `queue` is a multiprocessing queue.'''
    return queue.__module__.startswith('multiprocessing')


def dump(queue):
    '''
    Empty all pending items in a queue and return them in a list.
    
    Use only when no other processes/threads are reading from the queue.
    '''
    return list(iterate(queue))


def iterate(queue, block=False, limit_to_original_size=False,
            _prefetch_if_no_qsize=False):
    '''
    Iterate over the items in the queue.
    
    `limit_to_original_size=True` will limit the number of the items fetched to
    the original number of items in the queue in the beginning.
    '''
    if limit_to_original_size:
        
        if is_multiprocessing_queue(queue) and \
           not _platform_supports_multiprocessing_qsize():
            
            if _prefetch_if_no_qsize:
                for item in dump(queue):
                    yield item
                return
            raise NotImplementedError(
                "This platform doesn't support `qsize` for `multiprocessing` "
                "queues, so you can't iterate on it while limiting to "
                "original queue size. What you can do is set "
                "`_prefetch_if_no_qsize=True` to have the entire queue "
                "prefetched before yielding the items."
            )
        for _ in xrange(queue.qsize()):
            try:
                yield queue.get(block=block)
            except queue_module.Empty:
                return
    else: # not limit_to_original_size
        while True:
            try:
                yield queue.get(block=block)
            except queue_module.Empty:
                return


def get_item(queue, i):
    '''
    Get an item from the queue by index number without removing any items.
    
    Note: This was designed for `Queue.Queue`. Don't try to use this, for
    example, on `multiprocessing.Queue`.
    '''
    with queue.mutex:
        return queue.queue[i]

    
def queue_as_list(queue):
    '''
    Get all the items in the queue as a `list` without removing them.
    
    Note: This was designed for `Queue.Queue`. Don't try to use this, for
    example, on `multiprocessing.Queue`.
    '''
    with queue.mutex:
        return list(queue.queue)


@caching.cache()
def _platform_supports_multiprocessing_qsize():
    '''
    Return whether this platform supports `multiprocessing.Queue().qsize()`.
    
    I'm looking at you, Mac OS.
    '''
    if 'multiprocessing' not in sys.modules:
        if not import_tools.exists('multiprocessing'):
            return False
    import multiprocessing
    multiprocessing_queue = multiprocessing.Queue()
    try:
        multiprocessing_queue.qsize()
    except NotImplementedError:
        return False
    else:
        return True