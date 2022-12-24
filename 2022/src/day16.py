import os
import sys
sys.path.append(os.path.relpath("../../shared/python"))
from utils import *
from pprint import pprint
from dataclasses import dataclass
from collections import defaultdict
import math
import numpy as np
import operator
import copy
import re

# Puzzle description: https://adventofcode.com/2022/day/16


@dataclass
class Valve:
    id: str
    flow_rate: int
    leads_to: list
    is_open: bool = False
    minute_opened: int = 0


def read_input(input_file):
    valves = {}
    for l in read_file_str(input_file, True):
        match = re.search(
            r'^Valve (..) has flow rate=(\d*).* valves? (.*)$', l)
        if match:
            # print(match.group(0))
            id = match.group(1)
            valves[id] = Valve(id, int(match.group(2)),
                               match.group(3).split(', '))

    return valves


def solve(input):
    pass


def part1(input):
    result = 0
    pprint(input)
    return result


def part2(input):
    result = 0
    return result


def main():
    # input = read_input("../data/day16.txt")
    test_input = read_input("../data/day16-test.txt")

    assert (res := part1(test_input)) == 0, f'Actual: {res}'
    # print(f'Part 1 (test) {part1(test_input)}')  #
    # print(f'Part 1 {part1(input)}')  #

    assert (res := part2(test_input)) == 0, f'Actual: {res}'
    # print(f'Part 2 (test) {part2(test_input)}')  #
    # print(f'Part 2 {part2(input)}')  #


if __name__ == '__main__':
    main()
