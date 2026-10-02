import collections
import copy
import functools
import itertools
import math
import operator
import os
import queue
import re
import sys
from collections import defaultdict, namedtuple

# for profiling
from cProfile import Profile
from dataclasses import dataclass
from functools import lru_cache, reduce
from itertools import product
from operator import mul
from pprint import pprint
from pstats import SortKey, Stats
from queue import SimpleQueue

import numpy as np

from utils import aoc_input_file, read_file_str

# Puzzle description: https://adventofcode.com/2024/day/XX

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    input = read_file_str(aoc_input_file(__file__, input_file), True)
    return input


def part1(input):
    result = 0
    pprint(input)
    return result


def part2(input):
    result = 0
    return result


def main():
    # input = read_input("dayXX.txt")
    test_input = read_input("dayXX-test.txt")

    assert (res := part1(test_input)) == 0, f"Actual: {res}"
    # print(f'Part 1 {part1(input)}')  #

    #  assert (res := part2(test_input)) == 0, f'Actual: {res}'
    # print(f'Part 2 {part2(input)}')  #


if __name__ == "__main__":
    #  sys.setrecursionlimit(999999)

    main()

    #  with Profile() as profile:
    #
    #  main()
    #  (
    #  Stats(profile)
    #  .strip_dirs()
    #  .sort_stats(SortKey.TIME)
    #  .print_stats()
    #  )
