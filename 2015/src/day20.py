import sys
import os
import math
from collections import defaultdict

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2015/day/20

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None

TARGET = 34000000
VISIT = 50

# there's nothing special about this number; I started low and
# increased until I got a result
BIG_NUMBER = 1000000


def read_input(input_file):
    input = read_file_str(input_file, True)
    return input


def part1(target):
    houses = defaultdict(int)
    lowest = math.inf

    for elf in range(1, BIG_NUMBER):
        for house in range(elf, BIG_NUMBER, elf):
            houses[house] += elf * 10
            if houses[house] >= target:
                lowest = min(lowest, house)

    return lowest


def part2(target):
    houses = defaultdict(int)
    lowest = math.inf
    for elf in range(1, BIG_NUMBER):
        for house in range(elf, (VISIT+1)*elf, elf):
            houses[house] += elf * 11
            if houses[house] >= target:
                lowest = min(lowest, house)

    return lowest


# this brute force solution takes about 40s on 6th gen (i7-6500U) laptop
def main():
    print(f'Part 1 {part1(TARGET)}')  # 786240
    print(f'Part 2 {part2(TARGET)}')  # 831600


if __name__ == '__main__':
    main()
