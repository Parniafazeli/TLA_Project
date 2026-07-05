# -*- coding: utf-8 -*-
"""
Langton's Ant Student Template Module.
"""
import numpy as np


class LangtonsAnt:
    """
    [Part 2 - Langton's Ant]
    Implementation of Langton's Ant with support for multi-color rules.
    """

    def __init__(self, N, ant_position, rules):
        """
        Initialize the Langton's Ant simulation.
        
        Args:
            N (int): The grid size (NxN).
            ant_position (tuple): Starting coordinate of the ant as (r, c).
            rules (dict): Dictionary defining transition rules.
                          Format: {current_color: (next_color, turn_direction)}
                          where turn_direction is 'R' (right) or 'L' (left).
        """
        self.N = N
        self.grid = np.zeros((N, N), dtype=np.int32)
        self.r, self.c = ant_position
        self.direction = 0  # 0=up, 1=right, 2=down, 3=left
        self.rules = rules

    def get_states(self):
        """
        Returns the current state grid of the cells.
        
        Returns:
            np.ndarray: The NxN cellular grid.
        """
        return self.grid

    def get_current_position(self):
        """
        Returns the ant's current position as a tuple (r, c).
        
        Returns:
            tuple: Current coordinates of the ant.
        """
        return (self.r, self.c)

    def step(self):
        """
        Perform a single simulation step following the ruleset.
        """
        # 1. Get current color at ant's position
        current_color = int(self.grid[self.r, self.c])
        
        # 2. Look up rule for this color
        if current_color not in self.rules:
            # If color not in rules, use default: stay same color and turn right
            next_color = current_color
            turn = 'R'
        else:
            next_color, turn = self.rules[current_color]
        
        # 3. Update cell color
        self.grid[self.r, self.c] = next_color
        
        # 4. Turn the ant (R = +1, L = -1)
        if turn == 'R':
            self.direction = (self.direction + 1) % 4
        elif turn == 'L':
            self.direction = (self.direction - 1) % 4
        
        # 5. Move forward one step (with toroidal wrapping)
        if self.direction == 0:      # up
            self.r = (self.r - 1) % self.N
        elif self.direction == 1:    # right
            self.c = (self.c + 1) % self.N
        elif self.direction == 2:    # down
            self.r = (self.r + 1) % self.N
        elif self.direction == 3:    # left
            self.c = (self.c - 1) % self.N

    def update(self):
        """
        Alias for step() to support standard animation.
        """
        self.step()