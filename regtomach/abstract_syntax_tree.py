from anytree import Node, RenderTree, DoubleStyle
from anytree.exporter import DotExporter
from loguru import logger


class AbstractSyntaxTree:

    def __init__(self, head: Node):
        self.head = head

    def __repr__(self):
        my_repr: str = ""
        for pre, fill, node in RenderTree(self.head, style=DoubleStyle):
            my_repr += "%s%s" % (pre, node.name) + "\n"
        return my_repr

    def save_to_png(self, filename: str = "tree.png"):
        try:
            DotExporter(
                self.head,
                nodeattrfunc=lambda node: "shape=box",
            ).to_picture(filename)

        except Exception as e:
            logger.error(
                "Failed to create png file with your syntax tree.",
                {str(e)},
            )


    def to_drf(self):
        pass
