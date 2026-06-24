# -*- coding: utf-8 -*-

from turing_machine import TuringMachine
from test_turing_machine_example1 import print_states



# Busy Beaver 5-state نمونه
# فقط کافی است بیشتر از 2،3،4 حالت قبلی باشد

transitions = {


    # A
    ('a',''): ('b','1','R'),
    ('a','1'): ('c','1','L'),


    # B
    ('b',''): ('a','1','R'),
    ('b','1'): ('b','1','R'),


    # C
    ('c',''): ('d','1','L'),
    ('c','1'): ('a','1','L'),


    # D
    ('d',''): ('e','1','R'),
    ('d','1'): ('d','1','L'),


    # E
    ('e',''): ('a','1','R'),
    ('e','1'): ('qa','1','R'),

}



if __name__ == "__main__":

    print("================")
    print("BB with 5 states")

    print_states(transitions)


    tm = TuringMachine(
        transitions,
        start_state='a'
    )


    tm.debug("", step_limit=5000)