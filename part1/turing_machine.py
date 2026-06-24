# -*- coding: utf-8 -*-
"""A Turing machine simulator with double-sided infinite tape.

    Accepting '#'
    =============

    >>> from turing_machine import TuringMachine

    Instantiate the machine with particular transitions.

    >>> one_hash = TuringMachine(
    ...     {
    ...         ('q0', '#'): ('saw_#', '#', 'R'),
    ...         ('saw_#', ''): ('qa', '', 'R'),
    ...     }
    ... )

    Check whether it accepts a string:

    >>> one_hash.accepts('#')
    True

    >>> one_hash.accepts('##')
    False

    Check whether it rejects a string:

    >>> one_hash.rejects('#')
    False

    >>> one_hash.rejects('##')
    True

"""

import logging
from itertools import islice


class TuringMachine:
    """Turing machine simulator class with double-sided infinite tape.

    A machine is instantiated with transitions, start, accept and reject states
    and a blank symbol. We assume that the input and the tape alphabet can be
    deducted from the transitions.

    :param dict transitions: a mapping from (state, symbol) tuples to (state,
    symbol, direction) tuple. Directions are either 'L' (for left) or 'R' (for right).

    :param start_state: the initial state of the machine.

    :param accept_state: the accept state.

    :param reject_state: the reject state.

    :param blank_symbol: the special symbol that marks the tape cell to be empty.
    """

    def __init__(self, transitions, start_state='q0', accept_state='qa', reject_state='qr', blank_symbol=''):
        """Initialize the Turing machine."""
        self.transitions = transitions
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.blank_symbol = blank_symbol
        self.logger = logging.getLogger(__name__)

    def run(self, input_):
        """Execute the Turing machine for a particular input.

        :param input_: the input that is written on the tape. It can be a list
        of strings, or just a string, in which case each letter is treated as a symbol.

        This method MUST be a Python generator. It should yield a (action, configuration) tuple
        at each step of the computation.
        
        The action is either 'Accept', 'Reject' or None. 
        
        Configuration is a dictionary with the following keys:
        - 'state': the current state,
        - 'left_hand_side': list of symbols on the left hand side of the current position (closest first),
        - 'symbol': the current symbol under the head,
        - 'right_hand_side': list of symbols on the right hand side of the current position.
        """
        # Convert input string to list of symbols if needed
        if isinstance(input_, str):
            tape_symbols = list(input_)
        else:
            tape_symbols = list(input_)

        # Initialize tape: left side (reversed order, closest to head is last)
        left = []                # reversed left part, e.g. [cell_left2, cell_left1]
        # right side (normal order, first element is immediate right)
        right = tape_symbols[:]  # copy
        # current symbol under head
        if right:
            current_symbol = right.pop(0)
        else:
            current_symbol = self.blank_symbol

        state = self.start_state

        while True:
            # Build configuration dictionary
            config = {
                'state': state,
                'left_hand_side': left[:],      # return a copy
                'symbol': current_symbol,
                'right_hand_side': right[:]     # return a copy
            }

            # Check for halting states
            if state == self.accept_state:
                yield ('Accept', config)
                return
            if state == self.reject_state:
                yield ('Reject', config)
                return

            # Yield current step (machine still running)
            yield (None, config)

            # Look up transition
            key = (state, current_symbol)
            if key not in self.transitions:
                # No transition defined: reject
                state = self.reject_state
                continue

            next_state, write_symbol, direction = self.transitions[key]

            # Write symbol (overwrite current cell)
            current_symbol = write_symbol

            # Move head (double-sided infinite tape)
            if direction == 'R':
                # Move right: current cell becomes part of left side,
                # and new current symbol is taken from right (or blank if empty)
                left.append(current_symbol)
                if right:
                    current_symbol = right.pop(0)
                else:
                    current_symbol = self.blank_symbol
            elif direction == 'L':
                # Move left: current cell becomes part of right side (at front),
                # and new current symbol is taken from left (or blank if empty)
                right.insert(0, current_symbol)
                if left:
                    current_symbol = left.pop()
                else:
                    current_symbol = self.blank_symbol
            else:
                raise ValueError(f"Invalid direction: {direction}")

            # Update state
            state = next_state

    def accepts(self, input_, step_limit=100):
        """Check whether the Turing machine accepts a string.

        :param input_: the input string or list.
        :param step_limit: the maximum number of steps to simulate before stopping.
        :return: True if the machine halts in accept_state, False if it rejects,
                 or None if the step limit is reached without halting.
        """
        steps = 0
        for action, _ in self.run(input_):
            if steps >= step_limit:
                self.logger.warning(f"Step limit {step_limit} reached without halting.")
                return None
            if action == 'Accept':
                return True
            if action == 'Reject':
                return False
            steps += 1
        # Should not reach here because generator always ends with Accept/Reject
        return None

    def rejects(self, input_, **kwargs):
        """Check whether the Turing machine rejects a string.

        :param input_: the input string or list.
        :return: True if the machine rejects the string, False if it accepts.
        """
        result = self.accepts(input_, **kwargs)
        if result is None:
            return None
        return not result

    def debug(self, input_, step_limit=100, colored=False):
        """Print the execution configuration of the machine per transition for debugging.

        :param input_: the input string or list.
        :param step_limit: the maximum number of steps to output.
        :param colored: True to output colored boundaries in terminal.
        """
        for i, (action, config) in enumerate(self.run(input_)):
            if i >= step_limit:
                print(f"\n[Reached step limit {step_limit}]")
                break
            state = config['state']
            left_list = config['left_hand_side']
            symbol = config['symbol']
            right_list = config['right_hand_side']

            # left_list is stored reversed (closest to head is last)
            # For printing we need it in normal order (leftmost to cell left of head)
            left_normal = ''.join(reversed(left_list))
            right_normal = ''.join(right_list)

            # Print format: state left[symbol]right
            print(f"{state} {left_normal}[{symbol}]{right_normal}")
            
            if action is not None:
                print(f"Halts with {action}")
                break