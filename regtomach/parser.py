from regtomach.nodes import Optional, Alternative, Concat, KleeneClosure, Symbol, EmptyString
from regtomach.abstract_syntax_tree import AbstractSyntaxTree


class Parser:
    def __init__(self, input_str):
        self.input = input_str
        self.pos = 0
    
    def generate_syntax_tree(self):
        return AbstractSyntaxTree(self.parse())

    def peek(self):
        return self.input[self.pos] if self.pos < len(self.input) else None

    def consume(self):
        current = self.peek()
        self.pos += 1
        return current

    def parse(self):
        return self.parse_alternative()

    def parse_alternative(self):
        alternatives = [self.parse_concat()]
        while self.peek() == "|":
            self.consume()  # consume '|'
            alternatives.append(self.parse_concat())
        if len(alternatives) == 1:
            return alternatives[0]
        alt_node = Alternative()
        for child in alternatives:
            child.parent = alt_node
        return alt_node

    def parse_concat(self):
        nodes = []
        while self.peek() and self.peek() not in "|]}":
            nodes.append(self.parse_quantified())
        if len(nodes) == 1:
            return nodes[0]
        concat_node = Concat()
        for child in nodes:
            child.parent = concat_node
        return concat_node

    def parse_quantified(self):
        node = self.parse_atom()
        while self.peek() and self.peek() in "[{":
            if self.peek() == "[":
                self.consume()  # consume '['
                opt_node = Optional()
                self.parse_inner(node, opt_node, "]")
                node = opt_node
            elif self.peek() == "{":
                self.consume()  # consume '{'
                kleene_node = KleeneClosure()
                self.parse_inner(node, kleene_node, "}")
                node = kleene_node
        return node

    def parse_inner(self, child, parent_node, end_char):
        child.parent = parent_node
        while self.peek() and self.peek() != end_char:
            self.parse_concat().parent = parent_node
        self.consume()  # consume the closing ']' or '}'

    def parse_atom(self):
        char = self.peek()
        if char is None:
            return EmptyString()
        elif char not in "|[]{}":
            return Symbol(self.consume())
        return EmptyString()
