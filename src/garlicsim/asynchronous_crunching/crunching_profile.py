class CrunchingProfile(object):
    
    def __init__(self, clock_target=None,
                 step_options_profile=None):
  
        self.clock_target = clock_target
        self.step_options_profile = step_options_profile
  
    def state_satisfies(self, state):
        return state.clock >= self.clock_target
    
    def __repr__(self):
        
        stuff = []
        stuff.append("clock_target=%s" % self.clock_target)
        stuff.append("step_options_profile=%s" % self.step_options_profile)
        meow = ", ".join(stuff)
        return ("CrunchingProfile(%s)" % meow)