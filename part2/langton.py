# -*- coding: utf-8 -*-

import numpy as np


class LangtonsAnt:

    def __init__(self, size, start_position, rule_set):
        self.size = size
        self.board = np.zeros((size, size), dtype=np.int32)

        self.row, self.col = start_position

        self.direction = 0
        self.rule_set = rule_set

    def get_grid(self):
        return self.board

    def get_position(self):
        return (self.row, self.col)

    def move(self):
        current_state = int(self.board[self.row, self.col])

        if current_state in self.rule_set:
            new_state, turn_dir = self.rule_set[current_state]
        else:
            new_state = current_state
            turn_dir = "R"

        self.board[self.row, self.col] = new_state

        if turn_dir == "R":
            self.direction = (self.direction + 1) % 4
        elif turn_dir == "L":
            self.direction = (self.direction - 1) % 4

        if self.direction == 0:
            self.row = (self.row - 1) % self.size

        elif self.direction == 1:
            self.col = (self.col + 1) % self.size

        elif self.direction == 2:
            self.row = (self.row + 1) % self.size

        else:
            self.col = (self.col - 1) % self.size

    def next_step(self):
        self.move()