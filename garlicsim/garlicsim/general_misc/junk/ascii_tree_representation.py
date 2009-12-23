# Copyright 2009-2010 Ram Rachum.
# This program is distributed under the LGPL2.1 license.

from garlicsim.data_structures import Tree, Node, Block

#todo

def show(tree):
    if len(tree.roots) > 1: raise NotImplementedError
    return _show(tree.roots[0])


def _show(thing):
    pass