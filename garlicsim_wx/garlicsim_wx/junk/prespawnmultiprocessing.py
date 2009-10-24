import multiprocessing

BUFFER = 3
'''
This is the minimum number of idle processes that should always be available.
'''

class Process(multiprocessing.Process):
    def start(self):

        multiprocessing.Process.start(self)

class xProcess(object):
    def __init__(self):
        pass

    def start(self):
        self.process = recruit_process()


def f():
    print("working...")
    for i in xrange(10**8):
        pass
    print("done.")

def main():
    Proc = Process #multiprocessing.Process # Process
    p = Proc(target = f)
    p.start()
    p.join()
    print("process joined")

if __name__=="__main__": main()