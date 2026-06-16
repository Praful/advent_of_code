import sys
import os
import re

from collections import namedtuple

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2016/day/8

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None

# if Instruction is rect, arg1 is width (columns), arg2 is height (rows)
# if Instruction is rotate_row, arg1 is row, arg2 is shift
# if Instruction is rotate_column, arg1 is column, arg2 is shift
Instruction = namedtuple('Instruction', ['op', 'arg1', 'arg2'])


class RotatableGrid:
    # Initialize with a 2D list (list of lists).
    def __init__(self, data):

        if not data or not all(len(row) == len(data[0]) for row in data):
            raise ValueError("Data must be a non-empty rectangular 2D list.")
        # Create a deep copy to avoid modifying the original list
        self.grid = [row[:] for row in data]
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

    # Rotate a specific row horizontally.
    # Positive shifts move elements to the right (wraparound to start).
    # Negative shifts move elements to the left.
    def rotate_row(self, row_index, shifts):
        if not 0 <= row_index < self.rows:
            raise IndexError(f"Row index {row_index} out of range.")

        shifts %= self.cols  # Handle shifts larger than row length
        if shifts == 0:
            return

        # use list slicing to handle the wraparound
        row = self.grid[row_index]
        self.grid[row_index] = row[-shifts:] + row[:-shifts]

    # Rotate a specific column vertically.
    # Positive shifts move elements down (wraparound to top).
    # Negative shifts move elements up.
    def rotate_col(self, col_index, shifts):
        if not 0 <= col_index < self.cols:
            raise IndexError(f"Column index {col_index} out of range.")

        shifts %= self.rows  # Handle shifts larger than column length
        if shifts == 0:
            return

        # extract column
        col = [self.grid[r][col_index] for r in range(self.rows)]

        # rotate the 1D column list
        rotated_col = col[-shifts:] + col[:-shifts]

        # put it back
        for r in range(self.rows):
            self.grid[r][col_index] = rotated_col[r]

    # fill from (0,0) to (width-1, height-1) with value
    def fill_rect(self, width, height, value=True):
        for r in range(height):
            for c in range(width):
                self.grid[r][c] = value

    # return the current state of the grid
    def get_grid(self):
        return [row[:] for row in self.grid]

    # print the grid
    def __str__(self):
        return "\n".join(str(row) for row in self.grid)


def test_rotatable_grid():
    data = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12]
    ]

    grid = RotatableGrid(data)

    print("Original:")
    print(grid)

    # Rotate Row 1 (middle row) to the right by 1
    # [5, 6, 7, 8] becomes [8, 5, 6, 7]
    grid.rotate_row(1, 1)
    print("\nAfter rotating Row 1 right by 1:")
    print(grid)

    # Rotate column 2 (index 2) down by 1
    # The column was [3, 6, 11] but row 1 changed previously.
    # So current column 2 is: 3, 7, 11. Rotating down by 1: [11, 3, 7]
    grid.rotate_col(2, 1)
    print("\nAfter rotating Col 2 down by 1:")
    print(grid)

    grid = RotatableGrid(data)
    print("-" * 20)
    print("Original:")
    print(grid)

    # Rotate row 2 left by 1
    # The row [9, 10, 11, 12] becomes [10, 11, 12, 9]
    grid.rotate_row(2, -1)
    print("\nAfter rotating Row 2 left by 1:")
    print(grid)

    # Rotate column 1 up by 1
    # The column [2, 6, 11] becomes [6, 11, 2]
    grid.rotate_col(1, -1)
    print("\nAfter rotating Col 1 up by 1:")
    print(grid)


def parse_instruction(line):
    if "rect" in line:
        return Instruction("rect", *map(int, re.findall(r'\d+', line)))
    elif "rotate row" in line:
        return Instruction("rotate_row", *map(int, re.findall(r'\d+', line)))
    elif "rotate column" in line:
        return Instruction("rotate_column", *map(int, re.findall(r'\d+', line)))
    else:
        raise ValueError


def read_input(input_file):
    return list(map(parse_instruction, read_file_str(input_file, True)))

#  def print_grid(screen):
    #  print("\n".join("".join("#" if v else "." for v in row) for row in screen))


def solve(input, num_rows, num_cols, part2=False):
    screen = RotatableGrid(make_grid(num_rows, num_cols, False))

    for instr in input:
        if instr.op == "rect":
            screen.fill_rect(instr.arg1, instr.arg2)
        elif instr.op == "rotate_row":
            screen.rotate_row(instr.arg1, instr.arg2)
        elif instr.op == "rotate_column":
            screen.rotate_col(instr.arg1, instr.arg2)
        else:
            raise ValueError

    if part2:
        grid = screen.get_grid()
        for row in grid:
            print("".join(BLOCK if v else " " for v in row))

    return sum(map(sum, screen.get_grid()))


def main():
    #  test_rotatable_grid()

    input = read_input("../data/day08.txt")
    test_input = read_input("../data/day08-test.txt")

    assert (res := solve(test_input, 3, 7)) == 6, f'Actual: {res}'
    print(f'Part 1 {solve(input, 6, 50, True)}')  # 110, ZJHRKCPLYJ


if __name__ == '__main__':
    main()
