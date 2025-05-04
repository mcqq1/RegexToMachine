from anytree import NodeMixin

class ASTNode(NodeMixin):
    def __init__(self, parent=None):
        self.parent = parent
    
    @property
    def name(self):
        return self.__repr__()
    
    def __repr__(self):
        repr: str = self.__class__.__name__
        if hasattr(self, "symbol"):
            repr += f"({self.symbol})"
        return repr

class Symbol(ASTNode):
    def __init__(self, symbol, parent=None):
        super().__init__(parent)
        self.symbol = symbol

class Alternative(ASTNode):
    pass

class Concat(ASTNode):
    pass

class Optional(ASTNode):
    pass

class KleeneClosure(ASTNode):
    pass

class EmptyString(ASTNode):
    pass
