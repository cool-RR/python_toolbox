'''
todo: if we're changing step options, it's still necessary to replace the
cruncher
'''

class CrunchingProfile(object):
    
    def __init__(self, clock_target=None,
                 step_options_profile=None):
  
        self.clock_target = clock_target
        self.step_options_profile = step_options_profile
  
    def state_satisfies(self, state):
        return state.clock >= self.clock_target
    
    def __eq__(self, other):
        return isinstance(other, CrunchingProfile) and \
               self.clock_target == other.clock_target and \
               self.step_options_profile == other.step_options_profile
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __repr__(self):
        
        stuff = []
        stuff.append("clock_target=%s" % self.clock_target)
        stuff.append("step_options_profile=%s" % self.step_options_profile)
        meow = ", ".join(stuff)
        return ("CrunchingProfile(%s)" % meow)