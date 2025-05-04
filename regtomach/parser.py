from anytree import Node as AnyNode
from regtomach.abstract_syntax_tree import AbstractSyntaxTree

class Parser:
    def __init__(self, input_):
        self.input = input_
        self.pos = 0
    
    def generate_syntax_tree(self) -> AbstractSyntaxTree:
        head_node = self.parse_expression()
        return AbstractSyntaxTree(head=head_node)

    def current(self):
        return self.input[self.pos] if self.pos < len(self.input) else None

    def consume(self):
        self.pos += 1

    def match(self, expected):
        if self.current() == expected:
            self.consume()
            return True
        return False

    def parse_expression(self, parent=None):
        node = self.parse_term(parent=parent)
        while self.match("|"):
            alt_node = AnyNode("Alternative", parent=parent)
            alt_node.children = (node, self.parse_term(parent=alt_node))
            node = alt_node
        return node

    def parse_term(self, parent=None):
        factors = []
        while self.current() and self.current() not in "|)]}":
            factors.append(self.parse_factor(parent=parent))
        if len(factors) == 1:
            return factors[0]
        node = AnyNode("Concat", parent=parent)
        for f in factors:
            f.parent = node
        return node

    def parse_factor(self, parent=None):
        char = self.current()

        if char == "(":
            self.consume()
            return self.parse_expression(parent=parent if parent else None)
        elif char == "[":
            self.consume()
            node = AnyNode("Optional", parent=parent)
            inner = self.parse_expression(parent=node)
            assert self.match("]"), "Expected ']'"
            return node
        elif char == "{":
            self.consume()
            node = AnyNode("KleeneClosure", parent=parent)
            inner = self.parse_expression(parent=node)
            assert self.match("}"), "Expected '}'"
            return node
        elif char == "ε":
            self.consume()
            return AnyNode("EmptyString", parent=parent)
        else:
            self.consume()
            return AnyNode(f"Symbol('{char}')", parent=parent)

    def parse(self):
        return self.parse_expression()
