import numpy as np
import os
import sys
from itertools import combinations

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2023/day/11


GALAXY = '#'
EMPTY = '.'


def read_input(input_file):
    return to_numpy_array(read_file_str(input_file, True))


def expand_2D(a, multiple=2):
    # add rows to cosmos map
    # too slow for part 2

    result = None
    for row_index in range(a.shape[0]):
        row = a[row_index, :]

        if result is None:
            result = row
        else:
            result = np.vstack((result, row))

        if all(row == EMPTY):
            for _ in range(multiple-1):
                result = np.vstack((result, row))

    return result


def empty_rows_column(a):
    # Return indices of empty rows.
    # For empty column indices, transpose column before calling.

    empty_rows = []
    for row_index in range(a.shape[0]):
        row = a[row_index, :]

        if all(row == EMPTY):
            empty_rows.append(row_index)

    return np.array(empty_rows)


def galaxy_coords(a):
    galaxies = []
    for y in range(a.shape[0]):
        for x in range(a.shape[1]):
            if a[y, x] == GALAXY:
                galaxies.append((x, y))

    return galaxies


def to_numpy_array(a):
    rows = [list(l) for l in a]
    return np.array(rows, str)


# Too slow for part 2
def expand_galaxy(input, multiple=2):
    rows_expanded = expand_2D(input, multiple)
    cols_expanded = expand_2D(rows_expanded.T, multiple).T
    return galaxy_coords(cols_expanded)


def solve(expanded_coords):
    return sum(map(lambda p: manhattan_distance(p[0], p[1]), combinations(expanded_coords, 2)))


def part1(input, multiple=2):
    expanded_coords = expand_galaxy(input, multiple=multiple)
    return solve(expanded_coords)


def part2(input, multiples=2):
    # Work out how many empty rows and columns are before each galaxy. Then expand
    # each galaxy's coordinates by that amount.

    def new_coord(p):
        # calc expanded coordinate for p

        x, y = p
        empty_col_count = np.count_nonzero(empty_col_indexes < x)
        empty_row_count = np.count_nonzero(empty_row_indexes < y)

        x1 = x + empty_col_count * (multiples - 1)
        y1 = y + empty_row_count * (multiples - 1)

        return x1, y1

    empty_row_indexes = empty_rows_column(input)
    empty_col_indexes = empty_rows_column(input.T)
    expanded_coords = list(map(new_coord, galaxy_coords(input)))
    return solve(expanded_coords)


def main():
    input = read_input("../data/day11.txt")
    test_input1 = read_input("../data/day11-test-1.txt")
    #  test_input2 = read_input("../data/day11-test-1-expanded.txt")

    assert (res := part1(test_input1)) == 374, f'Actual: {res}'
    #  assert (res := part1(test_input2)) == 374, f'Actual: {res}' # expanded already

    print(f'Part 1 {part1(input)}')  # 9545480

    assert (res := part1(test_input1, 10)) == 1030, f'Actual: {res}'
    assert (res := part2(test_input1, 10)) == 1030, f'Actual: {res}'
    assert (res := part1(test_input1, 100)) == 8410, f'Actual: {res}'
    assert (res := part2(test_input1, 100)) == 8410, f'Actual: {res}'

    print(f'Part 2 {part2(input, 1_000_000)}')  # 406725732046


if __name__ == '__main__':
    main()
