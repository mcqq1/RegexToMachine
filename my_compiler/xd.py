from dataclasses import dataclass
from typing import Union, List

# Define regex node types
@dataclass
class Empty:
    pass

@dataclass
class Symbol:
    value: str

@dataclass
class Sequence:
    first: any
    second: any

@dataclass
class Alternative:
    left: any
    right: any

@dataclass
class Star:
    inner: any

@dataclass
class Plus:
    inner: any

@dataclass
class Optional:
    inner: any

# Parser
class RegexParser:
    def __init__(self, regex: str):
        self.regex = regex
        self.index = 0

    def parse(self):
        if not self.regex:
            return Empty()
        result = self.parse_expression()
        return result

    def parse_expression(self):
        terms = [self.parse_term()]

        while self.peek() == '|':
            self.consume('|')
            terms.append(self.parse_term())

        if len(terms) == 1:
            return terms[0]
        else:
            expr = terms[0]
            for term in terms[1:]:
                expr = Alternative(expr, term)
            return expr

    def parse_term(self):
        factors = [self.parse_factor()]

        while self.peek() and self.peek() not in '|)]':
            factors.append(self.parse_factor())

        if len(factors) == 1:
            return factors[0]
        else:
            expr = factors[0]
            for factor in factors[1:]:
                expr = Sequence(expr, factor)
            return expr

    def parse_factor(self):
        base = self.parse_base()

        while True:
            if self.peek() == '*':
                self.consume('*')
                base = Star(base)
            elif self.peek() == '+':
                self.consume('+')
                base = Plus(base)
            elif self.peek() == '?':
                self.consume('?')
                base = Optional(base)
            else:
                break
        return base

    def parse_base(self):
        if self.peek() == '(':
            self.consume('(')
            expr = self.parse_expression()
            self.consume(')')
            return expr
        elif self.peek() == 'ε':
            self.consume('ε')
            return Empty()
        else:
            return Symbol(self.consume_symbol())

    def consume_symbol(self):
        ch = self.regex[self.index]
        self.index += 1
        return ch

    def peek(self):
        if self.index >= len(self.regex):
            return None
        return self.regex[self.index]

    def consume(self, expected):
        if self.regex[self.index] != expected:
            raise ValueError(f"Expected '{expected}', got '{self.regex[self.index]}'")
        self.index += 1

def print_tree(node, prefix="", is_tail=True):
    connector = "└── " if is_tail else "├── "

    if isinstance(node, Empty):
        print(prefix + connector + "Empty")
    elif isinstance(node, Symbol):
        print(prefix + connector + f"<SYMBOL,{node.value}>")
    elif isinstance(node, Sequence):
        print(prefix + connector + "Sequence")
        print_tree(node.first, prefix + ("    " if is_tail else "│   "), False)
        print_tree(node.second, prefix + ("    " if is_tail else "│   "), True)
    elif isinstance(node, Alternative):
        print(prefix + connector + "Alternative")
        print_tree(node.left, prefix + ("    " if is_tail else "│   "), False)
        print_tree(node.right, prefix + ("    " if is_tail else "│   "), True)
    elif isinstance(node, Star):
        print(prefix + connector + "Kleene Star")
        print_tree(node.inner, prefix + ("    " if is_tail else "│   "), True)
    elif isinstance(node, Plus):
        print(prefix + connector + "Positive Closure")
        print_tree(node.inner, prefix + ("    " if is_tail else "│   "), True)
    elif isinstance(node, Optional):
        print(prefix + connector + "Optional")
        print_tree(node.inner, prefix + ("    " if is_tail else "│   "), True)

# Example Usage
if __name__ == "__main__":
    regex = "{a|b}"
    parser = RegexParser(regex)
    tree = parser.parse()

    print("Regex:", regex)
    print("Parsed Regex Tree:")
    print_tree(tree)
