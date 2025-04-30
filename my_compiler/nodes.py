class RegexNode:
    pass

class Alternative(RegexNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"Alternative({self.left}, {self.right})"

class KleeneClosure(RegexNode):
    def __init__(self, expr):
        self.expr = expr
    
    def __repr__(self):
        return f"KleeneClosure({self.expr})"

class Optional(RegexNode):
    def __init__(self, expr):
        self.expr = expr
    
    def __repr__(self):
        return f"Optional({self.expr})"

class Symbol(RegexNode):
    def __init__(self, symbol):
        self.symbol = symbol
    
    def __repr__(self):
        return f"Symbol({self.symbol})"

class EmptyString(RegexNode):
    def __repr__(self):
        return "EmptyString()"
