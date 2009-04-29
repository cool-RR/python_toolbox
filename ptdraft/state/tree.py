
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
    2. All members, except the last one, must have no children except
       their successor in the block.
    3. The last node may have any kinds of children.

    """
    def __init__(self,node_list):
        self.list=[]
        self.add(node_list)

    def add(self,node_list):
        if self.list!=[]:
            if node_list[0].parent==self.list[-1]:
                self.list=self.list+node_list
            elif self.node_list[0].parent==node_list[-1]:
                self.list=node_list+self.list
            else:
                raise StandardError("List of nodes is not adjacent to existing nodes")
        else:
            self.list=node_list[:]

        for i in range(len(node_list)):
            if i>=1:
                if node_list[i].parent!=node_list[i-1]:
                    raise StandardError("Tried to add non-consecutive nodes to block")
            if node_list[i].state.is_touched()==True:
                raise StandardError("Tried to add touched nodes to block")
            node_list[i].block=self

    def split(self,node):
        """
        splits block, where "node" is the first node of the second block of the two
        """
        i=self.list.index(node)
        second_list=self.list[i:]
        self.list=self.list[:i]
        if len(second_list)>=2:
            Block(second_list)
        else:
            for node in second_list:
                node.block=None
        if len(self.list)<=2:
            self.delete()


    def delete(self):
        """
        deletes the block, leaving all nibnodes without a block
        """
        for node in self:
            node.block=None

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
    def __init__(self):
        self.nodes=[] # A list for containing all the nodes in the tree.
        self.roots=[] # A list of roots. Root = node without parent
        #self.paths=[] # A list of paths. See class Path for more info.


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
                    template_node.derived_nodes.append(mynode)

        else:
            mynode.parent=parent
            parent.children.append(mynode)

            if mystate.is_touched()==True:
                if template_node!=None:
                    template_node.derived_nibnodes.append(mynibnode)
                if parent.block!=None:
                    if parent!=parent.block.list[-1]:
                        parent.block.split(parent.children[0])
            else:
                if parent.block!=None:
                    ind=parent.block.list.index(parent)
                    number=len(parent.block)-ind
                    if number==1:
                        if len(parent.children)==1:
                            parent.block.add([mynode])
                    else:
                        parent.block.split(parent.block.list[ind+1])

                else:
                    if len(parent.children)==1 and parent.state.is_touched()==False:
                        Block([parent,mynode])






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
