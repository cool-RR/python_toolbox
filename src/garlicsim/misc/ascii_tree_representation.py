from garlicsim.data_structures import Tree, Node, Block


def show(tree):
    if len(tree.roots) > 1: raise NotImplementedError
    return _show(tree.roots[0])


def _show(thing):
    pass