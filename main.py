# from my_compiler.parser import Parser
from my_compiler.visualize_tree import visualize_tree
# from my_compiler.create_drf import create_drf
# from my_compiler.nodes import RegexNode


# def main():
#     parser = Parser()

#     input_: str = input("Provide regex: ")
#     derivation_tree: list[RegexNode] = parser.parse(input_)
#     derivation_tree.visualize()

#     create_drf(derivation_tree)


if __name__ == "__main__":
    from my_compiler.tests import TEST_TREE

    visualize_tree(TEST_TREE)
