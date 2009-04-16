
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
        self.block=None

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

    def __len__(self):
        """
        Just returns 1 (useful because of N3Blocks)
        """
        return 1

    def soft_get_block(self):
        if self.block!=None:
            return self.block
        else:
            return self

class NaturalNibNodesBlock(object):
    """
    Who gets wrapped in a block? A succession of untouched nibnodes,
    which:
    1. Is at least 2 nibnodes in number
    2. All members, except the two last ones, must have no children except
       their successor in the block.
    3. The second to last node may have children who are touched nibnodes,
       in addition to the one untouched nib, the last nibnode, that is
       already its child
    4. The last nibnode may have any kinds of children.
    5. The parent of the first nibnode must be either touched or
       have additional children

    """
    def __init__(self,nibnodelist):
        self.list=[]
        self.add(nibnodelist)

    def add(self,list):
        if self.list!=[]:
            if list[0].parent==self.list[-1]:
                self.list=self.list+list
            elif self.list[0].parent==list[-1]:
                self.list=list+self.list
            else:
                raise StandardError("List of nibnodes is not adjacent to existing nibnodes")
        else:
            self.list=list[:]

        for i in range(len(list)):
            if i>=1:
                if list[i].parent!=list[i-1]:
                    raise StandardError("Tried to add non-consecutive nibnodes to block")
            if list[i].nib.is_touched()==True:
                raise StandardError("Tried to add touched nibnodes to block")
            list[i].block=self

    def split(self,nibnode):
        """
        splits block, where nibnode is the first node of the second block
        """
        i=self.list.index(nibnode)
        secondlist=self.list[i:]
        self.list=self.list[:i]
        if len(secondlist)>=2:
            NaturalNibNodesBlock(secondlist)
        else:
            for nibnode in secondlist:
                nibnode.block=None
        if len(self.list)<=2:
            self.delete()


    def delete(self):
        """
        deletes the block, leaving all nibnodes without a block
        """
        for nibnode in self:
            nibnode.block=None
        del self

    def __delitem__(self,item):
        if item==0 or item==-1 or item==len(self)-1: #check if it's an edge item
            self.list[item].block=None
            return self.list.__delitem__(item)
        else:
            return StandardError("Can't remove a nibnode from the middle of a block")

    def __contains__(self,item):
        return self.list.__contains__(item)

    def __iter__(self):
        return self.list.__iter__()

    def __len__(self):
        return len(self.list)

    def __getitem__(self,i):
        return self.list[i]
    pass

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
        if mynib.is_touched()==False and template_nibnode!=None:
            raise StandardError("You tried adding an untouched nib to a tree while specifying a template_nibnode.")

        try:
            if parent!=template_nibnode.parent:
                raise StandardError("parent you specified and parent of template_nibnode aren't the same!") # todo: Do something about this shit
        except AttributeError:
            pass

        self.nibnodes+=[mynibnode]
        if parent==None:
            self.roots+=[mynibnode]
            if mynib.is_touched()==True:
                if template_nibnode!=None:
                    template_nibnode.derived_nibnodes+=[mynibnode]

            """
            if len(self.roots)==1:
                for path in self.paths:
                    path.start=mynibnode
            """

        else:
            mynibnode.parent=parent
            parent.children+=[mynibnode]

            if mynib.is_touched()==True:
                if template_nibnode!=None:
                    template_nibnode.derived_nibnodes+=[mynibnode]
                if parent.block!=None:
                    if len(parent.block)-parent.block.list.index[parent]>=3:
                        parent.block.split(parent)
            else:
                if parent.block!=None:
                    ind=parent.block.list.index(parent)
                    number=len(parent.block)-ind
                    if number==1:
                        parent.block.add([mynibnode])
                    else:
                        parent.block.split(parent.block.list.index[i+1])

                else:
                    if len(parent.children)==1 and parent.nib.is_touched()==False:
                        NaturalNibNodesBlock([parent,mynibnode])

                """
                if parent.nib.is_touched()==True:
                    NaturalNibNodesBlock([mynibnode])
                else:
                    parent.block.add([mynibnode])
                """

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
