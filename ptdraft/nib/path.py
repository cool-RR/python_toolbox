from nibtree import *


class Path(object):
    """
    A path symbolizes a line of nibnodes in a nibtree.
    A nibtree may be a complex tree with many junctions,
    but a path is a direct line. Therefore, a path object contains
    information about which child to choose when going through
    a nibnode which has multiple children.

    Question: Assume you have a path defined, and now the
    nibtree is having some nibleaves added to it, making
    new decisions for the path necessary. what should the
    path do?
    should there be an automatic thing that will alert the path to it?
    maybe in the NibTree method for adding nibleaves?
    """
    def __init__(self,nibtree,start=None,decisions={}):
        #nibtree.path+=[self]
        self.nibtree=nibtree
        self.start=start
        self.decisions=decisions.copy()


    def __len__(self):
        j=self.start
        result=1
        while True:
            if self.decisions.has_key(j):
                j=self.decisions[j]
                result+=1
            elif len(kids=(j.naturalchildren+j.editedchildren))>0:
                if len(kids)>1:
                    warnings.warn("This path has come across a junction for which he has no information! Guessing.")
                j=kids[0]
                result+=1
            else:
                break
        return result

    def __getitem__(self,i):
        """
        for nibnode, gives next nibnode in path
        """

        if isinstance(i,int)==True:
            if i<0:
                i=len(self)+i

            j=self.start
            for j in range(i):
                if self.decisions.has_key(j):
                    j=self.decisions[j]
                else:
                    kids=(j.naturalchildren+j.editedchildren)
                    if len(kids)>0:
                        if len(kids)>1:
                            warnings.warn("This path has come across a junction for which iy has no information! Guessing.")
                            j=kids[0]
                #else
                raise IndexError
        elif isinstance(i,slice)==True:
            pass #todo
        elif isinstance(i,NibNode)==True:
            if self.decisions.has_key(i):
                return self.decisions[i]
            else:
                kids=(i.naturalchildren+i.editedchildren)
                if len(kids)>0:
                    if len(kids)>1:
                        warnings.warn("This path has come across a junction for which it has no information! Guessing.")
                    return kids[0]
            #else
            raise IndexError("Ran out of nibtree")
        else:
            return StandardError

    def cutofffirst(self):
        try:
            second=self[self.start]
        except IndexError:
            second=None
        return Path(self.nibtree,second,self.decisions)

    def getnibnodebytime(self,time):
        """
        Gets the nibnode in path which "occupies" the timepoint "time".
        This means that, if there is a nibnode which is after "time", it
        returns the nib immediately before it. Otherwise, returns None.
        """
        low=self.start
        if time<low.nib.clock:
            raise StandardError("You looked for a nibnode with a clock reading of "+str(time)+", while the earliest nibnode had a clock reading of "+str(self.start.nib.clock))
        """
        second=self[self.start]
        guessedrate=second.nib.time-self.start.nib.time

        try:
            new=round((time-self.start.nib.clock)/float(guessedrate))+2
            if
        except:
            high=self[-1]
        """
        while True:
            try:
                new=self[low]
                if new.nib.clock>time:
                    return low
                low=new
            except IndexError:
                return None




    def getrenderedsegments(self,starttime,endtime):
        """
        """
        segs=[]
        foogi=self.getnibnodebytime(starttime)
        if foogi==None:
            if starttime<self.start.nib.clock<endtime:
                myseg=[self.start.nib.clock,None]
            else:
                return []
        else:
            myseg=[foogi.nib.clock,None]

        current=self.start
        while True:
            try:
                new=self[current]
                if new.nib.clock>endtime:
                    myseg[1]=endtime
                    segs+=[myseg]
                    return segs
                current=new
            except IndexError:
                myseg[1]=new.nib.clock
                segs+=[myseg]
                return segs

    def leads_to_same_edge(self,path):
        """
        todo
        """
        return False






    """
    def __setitem__(self,i,value):
        pass
    """