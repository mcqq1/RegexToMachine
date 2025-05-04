from regtomach.abstract_syntax_tree import AbstractSyntaxTree
from tabulate import tabulate
from collections import defaultdict
from anytree import Node


class StateMachineError(Exception):
    pass


class Transition:
    def __init__(self, from_state: str, to_state: str, symbol: str):
        self.from_state: str = from_state
        self.to_state: str = to_state
        self.symbol: str = symbol

    def __repr__(self):
        return f"{self.from_state} --{self.symbol}--> {self.to_state}"


class StateMachine:

    def __init__(
        self,
        states: list[str] = [],
        transitions: list[Transition] = [],
        start_state: str = None,
        end_states: list[str] = [],
    ):
        self.states: list[str] = states
        self.transitions: list[Transition] = transitions
        self.start_state: str = start_state
        self.end_states: list[str] = end_states

    def __repr__(self):
        # building a nested dictionary: from_state -> symbol -> to_state
        table_data = defaultdict(dict)
        symbols_set = set()
        for t in self.transitions:
            table_data[t.from_state][t.symbol] = t.to_state
            symbols_set.add(t.symbol)

        symbols = sorted(symbols_set)
        headers = ["State"] + symbols
        rows = []

        for state in sorted(self.states):
            row = [state]
            for sym in symbols:
                row.append(table_data[state].get(sym, ""))
            rows.append(row)

        return tabulate(rows, headers=headers, tablefmt="grid")

    @classmethod
    def from_abstract_syntax_tree(cls, ast):
        machine = cls()
        start, ends = machine._build_from_ast(ast)
        machine.start_state = start
        machine.end_states = ends
        return machine

    def _build_from_ast(self, node):
        node_type = node.__class__.__name__

        if node_type == "Symbol":
            start = self.next_state_name()
            end = self.next_state_name()

            self.states.extend([start, end])
            self.transitions.append(Transition(start, end, node.symbol))

            return start, [end]

        elif node_type == "Concat":
            children = node.children
            assert len(children) >= 2, "Concat node must have at least two children"

            start, ends = self._build_from_ast(children[0])

            for child in children[1:]:
                next_start, next_ends = self._build_from_ast(child)

                for e in ends:
                    self.transitions.append(Transition(e, next_start, "ε"))

                ends = next_ends

            return start, ends

        elif node_type == "Alternative":
            start = self.next_state_name()
            end = self.next_state_name()
            self.states.extend([start, end])

            for child in node.children:
                child_start, child_ends = self._build_from_ast(child)
                self.transitions.append(Transition(start, child_start, "ε"))
                for e in child_ends:
                    self.transitions.append(Transition(e, end, "ε"))

            return start, [end]

        elif node_type == "Optional":
            start = self.next_state_name()
            end = self.next_state_name()
            self.states.extend([start, end])

            child_start, child_ends = self._build_from_ast(node.children[0])

            # Path skipping the optional part
            self.transitions.append(Transition(start, end, "ε"))

            # Path including the optional part
            self.transitions.append(Transition(start, child_start, "ε"))
            for e in child_ends:
                self.transitions.append(Transition(e, end, "ε"))

            return start, [end]

        elif node_type == "KleeneClosure":
            start = self.next_state_name()
            end = self.next_state_name()
            self.states.extend([start, end])

            child_start, child_ends = self._build_from_ast(node.children[0])

            # Direct path skipping repetition
            self.transitions.append(Transition(start, end, "ε"))

            # Path into the loop
            self.transitions.append(Transition(start, child_start, "ε"))

            for e in child_ends:
                # Loop back
                self.transitions.append(Transition(e, child_start, "ε"))
                # Or exit loop
                self.transitions.append(Transition(e, end, "ε"))

            return start, [end]

        else:
            raise NotImplementedError(f"AST node type '{node_type}' not supported")

    # auto generates next unique name for state
    def next_state_name(self):
        if not self.states:
            return "q1"

        latest_state: str = self.states[-1]
        latest_state_num: int = int(latest_state[1:])

        return "q" + str(latest_state_num + 1)

    def is_word_accepted(self, word: str) -> bool:
        if self.start_state is None:
            raise StateMachineError("Start state is not defined.")

        current_state = self.start_state

        for token in word:
            #
            next_state = None
            for transition in self.transitions:
                if (
                    transition.from_state == current_state
                    and transition.symbol == token
                ):
                    next_state = transition.to_state
                    break

            if next_state is None:
                # no valid transition found, reject
                return False

            current_state = next_state

        # after consuming the word, check if in an accepting state
        return current_state in self.end_states

    # this generates py file
    def to_drf_py(self):
        quoted_states: list[str] = [f'"{s}"' for s in self.states]

        content: str = (
            "from regtomach.state_machine import StateMachine\n\n"
            "def main():\n"
            f"    states = [{",".join(quoted_states)}]\n"
            f"    transitions = [""]"
            f"    "
            "    my_machine = StateMachine(states, transitions, start_state, end_states)\n"
            "    while True:\n"
            '        text_to_analyze: str = input("Provide a word:")'
            "        if my_machine.is_word_accepted(text_to_analyze):\n"
            '            print("Word is accepted!")\n'
            "        else:\n"
            '            print("Word is not accepted!")\n'
            '        print("=" * 10)\n\n'
            '    if __name__ == "__main__":\n'
            "        main()\n"
        )

        with open("drf.py", "w+") as f:
            f.write(content)
