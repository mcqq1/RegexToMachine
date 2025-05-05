from collections import defaultdict
from tabulate import tabulate


class NFA:
    def __init__(self):
        # Set of state identifiers
        self.states = set()
        # Start state identifier
        self.start_state = None
        # Set of accept state identifiers
        self.accept_states = set()
        # Transitions: state -> symbol (or None for ε) -> set of destination states
        self.transitions = defaultdict(lambda: defaultdict(set))

    def __repr__(self):
        symbols = []
        for symbol_to_state in self.transitions.values():
            symbols.extend(list(symbol_to_state.keys()))
        symbols = set(symbols)

        sorted_states = sorted(self.states, key=lambda s: int(s[1:]))

        headers = ["States"]
        headers.extend(symbols)

        rows = []
        for state in sorted_states:
            row = [state]

            for from_state, symbol_to_states in self.transitions.items():
                if state != from_state:
                    continue

                for symbol in symbols:
                    next_states = symbol_to_states[symbol]
                    row.append(next_states) if next_states else row.append(None)

            rows.append(row)

        for row in rows:
            if row[0] == self.start_state:
                row[0] = f"{row[0]} (start)"
            if row[0] in self.accept_states:
                row[0] = f"{row[0]} (accept)"

        return tabulate(rows, headers, tablefmt="github")

    @classmethod
    def from_ast(cls, ast):
        nfa = cls()
        # Counter for unique state IDs
        state_counter = 0

        def new_state():
            nonlocal state_counter
            sid = f"S{state_counter}"
            state_counter += 1
            nfa.states.add(sid)
            return sid

        def add_transition(frm, symbol, to):
            nfa.transitions[frm][symbol].add(to)

        def build(node):
            """
            recursively build a fragment for the AST node.
            returns a tuple (start_state, set_of_accept_states).
            """
            nodetype = type(node).__name__

            if nodetype == "Literal":
                # Single-symbol NFA
                start = new_state()
                end = new_state()
                symbol = node.value
                add_transition(start, symbol, end)
                return start, {end}

            elif nodetype == "Sequence":
                # Concatenate all children in order
                children = node.children
                s, accepts = build(children[0])
                for child in children[1:]:
                    next_s, next_accepts = build(child)
                    for acc in accepts:
                        add_transition(acc, None, next_s)
                    accepts = next_accepts
                return s, accepts

            elif nodetype == "Alternative":
                # Union: create new entry and exit with ε-links
                start = new_state()
                end = new_state()
                for child in node.children:
                    cs, cas = build(child)
                    add_transition(start, None, cs)
                    for acc in cas:
                        add_transition(acc, None, end)
                return start, {end}

            elif nodetype == "Kleene":
                # Kleene star (zero or more)
                start = new_state()
                end = new_state()
                cs, cas = build(node.children[0])
                # ε into body and bypass
                add_transition(start, None, cs)
                add_transition(start, None, end)
                # loop back and exit
                for acc in cas:
                    add_transition(acc, None, cs)
                    add_transition(acc, None, end)
                return start, {end}

            elif nodetype == "Optional":
                # Zero or one: like Kleene but no loop back
                start = new_state()
                end = new_state()
                cs, cas = build(node.children[0])
                add_transition(start, None, cs)
                add_transition(start, None, end)
                for acc in cas:
                    add_transition(acc, None, end)
                return start, {end}

            else:
                raise ValueError(f"Unsupported AST node type: {nodetype}")

        # Build full NFA
        start, accepts = build(ast)
        nfa.start_state = start
        nfa.accept_states = accepts
        return nfa
    

    def is_word_accepted(self, word: str) -> bool:
        """
        Simulate the NFA on the input word. Returns True if the NFA accepts it.
        """

        def epsilon_closure(states: set[str]) -> set[str]:
            """Compute the ε-closure of a set of states."""
            stack = list(states)
            closure = set(states)
            while stack:
                state = stack.pop()
                for nxt in self.transitions[state].get(None, ()):
                    if nxt not in closure:
                        closure.add(nxt)
                        stack.append(nxt)
            return closure

        # starting with ε-closure of the start state
        current = epsilon_closure({self.start_state})

        # for each input symbol, move and re-closure
        for sym in word:
            # move: from each state on sym
            next_states = set()
            for st in current:
                for tgt in self.transitions[st].get(sym, ()):
                    next_states.add(tgt)
            # take ε-closure again
            current = epsilon_closure(next_states)

            # If no states reachable, reject early
            if not current:
                return False

        # accept if any current state is in accept_states
        return any(st in self.accept_states for st in current)
