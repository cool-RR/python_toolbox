import multiprocessing
import Queue


def dump_queue(queue):
    result=[]

    while True:
        try:
            thing=queue.get(block=False)
            result.append(thing)
        except Queue.Empty:
            return result

