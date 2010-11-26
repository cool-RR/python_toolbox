
class PickleableObject(object):
    is_atomically_pickleable = True
    

class NonPickleableObject(object):
    is_atomically_pickleable = False
    