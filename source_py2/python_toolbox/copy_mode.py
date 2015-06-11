# Copyright 2009-2015 Ram Rachum.
# This program is distributed under the MIT license.


class CopyMode(dict):
    '''
    Passed as a memo to `deepcopy` to specify how objects should be copied.

    This type is meant to be subclassed. `__deepcopy__` methods may check which
    class the memo is to know what kind of deepcopying they should do.
    
    Typical usage:
    
        class NetworkStyleCopying(CopyMode): pass
            
        class Something(object):
            def __deepcopy__(self, memo):
                if isinstance(memo, NetworkStlyeCopying):
                    # Do network-style copying, whatever that means.
                else:
                    # Do normal copying.
                    
        s = Something()
        
        new_copy = copy.deepcopy(s, NetworkStyleCopying())
        # Now the new copy will be created using network style copying
    '''
    __repr__ = object.__repr__