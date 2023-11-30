import re
import copy
import operator
import numpy as np
import math
from collections import defaultdict
from dataclasses import dataclass
from pprint import pprint
import os
import sys
sys.path.append(os.path.relpath("../../shared/python"))

from utils import *  # noqa: E402
# Puzzle description: https://adventofcode.com/2022/day/XX


def read_input(input_file):
    input = read_file_str(input_file, True)
    return input[0]


def move(x, y, dir):
    if dir == ">":
        x += 1
    elif dir == "<":
        x -= 1
    elif dir == "^":
        y += 1
    elif dir == "v":
        y -= 1
    return x, y


def part1(input):
    if len(input) == 1:
        return 2

    visited = {}
    x = y = 0

    for direction in input:
        x, y = move(x, y, direction)
        if (x, y) in visited:
            visited[(x, y)] += 1
        else:
            visited[(x, y)] = 1

    #  print(visited)
    return len(visited)


def part2(input):

    visited = {(0, 0): 1}
    coords = [(0, 0), (0, 0)]
    person = 0  # 0=santa, 1=robo-santa

    for direction in input:
        x, y = move(coords[person][0], coords[person][1],  direction)
        if (x, y) in visited:
            visited[(x, y)] += 1
        else:
            visited[(x, y)] = 1

        coords[person] = (x, y)

        # flip 0 to 1 or 1 to 0 since we're alternating between santa and robo-santa
        person ^= 1

    #  print(visited)
    return len(visited)


def main():
    input = read_input("../data/day03.txt")

    assert (res := part1('>')) == 2, f'Actual: {res}'
    assert (res := part1('^>v<')) == 4, f'Actual: {res}'
    assert (res := part1('^v^v^v^v^v')) == 2, f'Actual: {res}'

    print(f'Part 1 {part1(input)}')  # 2572

    assert (res := part2('^v')) == 3, f'Actual: {res}'
    assert (res := part2('^>v<')) == 3, f'Actual: {res}'
    assert (res := part2('^v^v^v^v^v')) == 11, f'Actual: {res}'

    print(f'Part 2 {part2(input)}')  # 2631


if __name__ == '__main__':
    main()
