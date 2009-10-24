# Copyright 2009 Ram Rachum.
# This program is not licensed for distribution and may not be distributed.

class Cooldict(object):
    def __init__(self,dict=None):
        self.mylist=[]
        if dict!=None:
            for key in dict:
                self[key]=dict[key]

    def __getitem__(self,thing):
        for [key,value] in self.mylist:
            if key==thing:
                return value
        raise(KeyError)

    def __setitem__(self,thing,valuetowrite):
        for [key,value] in self.mylist:
            if key==thing:
                value=valuetowrite
                return
        self.mylist.append([thing,valuetowrite])

    def __repr__(self):
        thing=", ".join([str(key)+": "+str(value) for (key,value) in self.mylist])
        return("Cooldict("+thing+")")
