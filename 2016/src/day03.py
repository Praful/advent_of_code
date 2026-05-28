import sys
import os

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2016/day/3

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    def parse(s):
        return list(map(int, s.split()))

    input = map(parse, read_file_str(input_file, True))
    return list(input)


def possible_triangle(sides):
    return sides[0] + sides[1] > sides[2] and \
        sides[1] + sides[2] > sides[0] and \
        sides[2] + sides[0] > sides[1]


def part1(input):
    result = 0
    for row in input:
        if possible_triangle(row):
            result += 1

    return result


def part2(input):
    result = 0

    for i in range(0, len(input), 3):
        for j in range(3):
            sides = [input[i][j], input[i + 1][j], input[i + 2][j]]
            if possible_triangle(sides):
                result += 1

    return result


def main():
    input = read_input("../data/day03.txt")

    print(f'Part 1 {part1(input)}')  # 983
    print(f'Part 2 {part2(input)}')  # 1836


if __name__ == '__main__':
    main()
