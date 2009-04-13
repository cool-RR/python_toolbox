from nib import *

class NaturalNibNodesBlock(object):
    pass

class NibTreeOverview(object):
    def __init__(self,nibtree):
        """
        I'm assuming that the NibTreeOverview gets created by a new NibTree
        """
        self.nibtree=nibtree

    def track(self,action):
