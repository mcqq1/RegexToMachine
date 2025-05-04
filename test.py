from regtomach.state_machine import StateMachine, Transition, StateMachineError


def main():
    # Define transitions
    t1 = Transition(from_state="q0", to_state="q1", symbol="a")
    t2 = Transition(from_state="q1", to_state="q2", symbol="b")

    # Create state machine
    dfa = StateMachine(
        states=["q0", "q1", "q2"],
        transitions=[t1, t2],
        start_state="q0",
        end_states=["q2"]
    )

    # Test cases
    test_words = [
        "ab",     # should be accepted
        "a",      # should be rejected (no 'b')
        "b",      # should be rejected (doesn't start with 'a')
        "abb",    # should be rejected (too long)
        "",       # should be rejected (empty string)
        "abc",    # should be rejected (invalid symbol 'c')
    ]

    for word in test_words:
        try:
            result = dfa.is_word_accepted(word)
            print(f"Word '{word}' accepted? {result}")
        except StateMachineError as e:
            print(f"Word '{word}' caused an error: {e}")
    
    print(dfa)

if __name__ == "__main__":
    main()