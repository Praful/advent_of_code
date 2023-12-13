import numpy as np
import os
import sys
from itertools import combinations

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2023/day/11


def read_input(input_file):
    input = read_file_str(input_file, True)

    return input


def solve(input):
    pass


# too slow for part 2
def expand_2D(a, multiple=2):
    # expand row by row

    EMPTY = '.'
    result = None
    for row_index in range(a.shape[0]):
        row = a[row_index, :]

        if result is None:
            result = row
        else:
            result = np.vstack((result, row))

        if all(row == EMPTY):
            for n in range(multiple-1):
                result = np.vstack((result, row))

    return result


def empty_rows_column(a):
    # Return indices of empty rows.
    # For empty column indices, transpose column before calling.
    
    EMPTY = '.'
    empty_rows = []
    for row_index in range(a.shape[0]):
        row = a[row_index, :]

        if all(row == EMPTY):
            empty_rows.append(row_index)

    return np.array(empty_rows)


def galaxy_coords(a):
    GALAXY = '#'
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

    cosmos = to_numpy_array(input)

    rows_expanded = expand_2D(cosmos, multiple)
    cols_expanded = expand_2D(rows_expanded.T, multiple).T

    galaxies = galaxy_coords(cols_expanded)

    return galaxies

def solve(expanded_coords):
    return sum(map(lambda p: manhattan_distance(p[0], p[1]), combinations(expanded_coords, 2)))

def part1(input, multiple=2):
    expanded_coords = expand_galaxy(input, multiple=multiple)
    return solve(expanded_coords)


def part2(input, multiples=2):
    # Work out how many empty rows and columns are before each galaxy. Then expand
    # each galaxy by that amount.
    
    cosmos = to_numpy_array(input)
    galaxies = galaxy_coords(cosmos)
    empty_row_indexes = empty_rows_column(cosmos)
    empty_col_indexes = empty_rows_column(cosmos.T)
    expanded_coords = []

    for (x, y) in galaxies:
        empty_x_count = np.count_nonzero(empty_col_indexes < x)
        empty_y_count = np.count_nonzero(empty_row_indexes < y)

        x1 = x + empty_x_count * (multiples - 1)
        y1 = y + empty_y_count * (multiples - 1)

        expanded_coords.append((x1, y1))

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
