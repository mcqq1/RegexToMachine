from anytree import RenderTree, DoubleStyle
from anytree.exporter import DotExporter
from loguru import logger

from regtomach.nodes import ASTNode

class AbstractSyntaxTree:
    def __init__(self, head: ASTNode):
        self.head = head

    def __repr__(self):
        my_repr: str = ""
        for pre, fill, node in RenderTree(self.head, style=DoubleStyle):
            my_repr += "%s%s" % (pre, node) + "\n"
        return my_repr

    def save_to_png(self, filename: str = "tree.png"):
        try:
            DotExporter(
                self.head,
                nodeattrfunc=lambda node: "shape=box",
            ).to_picture(filename)

        except Exception as e:
            logger.error(
                f"Failed to create png file with your syntax tree. {str(e)}"
            )
