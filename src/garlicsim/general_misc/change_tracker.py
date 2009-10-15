import weakref

class ChangeTracker(object):
    
    def __init__(self):
        self.library = weakref.WeakKeyDictionary()
        
    def check_in(self, thing):
        if self.library.has_key(thing) is False:
            self.library[thing] = hash(thing)
            return True
        
        # self.library.has_key(thing) is True
        
        previous_hash = self.library(thing)
        new_hash = hash(thing)
        if previous_hash == new_hash:
            return False
        else:
            self.library[thing] = new_hash
            return True
            