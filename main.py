from regtomach.parser import Parser
from regtomach.abstract_syntax_tree import AbstractSyntaxTree
from regtomach.state_machine import StateMachine
from loguru import logger

def main():
    parser = Parser("{A|[CD]B}")

    syntax_tree: AbstractSyntaxTree = parser.generate_syntax_tree()
    
    logger.info("Your syntax tree:")
    print(syntax_tree)
    syntax_tree.save_to_png()
    
    machine: StateMachine = StateMachine.from_abstract_syntax_tree(syntax_tree)
    


if __name__ == "__main__":
    main()
