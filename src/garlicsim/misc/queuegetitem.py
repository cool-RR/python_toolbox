import Queue

def queue_get_item(queue, i):
  with queue.mutex:
    return self.queue[i]
