import weakref

class SleekRef(object):
    def __init__(self, thing, callback=None):
        self.callback = callback
        if callback and not callable(callback):
            raise Exception('%s is not a callable object.' % callback)
        try:
            self.ref = weakref.ref(self, thing, callback)
        except TypeError:
            self.ref = None
            self.thing = thing
        else:
            self.thing = None
            
    def __call__(self):
        return self.ref() if self.ref else self.thing
        