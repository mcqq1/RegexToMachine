class Node:

    def __init__(self, keychars: list[str], children: list["Node"]):
        self.keychars = keychars
        self.children = children


class Alternative(Node):

    def __repr__(self):
        return f"Alternative()"


class KleeneClosure(Node):

    def __repr__(self):
        return f"KleeneClosure({self.expr})"


class Optional(Node):

    def __repr__(self):
        return f"Optional({self.expr})"


class Symbol(Node):

    def __repr__(self):
        return f"Symbol({self.symbol})"


class EmptyString(Node):

    def __repr__(self):
        return "EmptyString()"
