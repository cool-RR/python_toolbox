

class CuteBaseTimer(object):
    __timers = [] # Change to weakref list
    
    def __init__(self, parent):
        self.__parent = parent
        CuteBaseTimer.__timers.append(self)
        
        
    @staticmethod # should be classmethod?
    def shut_off_timers_by_frame(frame):
        for timer in CuteBaseTimer.__timers:
            ancestor = timer.__parent
            while ancestor is not None:
                if ancestor == frame:
                    timer.Stop()
                    break
                ancestor = ancestor.GetParent()
    