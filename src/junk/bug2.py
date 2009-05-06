import multiprocessing
import imp

class MyProcess(multiprocessing.Process):
    def __init__(self,thing):
        multiprocessing.Process.__init__(self)
        self.thing=thing
    def run(self):
        print 'running...', self.thing()


if __name__=="__main__":
    module=imp.load_source('life', 'tmp/life.py')
    thing=module.step
    print(thing)
    p=MyProcess(thing)
    p.start()
