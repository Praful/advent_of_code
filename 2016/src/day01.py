import sys
import os

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2016/day/1

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    input = read_file_str(input_file, True)
    return input[0].split(', ')


def solve(input, part2=False):
    dir = Direction.NORTH
    pos = (0, 0)
    visited = set()
    found = False

    for move in input:
        dir = rotate_direction(dir, move[0] == "R")

        blocks = int(move[1:])
        for _ in range(blocks):
            pos = add_pos(pos, DIRECTION_DELTAS[dir])
            if part2:
                if pos in visited:
                    found = True
                    break
                else:
                    visited.add(pos)

        if found:
            break

    return manhattan_distance((0, 0), pos)


def main():
    input = read_input("../data/day01.txt")

    assert (res := solve(["R2", "L3"])) == 5, f'Actual: {res}'
    assert (res := solve(["R2", "R2", "R2"])) == 2, f'Actual: {res}'
    assert (res := solve(["R5", "L5", "R5", "R3"])) == 12, f'Actual: {res}'
    print(f'Part 1 {solve(input)}')  # 298

    assert (res := solve(["R8", "R4", "R4", "R8"], True)) == 4, f'Actual: {res}'
    print(f'Part 2 {solve(input, True)}')  # 158


if __name__ == '__main__':
    main()
