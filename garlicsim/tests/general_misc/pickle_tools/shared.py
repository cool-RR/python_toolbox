
class PickleableObject(object):
    _is_atomically_pickleable = True
    

class NonPickleableObject(object):
    _is_atomically_pickleable = False
    