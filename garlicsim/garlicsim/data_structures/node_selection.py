'''tododoc'''

from node import Node

class NodeRange(object):
    def __init__(self, first_node, last_node=None):
        path = last_node.make_containing_path()
        self.__node_list = list
        