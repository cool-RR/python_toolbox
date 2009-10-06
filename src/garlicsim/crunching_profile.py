
class CrunchingProfile(object):
    
    def __init__(self, nodes_distance=None, clock_distance=None,
                 step_options_profile=None):
  
        self.nodes_distance = nodes_distance
        self.clock_distance = clock_distance
        self.step_options_profile = step_options_profile
        
    def __repr__(self):
        
        stuff = []
        stuff.append("nodes_distance=%" % self.nodes_distance)
        stuff.append("clock_distance=%" % self.clock_distance)
        stuff.append("step_options_profile=%" % self.step_options_profile)
        meow = ", ".join(stuff)
        return ("CrunchingProfile(%s)" % meow)