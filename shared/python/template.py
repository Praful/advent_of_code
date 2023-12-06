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
from functools import reduce
from itertools import product
from operator import mul

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2022/day/XX


def read_input(input_file):
    input = read_file_str(input_file, True)
    return input


def solve(input):
    pass


def part1(input):
    result = 0
    print(input)
    return result


def part2(input):
    result = 0
    return result


def main():
    # input = read_input("../data/dayXX.txt")
    test_input = read_input("../data/dayXX-test.txt")

    assert (res := part1(test_input)) == 0, f'Actual: {res}'

    # print(f'Part 1 (test) {part1(test_input)}')  #
    # print(f'Part 1 {part1(input)}')  #

    #  assert (res := part2(test_input)) == 0, f'Actual: {res}'

    # print(f'Part 2 (test) {part2(test_input)}')  #
    # print(f'Part 2 {part2(input)}')  #


if __name__ == '__main__':
    main()
