from regtomach.parser import Parser
from regtomach.abstract_syntax_tree import AbstractSyntaxTree
from regtomach.state_machine import StateMachine
from loguru import logger

def main():
    gowno = "[A|B]"
    parser = Parser(gowno)

    syntax_tree: AbstractSyntaxTree = parser.generate_syntax_tree()
    
    logger.info("Your syntax tree:")
    print(syntax_tree)
    syntax_tree.save_to_png()
    
    # machine: StateMachine = StateMachine.from_abstract_syntax_tree(syntax_tree.head)
    
    while True:
        break
        word = input("Provide a word: ")
        print("Accepted") if machine.is_word_accepted(word) else print("Not accepted")
        print("=" * 10)


if __name__ == "__main__":
    main()
