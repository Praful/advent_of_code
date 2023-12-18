import numpy as np
import os
import sys

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2023/day/13


def read_input(input_file):
    with open(input_file) as f:
        input = [l.strip().split('\n') for l in f.read().split('\n\n')]

    return input


def mirrored_lines(terrain, part2=False):
    result = {}

    row_count = terrain.shape[0]
    col_count = terrain.shape[1]

    for mirror_row in range(1, row_count):
        mirrored_count = 0  # no of mirrored items for mirror located above row
        smudge_count = 0
        for row in range(mirror_row):
            target_row = abs(row - (mirror_row - 1)) + mirror_row
            if target_row < row_count:
                same_count = np.count_nonzero(terrain[row] == terrain[target_row])
                mirrored_count += same_count
                smudge_count += col_count - same_count

        if (not part2 and smudge_count == 0) or (part2 and smudge_count == 1):
            result[mirror_row] = mirrored_count

    return result


def solve(input, part2=False):
    result = 0

    for terrain in input:
        a = to_numpy_array(terrain)
        horiz_sym = mirrored_lines(a, part2)
        vert_sym = mirrored_lines(a.T, part2)

        horiz_max_key = horiz_max_value = vert_max_key = vert_max_value = 0

        # in case there are multiple lines of symmetry, choose the one with
        # most reflected objects
        if horiz_sym:
            horiz_max_key, horiz_max_value = max(
                horiz_sym.items(), key=lambda x: x[1])
        if vert_sym:
            vert_max_key, vert_max_value = max(
                vert_sym.items(), key=lambda x: x[1])

        if horiz_max_value > vert_max_value:
            result += horiz_max_key * 100
        else:
            result += vert_max_key

    return result


def main():
    input = read_input("../data/day13.txt")
    test_input = read_input("../data/day13-test.txt")

    assert (res := solve(test_input)) == 405, f'Actual: {res}'
    print(f'Part 1 {solve(input)}')  # 31265

    assert (res := solve(test_input, True)) == 400, f'Actual: {res}'
    print(f'Part 2 {solve(input, True)}')  # 39359


if __name__ == '__main__':
    main()
