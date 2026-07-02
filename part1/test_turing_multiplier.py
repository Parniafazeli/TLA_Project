# -*- coding: utf-8 -*-
from turing_machine import TuringMachine
from test_turing_machine_example1 import print_states

#create the Turing machine
transitions = {
    ('q0', '1'): ('q0', '1', 'R'),
    ('q0', '0'): ('q1', '0', 'R'),
    
    ('q1', '1'): ('q2', '0', 'L'),
    ('q1', '0'): ('q5', '0', 'R'),
    
    ('q2', '1'): ('q2', '1', 'L'),
    ('q2', '0'): ('q2', '0', 'L'),
    ('q2', ''): ('q3', '', 'R'),
    
    ('q3', '1'): ('q3', '1', 'R'),
    ('q3', '0'): ('q4', '0', 'R'),
    
    ('q4', '1'): ('q4', '1', 'R'),
    ('q4', '0'): ('q4', '0', 'R'),
    ('q4', ''): ('q6', '1', 'L'),
    
    ('q6', '1'): ('q6', '1', 'L'),
    ('q6', '0'): ('q7', '0', 'L'),
    
    ('q7', '1'): ('q4', '1', 'R'),
    ('q7', '0'): ('q1', '0', 'R'),
    
    ('q5', '0'): ('q5', '0', 'R'),
    ('q5', '1'): ('q8', '', 'R'),
    
    ('q8', '1'): ('q8', '1', 'R'),
    ('q8', '0'): ('q8', '', 'R'),
    ('q8', ''): ('qa', '', 'R'),
}


if __name__ == "__main__":
    print_states(transitions)
    machine = TuringMachine(transitions)

    def run(input_):
        w = input_
        print("Input:",w)
        print("Accepted" if machine.accepts(w) else "Rejected")
        # machine.debug(w, step_limit=1000)

        print()

    # SHOULD ACCEPT
    run("110111")
    # outputs 111111

    # SHOULD ACCEPT
    run("11101111")
    # outputs 111111111111

    run("01111")
