
class Node(object):
    """
    A node encapsulates a state, using the property ".state"
    Nodes are used to order states in a tree.
    """
    def __init__(self,mystate=None,parent=None):
        if mystate==None:
            self.state=State()
        else:
            self.state=mystate

        self.parent=parent
        self.block=None

        self.children=[]
        """
        A list of:
        1. nodes whose nibs were produced by simulation.
        2. nodes who were created by editing from the aforementioned set.
        """

        self.derived_nodes=[]
        """
        A list of nodes who were created by editing from this node
        """

    def __len__(self):
        """
        Just returns 1 (useful because of Blocks)
        """
        return 1

    def soft_get_block(self):
        if self.block!=None:
            return self.block
        else:
            return self

class Block(object):
    """
    Who gets wrapped in a block? A succession of untouched nodes,
    which:
    1. Is at least 2 nodes in number
    2. All members, except the two last ones, must have no children except
       their successor in the block.
    3. The second to last node may have children who are touched nodes,
       in addition to the one untouched state, the last node, that is
       already its child
    4. The last node may have any kinds of children.

    Maybe:
    5. The parent of the first nibnode must be either touched or
       have additional children

    Not sure if wrapping in a block should be forced.

    """
    def __init__(self,nodelist):
        self.list=[]
        self.add(nodelist)

    def add(self,nodelist):
        if self.list!=[]:
            if nodelist[0].parent==self.list[-1]:
                self.list=self.list+nodelist
            elif self.nodelist[0].parent==nodelist[-1]:
                self.list=nodelist+self.list
            else:
                raise StandardError("List of nibnodes is not adjacent to existing nibnodes")
        else:
            self.list=nodelist[:]

        for i in range(len(nodelist)):
            if i>=1:
                if nodelist[i].parent!=nodelist[i-1]:
                    raise StandardError("Tried to add non-consecutive nibnodes to block")
            if nodelist[i].state.is_touched()==True:
                raise StandardError("Tried to add touched nibnodes to block")
            nodelist[i].block=self

    def split(self,node):
        """
        splits block, where "node" is the first node of the second block of the two
        """
        i=self.list.index(node)
        secondlist=self.list[i:]
        self.list=self.list[:i]
        if len(secondlist)>=2:
            Block(secondlist)
        else:
            for node in secondlist:
                node.block=None
        if len(self.list)<=2:
            self.delete()


    def delete(self):
        """
        deletes the block, leaving all nibnodes without a block
        """
        for node in self:
            node.block=None
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


class Tree(object):
    """
    A tree is a tree of nodes. Each node encapsulates a state.

    How does the tree work?
    There is a list of nodes. Each node has the properties:
    ".parent", ".children" and ".dervied_nodes" within it,
    which refer to his relatives.

    Each node may have a parent, or may not, in which case it will also be called a root.

    maybe todo: make method fastaddstate (or fastaddnode)

    """
    def __init__(self,create_first_path=True):
        self.nodes=[] # A list for containing all the nodes in the tree.
        self.roots=[] # A list of roots. Root = node without parent
        self.paths=[] # A list of paths. See class Path for more info.
        """
        if createfirstpath==True:
            Path(self)
        """

    def new_natural_state(self,parent):
        """
        Creates a new natural nib, wraps in nibnode and adds to nibtree.
        Returns the nibnode.
        """
        x=State(touched=False)
        return self.add_state(x,parent)


    def new_touched_state(self,template_node=None):
        """
        Creates a new touched state, wraps in node and adds to tree.
        Returns the node.

        todo: currently this method does not attempt to duplicate the template_node.
        Maybe I'd like it to.
        """

        x=State(touched=False)
        if template_node==None:
            parent=None
        else:
            parent=template_node.parent


        return self.add_state(x,parent,template_node)


    def add_state(self,mystate,parent=None,template_node=None):
        """
        Wraps state in node and adds to tree.
        Returns the node.
        """
        mynode=Node(mystate)
        self.add_node(mynode,parent,template_node)
        return mynode


    def add_node(self,mynode,parent=None,template_node=None):
        """
        Adds a node to the tree.
        The state inside the added node may be a natural state or a touched state.
        If it's a natural nib it cannot have a template_nibnode.
        """

        mystate=mynode.state
        if mystate.is_touched()==False and template_node!=None:
            raise StandardError("You tried adding an untouched state to a tree while specifying a template_node.")

        try:
            if parent!=template_node.parent:
                raise StandardError("parent you specified and parent of template_node aren't the same!") # todo: Do something about this shit
        except AttributeError:
            pass

        self.nodes+=[mynode]
        if parent==None:
            self.roots+=[mynode]
            if mystate.is_touched()==True:
                if template_node!=None:
                    template_node.derived_nodes+=[mynode]

            """
            if len(self.roots)==1:
                for path in self.paths:
                    path.start=mynibnode
            """

        else:
            mynode.parent=parent
            parent.children+=[mynode]

            if mystate.is_touched()==True:
                if template_node!=None:
                    template_node.derived_nibnodes+=[mynibnode]
                if parent.block!=None:
                    if len(parent.block)-parent.block.list.index[parent]>=3:
                        parent.block.split(parent)
            else:
                if parent.block!=None:
                    ind=parent.block.list.index(parent)
                    number=len(parent.block)-ind
                    if number==1:
                        parent.block.add([mynode])
                    else:
                        parent.block.split(parent.block.list.index[i+1])

                else:
                    if len(parent.children)==1 and parent.state.is_touched()==False:
                        Block([parent,mynode])

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




    def nodecount(self):
        return len(self.nodes)

    def get_movie(self,start,end):
        """
        gives list of nodes from start to end

        to deprecate?
        """
        line=[end]
        current=end
        while current!=start:
            current=current.parent
            line.insert(0,current)
        return line
