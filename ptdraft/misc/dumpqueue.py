import multiprocessing
import Queue


def dump_queue(queue):
    result=[]
    while True:
        try:
            result.append(queue.get(block=False))
        except Queue.Empty:
            return result
