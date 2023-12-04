import re
from dataclasses import dataclass
from collections import defaultdict
import os
import sys

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2023/day/03


@dataclass
class Symbol:
    x: int
    y: int
    value: str

    def is_gear(self): return self.value == '*'

    def __hash__(self):
        return hash((self.x, self.y, self.value))


def read_input(input_file):
    input = read_file_str(input_file, True)
    return input


def nearby_symbols(input, y_part, x_part_start, x_part_end):
    def is_in_grid(x, y): return 0 <= y < len(input) and 0 <= x < len(input[y])

    def is_symbol(x, y):
        if is_in_grid(x, y):
            c = input[y][x]
            return not c.isnumeric() and c != '.'
        return False

    # look around part number for symbols
    result = []
    for y in range(y_part - 1, y_part + 2):
        for x in range(x_part_start - 1, x_part_end + 1):
            if is_symbol(x, y):
                result.append(Symbol(x, y, input[y][x]))
    return result


def solve(input):
    part1_result = 0
    number_symbol_map = defaultdict(list)

    for y, line in enumerate(input):
        for match in re.finditer(r'\d+', line):
            part_number = int(match.group())
            symbols = nearby_symbols(input, y, match.start(), match.end())
            if len(symbols) > 0:
                part1_result += part_number
                for symbol in symbols:
                    if symbol.is_gear():
                        number_symbol_map[symbol].append(part_number)

    part2_result = sum(part_numbers[0] * part_numbers[1]
                       for part_numbers in number_symbol_map.values() if len(part_numbers) == 2)

    return (part1_result, part2_result)


def main():
    input = read_input("../data/day03.txt")
    test_input = read_input("../data/day03-test.txt")

    print(f'Part 1 and 2 test {solve(test_input)}')  # 4361, 467835
    print(f'Part 1 and 2 {solve(input)}')  # 546312, 87449461


if __name__ == '__main__':
    main()
