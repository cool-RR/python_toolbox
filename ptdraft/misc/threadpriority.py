"""



import threading
import ctypes
import time

w32 = ctypes.windll.kernel32

THREAD_SET_INFORMATION = 0x20
THREAD_PRIORITY_ABOVE_NORMAL = 1

def set_priority(,priority):
    if not self.isAlive():
        print 'Unable to set priority of stopped thread'

    handle = w32.OpenThread(THREAD_SET_INFORMATION, False, self.tid)
    result = w32.SetThreadPriority(handle, priority)
    w32.CloseHandle(handle)
    if not result:
        print 'Failed to set priority of thread', w32.GetLastError()

class DummyThread(threading.Thread):

    def __init__(self, begin, name, iterations):
        threading.Thread.__init__(self)
        self.begin = begin
        self.tid = None
        self.iterations = iterations
        self.setName(name)

    def setPriority(self, priority):
        if not self.isAlive():
            print 'Unable to set priority of stopped thread'

        handle = w32.OpenThread(THREAD_SET_INFORMATION, False, self.tid)
        result = w32.SetThreadPriority(handle, priority)
        w32.CloseHandle(handle)
        if not result:
            print 'Failed to set priority of thread', w32.GetLastError()

    def run(self):
        self.tid = w32.GetCurrentThreadId()
        name = self.getName()
        self.begin.wait()
        while self.iterations:
            print name, 'running'
            start = time.time()
            while time.time() - start < 1:
                pass
            self.iterations -= 1



if __name__ == "__main__":
    start = threading.Event()

    normal = DummyThread(start, 'normal', 10)
    high = DummyThread(start, 'high', 10)

    normal.start()
    high.start()

    # XXX - This line adjusts priority - XXX
    high.setPriority(THREAD_PRIORITY_ABOVE_NORMAL)

    # Trigger thread execution
    start.set()
"""