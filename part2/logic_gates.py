# -*- coding: utf-8 -*-
"""
Glider-based Logic Gates Student Template Module.

"""

from conway import GameOfLife


class GliderLogicGates:

    def setup_and_gate(self, grid_size=35, input_a_present=False, input_b_present=False):

        g_Size = max(grid_size, 35)
        game=GameOfLife(g_Size, finite=True, fastMode=True)
        # Standard glider patterns
        glider_A = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        glider_B = [(0, 1), (1, 0), (2, 0), (2, 1), (2, 2)]
        #Standard Eater 1 patterns
        eater_a = [(0, 0), (0, 1), (1, 0), (1, 2), (2, 2), (3, 2), (3, 3)]
        eater_b = [(0, 2), (0, 3), (1, 1), (1, 3), (2, 1), (3, 0), (3, 1)]

        #Place eaters for glider A,B
        eater_a_row, eater_a_col = 23, 21
        for r, c in eater_a:
            game.grid[eater_a_row + r, eater_a_col + c] = 1

        eater_b_row, eater_b_col = 20, 3
        for r, c in eater_b:
            game.grid[eater_b_row + r, eater_b_col + c] = 1

        if input_a_present:
            #Place input A glider
            A_row, A_col = 10, 8
            for r, c in glider_A:
                game.grid[A_row + r, A_col + c] = 1
 
        if input_b_present:
            # Place input B glider
            B_row, B_col = 7, 17
            for r, c in glider_B:
                game.grid[B_row + r, B_col + c] = 1
 
        return game

    def setup_not_gate(self, grid_size=35, input_a_present=False):

        g_Size = max(grid_size, 35)
        game = GameOfLife(g_Size, finite=True, fastMode=True)

        control_glider = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        c_row, c_col = 2, 2
        for r, c in control_glider:
            game.grid[c_row + r, c_col + c] = 1

        if input_a_present:
            # Glider used to cancel the control glider
            cancel_glider = [(2, 1), (1, 0), (0, 2), (0, 1), (0, 0)]
            cancel_row = c_row + 8
            cancel_col = c_col + 8
            for r, c in cancel_glider:
                game.grid[cancel_row + r, cancel_col + c] = 1
 
        return game

    def run_and_gate(self, input_a_present, input_b_present):
               
        game = self.setup_and_gate(input_a_present=input_a_present,input_b_present=input_b_present)
        #run simulation
        for _ in range(100):
            game.evolve()
        #Check if the output block exists
        region = game.grid[15:17, 12:14]
        return bool(region.all())

    def run_not_gate(self, input_a_present):
        game = self.setup_not_gate(input_a_present=input_a_present)
 
        # run simulation
        for _ in range(80):
            game.evolve()
        region = game.grid[20:28, 20:28]

        return bool(region.sum() > 0)
 