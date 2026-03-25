# StringRay1024;
import sys
import os
import queue

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2022/day/24

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None

WALL = '#'
GROUND = '.'

BLIZZARDS = ARROWS_TO_DIRECTION2.keys()


class Blizzard():
    def __init__(self, direction, position):
        self._direction = direction
        self._position = position

    @property
    def direction(self):
        return self._direction

    @property
    def position(self):
        return self._position

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'{self.direction}: {self.position}'

    def __eq__(self, other):
        if not isinstance(other, Blizzard):
            return False

        return self.direction == other.direction and self.position == other.position

    @staticmethod
    def list_match(b1, b2):
        return not any(e1 != e2 for e1, e2 in zip(b1, b2))

    @staticmethod
    def list_print(b):
        for e in b:
            print(e)

    @staticmethod
    # move all blizzards in grid once
    def next_blizzards(grid, blizzard_pos):
        W, L = len(grid[0]), len(grid)
        result = []

        for b in blizzard_pos:
            new_pos = add_pos(b.position, ARROWS_TO_DIRECTION2[b.direction])
            if new_pos[0] == 0:
                new_pos = (L - 2, new_pos[1])
            elif new_pos[0] == L - 1:
                new_pos = (1, new_pos[1])

            if new_pos[1] == 0:
                new_pos = (new_pos[0], W - 2)
            elif new_pos[1] == W - 1:
                new_pos = (new_pos[0], 1)

            result.append(Blizzard(b.direction, new_pos))

        return result


def find_opening(row):
    for i, c in enumerate(row):
        if c != WALL:
            return i


def read_input(input_file):
    grid = read_file_str(input_file, True)
    start = (0, find_opening(grid[0]))
    end = (len(grid) - 1, find_opening(grid[-1]))

    blizzard_pos = []

    for r, v in enumerate(grid):
        for c, v2 in enumerate(v):
            if v2 in BLIZZARDS:
                blizzard_pos.append(Blizzard(v2, (r, c)))

    all_blizzard_moves = find_all_blizzard_moves(grid, blizzard_pos)
    return grid, start, end, all_blizzard_moves


# these are all the positions of the blizzards after each move
def find_all_blizzard_moves(grid, initial):
    b = initial
    result = []
    while True:
        new_b = Blizzard.next_blizzards(grid, b)
        result.append(set(p.position for p in new_b))
        # check for cycle
        if Blizzard.list_match(initial, new_b):
            break
        b = new_b

    return result


def is_wall(grid, p):
    return tile(grid, p) == WALL


def solve(input, start_t=0):
    def not_wall(g, x): return tile(g, x) != WALL

    grid, start, end, all_blizzard_moves = input

    q = queue.SimpleQueue()
    q.put((start, start_t))
    visited = set()

    num_states = len(all_blizzard_moves)

    # bfs
    while not q.empty():
        p, t = q.get()

        blizzard_list_id = t % num_states
        blizzard_list = all_blizzard_moves[blizzard_list_id]

        if (p, blizzard_list_id) not in visited:
            visited.add((p, blizzard_list_id))

            if p == end:
                return t - start_t

            # wait
            if p not in blizzard_list:
                q.put((p, t+1))

            # try moving
            for adj in neighbours(p, grid, condition=not_wall):
                if adj not in blizzard_list:
                    q.put((adj, t+1))

    return 0


def part1(input):
    grid, start, end, all_blizzards = input
    return solve((grid, start, end, all_blizzards))


def part2(input):
    grid, start, end, all_blizzards = input
    t1 = solve((grid, start, end, all_blizzards))
    t2 = solve((grid, end, start, all_blizzards), t1)
    t3 = solve((grid, start, end, all_blizzards), t1 + t2)
    return t1 + t2 + t3


def main():
    input = read_input("../data/day24.txt")
    #  test_input = read_input("../data/day24-test.txt")
    test_input2 = read_input("../data/day24-test2.txt")

    #  assert (res := part1(test_input)) == 0, f'Actual: {res}'
    assert (res := part1(test_input2)) == 18, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 332

    assert (res := part2(test_input2)) == 54, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 942


if __name__ == '__main__':
    main()
