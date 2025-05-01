from my_compiler.nodes import (
    Symbol,
    Concat,
    Alternative,
    Optional,
    KleeneClosure,
    EmptyString,
)


class Parser:
    def __init__(self, input_):
        self.input = input_
        self.pos = 0

    def current(self):
        return self.input[self.pos] if self.pos < len(self.input) else None

    def consume(self):
        self.pos += 1

    def match(self, expected):
        if self.current() == expected:
            self.consume()
            return True
        return False

    def parse_expression(self):
        left = self.parse_term()
        while self.match("|"):
            right = self.parse_term()
            left = Alternative(left, right)
        return left

    def parse_term(self):
        factors = []
        while self.current() and self.current() not in "|)]}":
            factors.append(self.parse_factor())
        return factors[0] if len(factors) == 1 else Concat(factors)

    def parse_factor(self):
        char = self.current()

        if char == "(":
            self.consume()
            expr = self.parse_expression()
            assert self.match(")"), "Expected ')'"
            return expr
        elif char == "[":
            self.consume()
            expr = self.parse_expression()
            assert self.match("]"), "Expected ']'"
            return Optional(expr)
        elif char == "{":
            self.consume()
            expr = self.parse_expression()
            assert self.match("}"), "Expected '}'"
            return KleeneClosure(expr)
        elif char == "ε":
            self.consume()
            return EmptyString()
        else:
            self.consume()
            return Symbol(char)
