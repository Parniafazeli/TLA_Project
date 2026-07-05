from turing_machine import TuringMachine

beaver_programs = [
    {},  # 0

    {
        ('a', '0'): ('h', '1', 'R'),
    },

    # 2-state: 4 ones
    {
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('b', '1', 'L'),
        ('b', '0'): ('a', '1', 'L'),
        ('b', '1'): ('h', '1', 'R'),
    },

    # 3-state: 6 ones
    {
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('c', '1', 'L'),
        ('b', '0'): ('a', '1', 'L'),
        ('b', '1'): ('b', '1', 'R'),
        ('c', '0'): ('b', '1', 'L'),
        ('c', '1'): ('h', '1', 'R'),
    },

    # 4-state: 13 ones 
    {
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('b', '1', 'L'),
        ('b', '0'): ('a', '1', 'L'),
        ('b', '1'): ('c', '1', 'R'),
        ('c', '0'): ('d', '1', 'L'),
        ('c', '1'): ('h', '1', 'R'),
        ('d', '0'): ('a', '1', 'L'),
        ('d', '1'): ('d', '0', 'R'),   
    },

    # 5-state: 4098 ones
    {
        ('a', '0'): ('b', '1', 'R'),
        ('a', '1'): ('c', '1', 'L'),
        ('b', '0'): ('a', '1', 'L'),
        ('b', '1'): ('d', '1', 'R'),
        ('c', '0'): ('e', '1', 'L'),
        ('c', '1'): ('b', '1', 'L'),
        ('d', '0'): ('a', '1', 'R'),
        ('d', '1'): ('e', '0', 'L'),
        ('e', '0'): ('h', '1', 'R'),
        ('e', '1'): ('c', '0', 'L'),
    },

]

def busy_beaver(n):
    if n < 1 or n > 6:
        print("n must be between 1 and 6")
        return

    program = beaver_programs[n]
    if not program:
        print(f"No program defined for {n} states.")
        return

    print(f"\nRunning Busy Beaver with {n} states...")

    tm = TuringMachine(
        program,
        start_state='a',
        accept_state='h',
        reject_state='r',
        blank_symbol='0'
    )

    initial_tape = '0' * 14
    step_limit = 50000000 if n == 5 else 10000

    result = tm.accepts(initial_tape, step_limit=step_limit)
    if result is None:
        print(f"Step limit {step_limit} reached without halting.")
        return

    print(f"Result: {'Accepted' if result else 'Rejected'}")

    last_config = None
    for action, config in tm.run(initial_tape):
        last_config = config
        if action is not None:
            break

    if last_config:
        left = ''.join(reversed(last_config['left_hand_side']))
        right = ''.join(last_config['right_hand_side'])
        tape = left + last_config['symbol'] + right
        ones_count = tape.count('1')
        print(f"Number of 1s written: {ones_count}")
        print(f"Final tape: {tape}")

def usage():
    print("Usage: python busy_beaver.py [1|2|3|4|5|6]")
    import sys
    sys.exit(1)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        usage()
    try:
        n = int(sys.argv[1])
        busy_beaver(n)
    except ValueError:
        usage()