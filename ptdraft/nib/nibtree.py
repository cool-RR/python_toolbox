from nibtreeoverview import *

class NibNode(object):
    """
    A nibnode refers to a nib with the property ".nib".
    Nibnodes are used to order nibs in a nibtree.
    """
    def __init__(self,nib=None,parent=None):
        if nib==None:
            self.nib=Nib()
        else:
            self.nib=nib

        self.parent=parent

        self.children=[]
        """
        A list of:
        1. nibnodes whose nibs were produced by simulation
        2. nibnodes who were created by editing from the aforementioned set.
        """

        self.derived_nibnodes=[]
        """
        A list of nibnodes who were created by editing from this nibnode
        """

class NibTree(object):
    """
    A nibtree is a tree of nibnodes. Each nibnode corresponds to a nib.

    How does the nibtree work?
    There is a list of nibnodes. Each nibnode has the properties:
    ".parent", ".children" and ".dervied_nibnodes" within it,
    which refer to his relatives.

    Each node may have a parent, or may not, in which case he will also be called a root.

    maybe todo: make method fastaddnib (or fastaddnibnode)

    """
    def __init__(self,create_first_path=True):
        self.nibnodes=[] # A list for containing all the nibnodes in the tree.
        self.roots=[] # A list of roots. Root = node without parent
        self.paths=[] # A list of paths. See class Path for more info.
        """
        if createfirstpath==True:
            Path(self)
        """

    def new_natural_nib(self,parent):
        """
        Creates a new natural nib, wraps in nibnode and adds to nibtree.
        Returns the nibnode.
        """
        x=Nib(touched=False)
        return self.add_nib(x,parent)


    def new_touched_nib(self,template_nibnode=None):
        """
        Creates a new touched nib, wraps in nibnode and adds to nibtree.
        Returns the nibnode.

        todo: currently this method does not attempt to duplicate the template_nibnode.
        Maybe I'd like it to.
        """

        x=Nib(touched=False)
        if template_nibnode==None:
            parent=None
        else:
            parent=template_nibnode.parent


        return self.add_nib(x,parent,template_nibnode)


    def add_nib(self,mynib,parent=None,template_nibnode=None):
        """
        Wraps nib in nibnode and adds to tree.
        Returns the nibnode.
        """
        mynibnode=NibNode(mynib)
        self.add_nib_node(mynibnode,parent,template_nibnode)
        return mynibnode


    def add_nib_node(self,mynibnode,parent=None,template_nibnode=None):
        """
        Adds a nibnode to the tree.
        The nib inside the added nibnode may be a natural nib or a touched nib.
        If it's a natural nib it cannot have a template_nibnode.
        """
        mynib=mynibnode.nib
        if mynib.is_touched()==False and template_nibnode==None:
            raise StandardError("You tried adding an untouched nib to a tree while specifying a template_nibnode.")

        self.nibnodes=[mynibnode]
        if parent==None:
            self.roots+=[mynibnode]
            """
            if len(self.roots)==1:
                for path in self.paths:
                    path.start=mynibnode
            """

        else:
            mynibnode.parent=parent
            parent.children+=[mynibnode]
            if mynib.is_touched()==True:
                template_nibnode.derived_nibnodes+=[mynibnode]

            """
            # Update paths:
            kiddies=parent.editedchildren+parent.naturalchildren
            if len(kiddies)>0:
                for path in self.paths:
                    path.decisions[parent]=mynibnode
            """

    def nibnodecount(self):
        return len(self.nibnodelist)

    def get_movie(self,start,end):
        """
        gives list of nibnodes from start to end

        to deprecate?
        """
        line=[end]
        current=end
        while current!=start:
            current=current.parent
            line.insert(0,current)
        return line
