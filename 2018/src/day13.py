import os
from re import I
import sys

sys.path.append(os.path.relpath("../../shared/python"))
import utils
from collections import defaultdict
import numpy as np
from enum import Enum
import copy

# Puzzle description: https://adventofcode.com/2018/day/13


class Direction(Enum):
    RIGHT = '>'
    LEFT = '<'
    DOWN = 'v'
    UP = '^'
    STRAIGHT = '*'

    @classmethod
    def is_valid(cls, s):
        return utils.is_valid(Direction, s)


OFF_TRACK = ' '
MOVE_DELTA = {Direction.DOWN: (0, 1), Direction.LEFT: (-1, 0),
              Direction.RIGHT: (1, 0), Direction.UP: (0, -1)}


class TrackPart(Enum):
    VTRACK = '|'
    HTRACK = '-'
    CORNER1 = '\\'
    CORNER2 = '/'
    INTERSECTION = '+'

    @classmethod
    def is_valid(cls, s):
        return utils.is_valid(TrackPart, s)


class Cart:
    # last junction turn
    def __init__(self, x, y, direction, intersection_direction=Direction.LEFT):
        self.position = (x, y)
        self.direction = direction
        self.intersection_direction = intersection_direction
        self.has_crashed = False

    def __str__(self) -> str:
        return f'Position: {self.position}, direction: {self.direction}, intersection direction: {self.intersection_direction}'

    @classmethod
    def same_position(cls, c1, c2):
        return c1.position == c2.position


# Assumes cart doesn't ever start on corner
def is_corner(grid, x, y):
    return grid[y, x] == TrackPart.CORNER1.value or grid[y, x] == TrackPart.CORNER2.value


# Used to determine which direction a cart goes when at corner
CORNER_DIRECTION = {
    TrackPart.CORNER1: {
        Direction.UP: Direction.LEFT,
        Direction.RIGHT: Direction.DOWN,
        Direction.DOWN: Direction.RIGHT,
        Direction.LEFT: Direction.UP},
    TrackPart.CORNER2: {
        Direction.UP: Direction.RIGHT,
        Direction.RIGHT: Direction.UP,
        Direction.DOWN: Direction.LEFT,
        Direction.LEFT: Direction.DOWN}
}

INTERSECTION_ORDER = [Direction.LEFT, Direction.STRAIGHT, Direction.RIGHT]


# Used to determine which direction a cart goes when at an intersection
INTERSECTION_DIRECTION = {
    Direction.LEFT: {
        Direction.LEFT: Direction.DOWN,
        Direction.RIGHT: Direction.UP,
        Direction.UP: Direction.LEFT,
        Direction.DOWN: Direction.RIGHT
    },
    Direction.RIGHT: {
        Direction.LEFT: Direction.UP,
        Direction.RIGHT: Direction.DOWN,
        Direction.UP: Direction.RIGHT,
        Direction.DOWN: Direction.LEFT
    }
}


def next_direction_from_intersection(cart):
    if cart.intersection_direction == Direction.STRAIGHT:
        direction = cart.direction
    else:
        direction = INTERSECTION_DIRECTION[cart.intersection_direction][cart.direction]

    # cycle through the three options in order, looping back after last option
    next_int_direction = INTERSECTION_ORDER[(INTERSECTION_ORDER.index(
        cart.intersection_direction) + 1) % len(INTERSECTION_ORDER)]

    return direction, next_int_direction


def move_cart(grid, cart):
    xy_delta = MOVE_DELTA[cart.direction]
    x = cart.position[0] + xy_delta[0]
    y = cart.position[1] + xy_delta[1]
    track = grid[y, x]
    direction = cart.direction
    int_direction = cart.intersection_direction

    if is_corner(grid, x, y):
        direction = CORNER_DIRECTION[TrackPart(track)][cart.direction]
    elif track == TrackPart.INTERSECTION.value:
        direction, int_direction = next_direction_from_intersection(cart)

    cart.position = (x, y)
    cart.direction = direction
    cart.intersection_direction = int_direction

    return


def crash(carts, cart):
    result = False
    for c in carts:
        if c != cart and (not c.has_crashed) and Cart.same_position(cart, c):
            result = True
            c.has_crashed = True

    return result


def solve(grid, carts, exit_on_first_crash=True):

    moving_carts = copy.deepcopy(carts)
    moves = 0
    while True:
        # sort carts by row then col
        carts = sorted(moving_carts, key=lambda c: (
            c.position[1], c.position[0]))
        # grid_copy = np.copy(grid)

        for c in carts:
            if not c.has_crashed:
                move_cart(grid, c)
                if crash(carts, c):
                    if exit_on_first_crash:
                        return c.position
                    else:
                        c.has_crashed = True

                # grid_copy[c.position[1], c.position[0]] = c.direction.value

        active_carts = [c for c in carts if not c.has_crashed]
        if len(active_carts) == 1:
            return active_carts[0].position

        # print_grid(grid_copy)

    return None


def print_grid(grid): [print(''.join(l)) for l in grid]


def test(grid):
    # print('>'==Direction.RIGHT.value)

    # [print(l.value) for l in list(Track)]
    # print(Track.is_valid('|'))
    # print(Track.is_valid('r'))
    # print(Direction.is_valid('^'))
    # print(Direction.is_valid('v'))

    # for y in range(0, grid.shape[0]):
    # for x in range(0, grid.shape[1]):
    # if Direction.is_valid(grid[y, x]):
    h, w = grid.shape
    [print(x, y, grid[y, x]) for y in range(h)
     for x in range(w) if is_corner(grid, x, y)]


def read_input(input_file):
    input = utils.read_file_str(input_file)
    carts = []
    grid = np.full((len(input), len(input[1])), OFF_TRACK, dtype=str)
    for y, row in enumerate(input):
        for x, col in enumerate(row.strip('\n')):
            grid[y, x] = col
            if Direction.is_valid(col):
                carts.append(Cart(x, y, Direction(col)))

    # test(grid)

    # print_grid(grid)
    # utils.print_np_info(grid)

    return grid, carts


def main():
    main_grid, main_carts = read_input("../data/day13.txt")
    test_grid, test_carts = read_input("../data/day13-test.txt")
    test_grid2, test_carts2 = read_input("../data/day13-test2.txt")

    # print(f'Part 1 (test) {solve(test_grid, test_carts)}')  # 7, 3
    print(f'Part 1 {solve(main_grid, main_carts)}')  # 103,85
    # print(f'Part 2 (test2) {solve(test_grid2, test_carts2, False)}')  # 6,4
    print(f'Part 2 {solve(main_grid, main_carts, False)}')  # 88, 64


if __name__ == '__main__':
    main()
