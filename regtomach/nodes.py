from anytree import AnyNode


class Literal(AnyNode):
    def __init__(self, value, parent=None):
        super().__init__(name=f"Literal({value})", parent=parent)
        self.value = value


class Sequence(AnyNode):
    def __init__(self, children, parent=None):
        super().__init__(name="Sequence", parent=parent)
        for child in children:
            child.parent = self


class Kleene(AnyNode):
    def __init__(self, child, parent=None):
        super().__init__(name="Kleene", parent=parent)
        child.parent = self


class Optional(AnyNode):
    def __init__(self, child, parent=None):
        super().__init__(name="Optional", parent=parent)
        child.parent = self


class Alternative(AnyNode):
    def __init__(self, branches, parent=None):
        super().__init__(name="Alternative", parent=parent)
        for br in branches:
            br.parent = self
