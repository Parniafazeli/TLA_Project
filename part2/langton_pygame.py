# -*- coding: utf-8 -*-

import argparse
import pygame

from langton import LangtonsAnt


DEFAULT_RULES = {
    0: (1, "R"),
    1: (0, "L"),
}

MULTI_COLOR_RULES = {
    0: (1, "R"),
    1: (2, "L"),
    2: (3, "R"),
    3: (0, "L"),
}

PALETTE = [
    (0, 0, 0),
    (240, 240, 240),
    (77, 166, 255),
    (255, 130, 67),
    (134, 199, 86),
    (186, 112, 255),
    (255, 207, 64),
    (80, 214, 193),
]


def draw_grid(board, cell_size, ant_pos=None, ant_color=(220, 40, 40)):
    rows, cols = board.shape
    surface = pygame.Surface((cols * cell_size, rows * cell_size))

    for row in range(rows):
        for col in range(cols):
            color = PALETTE[int(board[row, col]) % len(PALETTE)]
            pygame.draw.rect(
                surface,
                color,
                pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size),
            )

    if ant_pos is not None:
        row, col = ant_pos
        center = (
            col * cell_size + cell_size // 2,
            row * cell_size + cell_size // 2,
        )
        pygame.draw.circle(surface, ant_color, center, max(2, cell_size // 3))

    return surface


def run_simulation(ant, cell_size=6, fps=60, max_steps=None, title="Langton's Ant"):
    pygame.init()

    board = ant.get_grid()

    screen = pygame.display.set_mode(
        (board.shape[1] * cell_size, board.shape[0] * cell_size)
    )

    pygame.display.set_caption(title)

    clock = pygame.time.Clock()

    running = True
    steps = 0

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        surface = draw_grid(board, cell_size, ant.get_position())
        screen.blit(surface, (0, 0))
        pygame.display.flip()

        ant.move()
        board = ant.get_grid()

        steps += 1

        if max_steps is not None and steps >= max_steps:
            running = False

        clock.tick(fps)

    pygame.quit()


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--size", type=int, default=200)
    parser.add_argument("--row", type=int, default=None)
    parser.add_argument("--col", type=int, default=None)
    parser.add_argument("--cell-scale", type=int, default=6)
    parser.add_argument("--fps", type=int, default=60)
    parser.add_argument("--steps", type=int, default=None)

    parser.add_argument(
        "--multi-color",
        action="store_true",
    )

    return parser.parse_args()


def main():
    args = get_args()

    start_row = args.row if args.row is not None else args.size // 2
    start_col = args.col if args.col is not None else args.size // 2

    rules = MULTI_COLOR_RULES if args.multi_color else DEFAULT_RULES

    ant = LangtonsAnt(args.size, (start_row, start_col), rules)

    run_simulation(
        ant,
        cell_size=args.cell_scale,
        fps=args.fps,
        max_steps=args.steps,
        title="Langton's Ant",
    )


if __name__ == "__main__":
    main()