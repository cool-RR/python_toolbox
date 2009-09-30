# Copyright 2009 Ram Rachum.
# This program is not licensed for distribution and may not be distributed.

"""
Does it matter whether we are using locks from threading or multiprocessing?
"""

import threading

class Niftylock(object):
    def __init__(self,lock=threading.Lock):
        self.lock=lock
        self.objects=dict()
        self.mylock=threading.RLock() #What if we want multiprocessing?

    def __getitem__(self,object):
        self.mylock.acquire()
        try:
            requested_lock=self.objects[id(object)]
        except KeyError:
            requested_lock=self.objects[id(object)]=self.lock()
        self.mylock.release()
        return requested_lock

    def __delitem__(self,object):
        del self.objects[id(object)]

    def acquire(self,object,blocking=1):
        self[object].acquire(blocking)

    def release(self,object):
        self[object].release()
        #Garbage collection? It's a stumper.













if __name__=="__main__":
    import random
    SIZE=1000

    l=[[0] for i in range(SIZE)]

    n=Niftylock()

    def doshit():
        global SIZE, l
        x=random.randint(0,SIZE-1)
        y=x
        while (x-y)%SIZE!=1:
            n.acquire(l[y])
            if l[y][0]==0:
                #time.sleep(0.1)
                l[y][0]+=1
                n.release(l[y]) #first
                return True
            else:
                n.release(l[y]) #second
                y=(y+1)%SIZE
        return "Done!"

    def gocrazy():
        while doshit()!="Done!":
            pass

    threads=[]
    for i in range(100):
        threads.append(threading.Thread(target=gocrazy))
        threads[-1].start()
    for i in range(100):
        threads[i].join()
    print(l)
