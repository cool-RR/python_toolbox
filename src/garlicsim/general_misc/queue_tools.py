# Copyright 2009 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

'''
This module defines several functions that might be useful when working with
queues.
'''

import Queue

def dump(queue):
    '''
    Empties all pending items in a queue and returns them in a list.
    
    Use only when no other processes/threads are reading from the queue.
    '''
    result = []

    # START DEBUG CODE
    #initial_size = queue.qsize()
    #print("Queue has %s items initially." % initial_size)
    #  END  DEBUG CODE

    #queue.put(Stopper)
    #queue.put(SecondStopper)
    
    try:
        while True:
            thing = queue.get(block=False)
            result.append(thing)
    except Queue.Empty:
        pass
    
    #for thing in iter(queue.get, Stopper): # todo sentinel=
    #    result.append(thing)
    
    #result = result[:-1]
    
    # START DEBUG CODE
    #current_size = queue.qsize()
    #total_size = current_size + len(result)
    #print("Dumping complete:")
    #if current_size == initial_size:
        #print("No items were added to the queue.")
    #else:
        #print("%s items were added to the queue." % \
              #(total_size - initial_size))
    #print("Extracted %s items from the queue, queue has %s items left" \
    #% (len(result), current_size))
    #  END  DEBUG CODE
            
    return result


def queue_get_item(queue, i):
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