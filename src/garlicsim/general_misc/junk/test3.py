import time
import sys
import multiprocessing

# import logging
# logger = multiprocessing.log_to_stderr()
# logger.setLevel(logging.DEBUG)


STOPPED = 'STOP'

def dump_queue(queue):
    result = []
    
    for thing in iter(queue.get, STOPPED):
        if not isinstance(thing, list):
            print 'we got something we should not have: %s' % thing
        result.append(thing)
    return result



class Process(multiprocessing.Process):
    def __init__(self, x):
        multiprocessing.Process.__init__(self)
        self.q = multiprocessing.Queue()
        self.event = x
    def run(self):
        for i in range(100):
            self.q.put([range(20) for j in range(10)])
        self.q.put(STOPPED)
        self.event.set()


if __name__ == '__main__':
    x = multiprocessing.Event()
    p = Process(x)
    p.start()
    x.wait()
    l = dump_queue(p.q)
    print len(l)
    p.join()