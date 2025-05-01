class Node:
    def __repr__(self):
        return f"{self.__class__.__name__}({self.get_children()})"

    def get_children(self):
        return None


class Symbol(Node):
    def __init__(self, value):
        self.value = value

    def get_children(self):
        return None

class Concat(Node):
    def __init__(self, children):
        self.children = children

    def get_children(self):
        return self.children

class Alternative(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def get_children(self):
        return [self.left, self.right]

class Optional(Node):
    def __init__(self, expr):
        self.expr = expr

    def get_children(self):
        return self.expr


class KleeneClosure(Node):
    def __init__(self, expr):
        self.expr = expr

    def get_children(self):
        return self.expr

class EmptyString(Node):
    
    def get_children(self):
        return None
