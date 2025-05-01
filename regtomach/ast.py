from anytree import Node, RenderTree
from anytree.exporter import UniqueDotExporter

class AbstractSyntaxTree:

    def __init__(self, head: Node):
        self.head = head
    
    def __repr__(self):
        my_repr: str = ""
        for pre, fill, node in RenderTree(self.head):
            my_repr += "%s%s" % (pre, node.name) + "\n"
        return my_repr
    
    def save_to_png(self, filename: str = "tree.png"):
        UniqueDotExporter(self.head).to_picture(filename)
