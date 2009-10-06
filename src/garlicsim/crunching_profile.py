
class CrunchingProfile(object):
    
    def __init__(nodes=None, clock=None, step_options_profile=None):
        
        assert nodes or clock
        
        self.nodes = nodes
        self.clock = clock
        self.step_options_profile = step_options_profile
        
    def __repr__(self):
        
        stuff = []
        stuff.append("nodes=%" % self.nodes)
        stuff.append("clock=%" % self.clock)
        stuff.append("step_options_profile=%" % self.step_options_profile)
        meow = ", ".join(stuff)
        return ("CrunchingProfile(%s)" % meow)