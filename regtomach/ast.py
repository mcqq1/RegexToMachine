from anytree import RenderTree, AnyNode
from anytree.dotexport import RenderTreeGraph


class AbstractSyntaxTree:

    def __init__(self, head: AnyNode):
        self.head = head

    def __repr__(self):
        repr: str = ""
        for pre, _, node in RenderTree(self.head):
            repr += f"{pre}{node.name}\n"
        return repr

