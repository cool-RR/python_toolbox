
# maybe call it AddedNodes?

class NodesAdded(int):
    '''
    sync_crunchers functions return a NodesAdded object instead of an int.
    
    NodesAdded is jsut a subclass of int which has a nice __repr__ saying
    what the context of that number is.
    '''
    def __repr__(self):
        return '<' + int.__repr__(self) + ' nodes were added to the tree>'
    
    def __add__(self, other):
        # If it's being added to another NodesAdded, keep it as a NodesAdded
        # object.
        int_result = int.__add__(self, other)
        if isinstance(other, NodesAdded):
            return NodesAdded(int_result)
        else:
            return int_result
        
    __radd__ = __add__
    
    def __sub__(self, other):
        # If it's being substracted with another NodesAdded, keep it as a
        # NodesAdded object.
        int_result = int.__sub__(self, other)
        if isinstance(other, NodesAdded):
            return NodesAdded(int_result)
        else:
            return int_result
        
    __rsub__ = __sub__
            