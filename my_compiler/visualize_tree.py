from my_compiler.nodes import RegexNode


def visualize_tree(tree: list[RegexNode]):
    for node in tree:
        print(node)
