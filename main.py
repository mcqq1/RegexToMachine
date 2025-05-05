from regtomach.parser import Parser
from regtomach.nfa import NFA


if __name__ == "__main__":
    regex: str = input("Provide a regex: ")
    parser = Parser(regex)
    ast = parser.to_abstract_syntax_tree()

    print(ast)

    my_automat = NFA.from_ast(ast.head)
    print(my_automat, "\n")

    while True:
        word: str = input("Provide a word: ")
        print(my_automat.is_word_accepted(word))
        print("=" * 10)
