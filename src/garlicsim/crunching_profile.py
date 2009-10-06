class CrunchingProfile(object):
    
    def __init__(self, nodes_distance=0, clock_distance=0,
                 step_options_profile=None):
  
        self.nodes_distance = nodes_distance
        self.clock_distance = clock_distance
        self.step_options_profile = step_options_profile
        
    def is_done(self):
        return (self.nodes_distance <= 0) and \
               (self.clock_distance <= 0)
        
    def __repr__(self):
        
        stuff = []
        stuff.append("nodes_distance=%s" % self.nodes_distance)
        stuff.append("clock_distance=%s" % self.clock_distance)
        stuff.append("step_options_profile=%s" % self.step_options_profile)
        meow = ", ".join(stuff)
        return ("CrunchingProfile(%s)" % meow)