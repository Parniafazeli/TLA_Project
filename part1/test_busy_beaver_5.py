
from turing_machine import TuringMachine
from test_turing_machine_example1 import print_states


transitions = {
    
('a','0'): ('b','1','R'),
    ('a','1'): ('b','1','L'),


    ('b','0'): ('a','1','L'),
    ('b','1'): ('c','0','L'),


    ('c','0'): ('e','1','R'),
    ('c','1'): ('d','1','L'),


    ('d','0'): ('d','1','R'),
    ('d','1'): ('a','0','R'),


    ('e', '0'): ('e', '1', 'R'),
    ('e', '1'): ('qa', '1', 'L'),

}

if __name__ == "__main__":

    print("================")
    print("BB with 5 states")

    print_states(transitions)


    tm = TuringMachine(
        transitions,
        start_state='a',
        accept_state='qa',
        reject_state='r',
        blank_symbol='0'

    )


    tm.debug("", step_limit=5000)