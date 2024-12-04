import sys
import os

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2024/day/4


def read_input(input_file):
    input = read_file_str(input_file, True)
    return input


def part1(input):
    result = 0
    FIND = "XMAS"

    for r, row in enumerate(input):
        for c, _ in enumerate(row):
            for p in DIRECTIONS_ALL:
                found = True
                current_point = (r, c)
                for letter in FIND:
                    if not in_grid(current_point, input) or \
                            input[current_point[0]][current_point[1]] != letter:
                        found = False
                        break

                    current_point = (
                        current_point[0] + p[0], current_point[1] + p[1])

                if found:
                    result += 1

    return result


def part2(input):
    result = 0
    FIND = "MS"

    # we're looking for A's then checking diagonals are M or S so that
    # diagonal spells MAS or SAM
    def is_diagonal(char1, char2):
        return char1 in FIND and char2 in FIND and char1 != char2

    for r, row in enumerate(input):
        for c, _ in enumerate(row):
            if row[c] == "A":
                # relative to "A": top left (0), top right (1), bottom left (2), bottom right (3)
                corners = [(r-1, c-1), (r-1, c+1), (r+1, c-1), (r+1, c+1)]

                if all(in_grid(p, input) for p in corners):
                    corner_letters = [input[a][b] for a, b in corners]
                    if is_diagonal(corner_letters[0], corner_letters[3]) and \
                            is_diagonal(corner_letters[1], corner_letters[2]):
                        result += 1

    return result


def main():
    input = read_input("../data/day04.txt")
    test_input = read_input("../data/day04-test.txt")

    assert (res := part1(test_input)) == 18, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 2401

    assert (res := part2(test_input)) == 9, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 1822


if __name__ == '__main__':
    main()
