import time
import sys
import multiprocessing

class Stopper(object):
    pass

def dump_queue(queue):
    """
    Empties all pending items in a queue and returns them in a list.
    
    Use only when no other processes/threads are reading from the queue.
    """
    result = []

    # START DEBUG CODE
    initial_size = queue.qsize()
    print("Queue has %s items initially." % initial_size)
    #  END  DEBUG CODE

    queue.put(Stopper)
    #queue.put(SecondStopper)
    
    for thing in iter(queue.get, Stopper): # todo sentinel=
        result.append(thing)
    
    # START DEBUG CODE
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
    #  END  DEBUG CODE
            
    return result



class Process(multiprocessing.Process):
    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.q = multiprocessing.Queue()
    def run(self):
        for i in range(100):
            self.q.put([range(20) for j in range(10)])
            sys.stdout.write('Put item %s.\n' % i)
            sys.stdout.flush()



if __name__ == '__main__':
    p = Process()
    p.start()
    # p.join()
    time.sleep(1)
    l = dump_queue(p.q)
