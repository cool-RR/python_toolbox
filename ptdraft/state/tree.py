
class Node(object):
    """
    A node encapsulates a State with the attribute ".state"
    Nodes are used to order states in a tree.
    """
    def __init__(self,mystate=None,parent=None):
        if mystate==None:
            self.state=State()
        else:
            self.state=mystate

        self.parent=parent


        self.block=None
        """
        A node may be a member of a Block. See class Block
        for more details.
        """

        self.children=[]
        """
        A list of:
        1. Nodes whose states were produced by simulation from this node.
        2. Nodes who were "created by editing" from one of
           the nodes in the aforementioned set.
        """

        self.derived_nodes=[]
        """
        A list of nodes who were created by editing from this node.
        These nodes should have the same parent as this node.
        """

    def __len__(self):
        """
        Just returns 1 (useful because of Blocks)
        """
        return 1

    def soft_get_block(self):
        """
        If this node is a member of a Block, returns the Block.
        Otherwise, returns the node itself.
        """
        if self.block!=None:
            return self.block
        else:
            return self

class Block(object):
    """
    A Block is a device for bundling together a succession of natural
    nodes. It makes the tree more organized and easy to browse,
    and improves performance.

    When you're doing a simulation, often you'll have a succession of 1000+
    natural nodes, which were created "organically", each from its parent,
    by simulation. There is no point in displaying a 1000 nodes in the
    tree browser: Therefore they are grouped together into a Block.

    Who qualifies to get wrapped in a block? A succession of untouched nodes,
    which:
    1. Is at least 2 nodes in number
    2. All members, except the last one, must have no children except
       their successor in the block.
    3. The last node may have any kinds of children.

    If you want to check whether a certain node is in a block or not,
    check its ".block" attribute.

    """
    def __init__(self,node_list):

        self.list=[]

        self.add(node_list)

    def add(self,node_list):
        """
        Adds a list of nodes to the Block.
        These nodes must already be successive.
        They must come right before the block or right after it. (Unless
        the block is empty)
        """
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
        Splits block, where "node" is the first node of
        the second block of the two.
        If either of the new blocks is too small to be a block,
        it gets deleted, and its nodes will be block-less.
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
        Deletes the block, leaving all nodes without a block.
        """
        for node in self:
            node.block=None

    def __delitem__(self,item):
        """
        Removes a node from the Block. Can only remove
        an edge node.
        """
        if item==0 or item==-1 or item==len(self)-1: #check if it's an edge item
            self.list[item].block=None
            return self.list.__delitem__(item)
        else:
            return StandardError("Can't remove a node from the middle of a block")

    def __contains__(self,node):
        """
        Returns whether the block contains "node"
        """
        return self.list.__contains__(node)

    def __iter__(self):
        return self.list.__iter__()

    def __len__(self):
        """
        Returns the number of nodes in the block.
        """
        return len(self.list)

    def __getitem__(self,i):
        return self.list[i]


class Tree(object):
    """
    A tree of nodes. Each node encapsulates a state.

    A tree is used within a Project to organize everything that
    is happenning in the simulation. Typically, when doing a simulation,
    this tree will be a "degenerate" tree, i.e. a straight, long
    succession of nodes with no more than one child each.
    However, trees are useful, because they give you the ability
    to "split" or "fork" the simulation at any node you wish,
    allowing you to explore and analyze different "scenarios"
    in parallel in the same simulation.


    How does the tree work?
    There is a list of nodes. Each node has the properties:
    ".parent", ".children" and ".dervied_nodes" within it,
    which refer to its relatives.

    Each node may have a parent, or may not, in which case it will also be called a root.

    maybe todo: make method fastaddstate (or fastaddnode)

    """
    def __init__(self):
        self.nodes=[] # A list for containing all the nodes in the tree.
        self.roots=[] # A list of roots. Root = node without parent.


    def new_natural_state(self,parent):
        """
        Creates a new natural state, wraps in node and adds to tree.
        Returns the node.
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
        Returns the node.
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
        return mynode





    def node_count(self):
        return len(self.nodes)

"""
    Junk:

    def get_movie(self,start,end):
        \"""
        gives list of nodes from start to end

        \"""
        line=[end]
        current=end
        while current!=start:
            current=current.parent
            line.insert(0,current)
        return line
"""