"""
TODO:
maybe nibs and nibleafs are redundant? maybe merge them?
"""



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

    """
    def __init__(self):
        self.nibleaflist=[] # A list for containing all the nibleafs in the tree.
        self.roots=[] # A list of roots. Root = leaf without parent

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
        else:
            mynibleaf.parent=parent
            if mynib.istouched()==True:
                parent.editedchildren+=[mynibleaf]
            else:
                parent.naturalchildren+=[mynibleaf]

    def nibleafcount(self):
        return len(self.nibleaflist)

    def getmovie(self,start,end):
        """
        gives list of nibleaves
        """
        line=[end]
        current=end
        while current!=start:
            current=current.parent
            line.insert(0,current)
        return line


