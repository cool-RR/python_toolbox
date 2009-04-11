"""
TODO:
maybe nibs and nibleafs are redundant? maybe merge them?
---
maybe it's silly that a parentless nibleaf must be touched?
---
create mechanism for "stitching" nibleaves (making one a child
of the other artificially)
--
What to do with paths???
--
"""

import warnings


class Nib(object):
    """
    A nib is something like a time-point. It's something like a frozen state of the simulation.

    Most nibs are not touched, but some nibs are touched.
    A touched nib is a special kind of nib.
    Right now I set a distinct class for it, but I'm not %100 sure this is the right thing to do.
    A touched nib is a nib that was not formed naturally by a simulation step:
    It was created by the user, either from scratch or based on an untouched nib.
    """
    def __init__(self,touched=False):
        self.__touched=touched
    def istouched(self):
        return self.__touched
    def maketouched(self):
        self.__touched=True
    def makenutouched(self):
        self.__touched=False



class NibLeaf(object):
    """
    A nibleaf refers to a nib with the property ".nib".
    Nibleaves are used to order nibs in a nibtree.
    """
    def __init__(self,mynib):
        self.nib=mynib
        self.parent=None # A nibleaf may be filled in here for a parent
        self.naturalchildren=[] # A list of nibleaves whose nibs were produced by natural simulation
        self.editedchildren=[] # A list of nibleaves whose nibs were produced by manual editing, probably by user

class NibTree(object):
    """
    A nibtree is a tree of nibleaves. Each nibleaf corresponds to a nib.

    How does the nibtree work?
    There is a list of nibleaves. Each nibleaf has the properties:
    ".parent", ".naturalchildren" and ".editedchildren" within it,
    which refer to his relatives.

    Each leaf may have a parent, or may not, in which case he will also be called a root.
    When a leaf has a parent, it means that for the parent,
    this nib is either a natural child, or an edited child.

    If leaf2 is a natural child of leaf1, it means that
    leaf2 was created by simulation from leaf1.
    It means that leaf2 has a "clock reading" more advanced than leaf1.
    It also means that leaf2 is an untouched nib.

    If leaf2 is an edited child of leaf1k, it means that
    leaf2 was created by editing leaf1. leaf2 is leaf1 tinkered with.
    Therefore leaf1 and leaf2 will have the same "clock reading".
    It also means that leaf1 is a touched nib.

    maybe todo: make method fastaddnib (or fastaddnibleaf)

    """
    def __init__(self,createfirstpath=True):
        self.nibleaflist=[] # A list for containing all the nibleafs in the tree.
        self.roots=[] # A list of roots. Root = leaf without parent
        self.paths=[] # A list of paths. See class Path for more info.
        """
        if createfirstpath==True:
            Path(self)
        """

    def newnib(self,parent=None,touched=False):
        """
        Creates a new nib, wraps in nibleaf and adds to nibtree.
        Returns the nibleaf.
        """
        if parent==None and touched==False:
            raise StandardError("You are creating a nib without specifying a parent: If that's indeed what you want, the nib must be touched, so please specify touched=True when calling newnib.")
        x=Nib(touched)
        return self.addnib(x,parent)

    def addnib(self,mynib,parent=None):
        """
        Wraps nib in nibleaf and adds to tree.
        Returns the nibleaf.
        """
        mynibleaf=NibLeaf(mynib)
        self.addnibleaf(mynibleaf,parent)
        return mynibleaf

    def addnibleaf(self,mynibleaf,parent=None):
        """
        Adds a nibleaf to the tree.
        The nib inside the added nibleaf may be a natural nib or a touched nib.
        If it's a natural nib it must have a parent.
        If it's a touched nib, it may not have a parent, but if it does have a parent,
        the parent must have the same "clock reading" as the touched nib.
        """
        if parent!=None and isinstance(parent,NibLeaf)==False:
            raise StandardError("Parent must be a nibleaf!")
        mynib=mynibleaf.nib
        if mynib.istouched()==False and parent==None:
            raise StandardError("You tried adding an untouched nib to a tree without specifying a parent nib")
        # todo: check that if nib is touched clock reading is the same



        self.nibleaflist+=[mynibleaf]
        if parent==None:
            self.roots+=[mynibleaf]
            """
            if len(self.roots)==1:
                for path in self.paths:
                    path.start=mynibleaf
            """

        else:
            mynibleaf.parent=parent

            """
            # Update paths:
            kiddies=parent.editedchildren+parent.naturalchildren
            if len(kiddies)>0:
                for path in self.paths:
                    path.decisions[parent]=mynibleaf
            """
            # Add the new nib to the appropriate children-list
            if mynib.istouched()==True:
                parent.editedchildren+=[mynibleaf]
            else:
                parent.naturalchildren+=[mynibleaf]

    def nibleafcount(self):
        return len(self.nibleaflist)

    def getmovie(self,start,end):
        """
        gives list of nibleaves from start to end
        """
        line=[end]
        current=end
        while current!=start:
            current=current.parent
            line.insert(0,current)
        return line

class Path(object):
    """
    A path symbolizes a line of nibleafs in a nibtree.
    A nibtree may be a complex tree with many junctions,
    but a path is a direct line. Therefore, a path object contains
    information about which child to choose when going through
    a nibleaf which has multiple children.

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
        for nibleaf, gives next nibleaf in path
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
        elif isinstance(i,NibLeaf)==True:
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

    def getnibleafbytime(self,time):
        """
        Gets the nibleaf in path which "occupies" the timepoint "time".
        This means that, if there is a nibleaf which is after "time", it
        returns the nib immediately before it. Otherwise, returns None.
        """
        low=self.start
        if time<low.nib.clock:
            raise StandardError("You looked for a nibleaf with a clock reading of "+str(time)+", while the earliest nibleaf had a clock reading of "+str(self.start.nib.clock))
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
        foogi=self.getnibleafbytime(starttime)
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







    """
    def __setitem__(self,i,value):
        pass
    """