from treelib import Tree, Node
from my_compiler.nodes import RegexNode


def visualize_tree(parsed_tree: list[RegexNode]):
    tree = Tree()

    tree.create_node("Regex")

    for node in parsed_tree:
        
        tree.create_node(node)
        
        

    tree.show()
