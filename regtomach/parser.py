

class Parser:
    def __init__(self, regex):
        self.regex = regex
        self.pos = 0

    def parse(self):
        node = self._parse_expression()
        if self.pos < len(self.regex):
            raise ValueError(f"Unexpected character at pos {self.pos}: {self.regex[self.pos]}")
        return node

    def _peek(self):
        return self.regex[self.pos] if self.pos < len(self.regex) else None

    def _parse_expression(self):
        # parse branches separated by |
        branches = [self._parse_term()]
        while self._peek() == '|':
            self.pos += 1
            branches.append(self._parse_term())
        if len(branches) > 1:
            return Alternative(branches)
        return branches[0]

    def _parse_term(self):
        # parse sequence of factors
        factors = []
        while True:
            c = self._peek()
            if c is None or c in ']|}':
                break
            if c == '|':
                break
            factors.append(self._parse_factor())
        if len(factors) > 1:
            return Sequence(factors)
        elif factors:
            return factors[0]
        else:
            # empty sequence => treat as empty literal
            return Literal('')

    def _parse_factor(self):
        c = self._peek()
        if c == '{':
            return self._parse_group(Kleene, '{', '}')
        elif c == '[':
            return self._parse_group(Optional, '[', ']')
        else:
            # literal (any non-special)
            self.pos += 1
            return Literal(c)

    def _parse_group(self, NodeClass, open_ch, close_ch):
        # consume opening
        self.pos += 1
        start = self.pos
        depth = 1
        # find matching close_ch
        while self.pos < len(self.regex) and depth:
            if self.regex[self.pos] == open_ch:
                depth += 1
            elif self.regex[self.pos] == close_ch:
                depth -= 1
            self.pos += 1
        if depth != 0:
            raise ValueError(f"Unmatched {open_ch}")
        # inner text without the final close_ch
        inner = self.regex[start:self.pos-1]
        # parse inner separately
        child = RegexParser(inner).parse()
        return NodeClass(child)

def parse_regex(rgx: str) -> AnyNode:
    """Parse `rgx` into an anytree AST."""
    return RegexParser(rgx).parse()
