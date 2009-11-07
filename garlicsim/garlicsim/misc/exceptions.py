'''tododoc'''

class InvalidSimpack(Exception):
    '''
    An exception to raise when trying to load an invalid simpack.
    '''
    pass

class SimpackError(Exception):
    '''
    An exception to raise when a simpack behaves unexpectedly.
    '''
    pass
