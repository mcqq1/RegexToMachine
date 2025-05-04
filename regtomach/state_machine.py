from regtomach.abstract_syntax_tree import AbstractSyntaxTree
from anytree import Node


class Transition:
    def __init__(self, start: State, end: State, character: str):
        self.start: State = start
        self.end: State = end
        self.character: str = character


class State:
    def __init__(self, name: str, transitions: list[Transition]):
        self.name = name
        self.transitions = transitions


class StateMachine:

    @classmethod
    def from_abstract_syntax_tree(cls, ast: AbstractSyntaxTree):
        pass

    def __init__(
        self,
        states: list[State],
        transitions: list[Transition],
        start_state: State,
        end_states: list[State],
    ):
        self.states: list[State] = states
        self.transitions: list[Transition] = transitions
        self.start_state: State = start_state
        self.end_states: list[State] = end_states

    def is_word_accepted(word: str) -> bool:
        pass
