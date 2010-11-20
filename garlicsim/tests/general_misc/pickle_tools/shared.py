
class PicklableObject(object):
    is_atomically_pickleable = True
    

class UnpicklableObject(object):
    is_atomically_pickleable = False
    