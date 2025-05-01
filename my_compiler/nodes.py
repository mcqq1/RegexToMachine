class Node:

    def __init__(self, children: list["Node"]):
        self.children = children

    def __str__(self):
        return f"{self.__class__.__name__}({self.children})"


class Symbol(Node):
    keychars: list[str] = None


class Alternative(Node):

    keychars: list[str] = ["|"]


class KleeneClosure(Node):

    keychars: list[str] = ["{", "}"]
    is_bracket: bool = True


class Optional(Node):

    keychars: list[str] = ["[", "]"]
    is_bracket: bool = True


class EmptyString(Node):

    keychars: list[str] = ["ε"]
