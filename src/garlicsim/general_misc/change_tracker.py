import weakref


class ChangeTracker(object): 
    '''
    '''
    # Todo: Someone suggested that it's possible the hash won't change even
    # when the object changes, which might break my program. If so, we can 
    # use pickle.
    
    def __init__(self):
        self.library = weakref.WeakKeyDictionary()
        
    def check_in(self, thing):
        if thing not in self.library:
            self.library[thing] = hash(thing)
            return True
        
        # thing in self.library
        
        previous_hash = self.library[thing]
        new_hash = hash(thing)
        if previous_hash == new_hash:
            return False
        else:
            self.library[thing] = new_hash
            return True
    
    def __contains__(self, thing):
        return self.library.__contains__(thing)