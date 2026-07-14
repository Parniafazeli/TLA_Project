# -*- coding: utf-8 -*-
from turing_machine import TuringMachine
from test_turing_machine_example1 import print_states
transitions = {
    ('q0', '1'): ('q1', 'X', 'R'),
    ('q1', '0'): ('q_step2_back', '0', 'L'),
    
    ('q_step2_back', 'X'): ('q_step2_clear0', '', 'R'),
    ('q_step2_clear0', '0'): ('qa', '', 'R'),
    
    ('q1', '1'): ('q2', 'X', 'R'),
    
    ('q2', '1'): ('q2', '1', 'R'),
    ('q2', '0'): ('q3', '0', 'R'),
    
    ('q3', '1'): ('q4', 'Y', 'R'),
    
    ('q4', '1'): ('q4', '1', 'R'),
    ('q4', ''): ('q_step8', '#', 'R'),
    
    ('q4', '#'): ('q_step11', '#', 'R'),
    
    ('q_step8', ''): ('q5', '1', 'L'),
    
    ('q5', '1'): ('q5', '1', 'L'),
    ('q5', '#'): ('q5', '#', 'L'),
    ('q5', 'Y'): ('q6', 'Y', 'R'),
    
    ('q6', '1'): ('q7', 'Y', 'R'),
    
    ('q6', '#'): ('q8', '#', 'L'),
    
    ('q7', '1'): ('q7', '1', 'R'),
    ('q7', '#'): ('q_step11', '#', 'R'),
    ('q_step11', '1'): ('q_step11', '1', 'R'),
    ('q_step11', ''): ('q5', '1', 'L'),
    
    ('q8', 'Y'): ('q8', '1', 'L'),
    
    ('q8', '0'): ('q9', '0', 'L'),
    ('q9', '1'): ('q9', '1', 'L'),
    
    ('q9', 'X'): ('q15_check', 'X', 'R'),
    
    ('q15_check', '1'): ('q2', 'X', 'R'),
    ('q15_check', '0'): ('q_clean_leftmost', '0', 'L'),
    
    ('q_clean_leftmost', 'X'): ('q_clean_leftmost', '', 'L'),
    ('q_clean_leftmost', ''): ('q_clean_rightwards', '', 'R'),
    ('q_clean_rightwards', ''): ('q_clean_rightwards', '', 'R'),
    
    ('q_clean_rightwards', '0'): ('q_clean_skip1s', '', 'R'),
    ('q_clean_skip1s', '1'): ('q_clean_skip1s', '1', 'R'),
    
    ('q_clean_skip1s', '#'): ('q_find_blank_end', '1', 'R'),
    
    ('q_find_blank_end', '1'): ('q_find_blank_end', '1', 'R'),
    ('q_find_blank_end', ''): ('q_remove_last_1', '', 'L'),
    ('q_remove_last_1', '1'): ('qa', '', 'L')
}


if __name__ == "__main__":
    print_states(transitions)
    machine = TuringMachine(transitions)

    def run(input_):
        w = input_
        print("Input:",w)
        print("Accepted" if machine.accepts(w) else "Rejected")
        machine.debug(w, step_limit=1000)

        print()

    # SHOULD ACCEPT
    run("110111")
    # outputs 111111

    # SHOULD ACCEPT
    run("11101111")
    # outputs 111111111111

    run("01111")
