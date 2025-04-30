from my_compiler.nodes import Alternative, KleeneClosure, Optional, Symbol, EmptyString


TEST_TREE = [Alternative(KleeneClosure(Symbol("A")), Optional(Symbol("B")))]
