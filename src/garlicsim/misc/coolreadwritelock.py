from readwritelock import ReadWriteLock

class ContextManager(object):
    def __init__(self, lock, acquire_func):
        self.lock = lock
        self.acquire_func = acquire_func
    def __enter__(*args, **kwargs):
        self.acquire_func()
    def __exit__(*args, **kwargs):
        self.lock.release()

class CoolReadWriteLock(ReadWriteLock):
    def __init__(self, *args, **kwargs):
        ReadWriteLock.__init__(self, *args, **kwargs)
        self.read = ContextManager(self, self.acquireRead)
        self.write = ContextManager(self, self.acquireWrite)
        
        