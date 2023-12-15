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
from functools import lru_cache
from itertools import combinations_with_replacement
from itertools import permutations
from operator import mul

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2023/day/12


def read_input(input_file):
    result = []
    for line in read_file_str(input_file, True):
        records, damages = line.split()
        result.append((records, tuple(map(int, damages.split(",")))))

    return result


def possible_matches(s):
    x = s.count('?')
    comb = product('.#', repeat=x)
    result = []
    for filler in comb:
        n = s
        for c in filler:
            n = n.replace('?', c, 1)
        result.append(n)

    return result


REGEX_TEMPLATE = r'^[\.]*%s[\.]*$'
REGEX_DAMAGES = r'[\#]{%i}'


def make_regex(damages):
    result = r''
    damage_count = len(damages)
    for i, n in enumerate(damages):
        result += REGEX_DAMAGES % n
        if i < damage_count - 1:
            result += r'[\.]+'

    return re.compile(REGEX_TEMPLATE % result)


# Part 1 using brute force and regex; too slow for part 2.
def matches1(record, damages):
    count = 0
    regex = make_regex(damages)
    for poss in possible_matches(record):
        res = re.findall(regex, poss)
        if len(res) == 1:
            count += 1

    return count


def unfold(input):
    result = []
    for record, damages in input:
        new_record = (record+'?') * 5
        new_damage = (damages) * 5
        result.append((new_record[:-1], new_damage))

    return result


@lru_cache(maxsize=256)
def matches2(record, damages):
    # Part 2 fast method using recursion and cache (memoization).

    def more_damaged_springs(): return len(damages) > 1

    def found_damaged_springs():
        return re.findall(r'^[\#\?]{%i}' % damages[0], record)

    def valid_next_spring(): return not(
        (len(record) < damages[0]+1) or record[damages[0]] == '#')

    if not damages:
        return 0 if record.find('#') > -1 else 1

    if not record:
        return 0

    result = 0

    if record[0] == '#':
        if found_damaged_springs():
            if more_damaged_springs():
                if not valid_next_spring():
                    return 0
                else:
                    result += matches2(record[damages[0]+1:], damages[1:])
            else:
                result += matches2(record[damages[0]:], damages[1:])

    elif record[0] == '.':
        result += matches2(record[1:], damages)

    elif record[0] == '?':
        result += matches2(record.replace('?', '#', 1), damages) + \
            matches2(record.replace('?', '.', 1), damages)

    return result


def part1(input):
    # part 1 slow method
    #  return sum(matches1(record, damages) for record, damages in input)

    return sum(matches2(record, damages) for record, damages in input)


def part2(input):
    return sum(matches2(record, damages) for record, damages in unfold(input))


def main():
    input = read_input("../data/day12.txt")
    test_input = read_input("../data/day12-test.txt")

    assert (res := part1(test_input)) == 21, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 7260

    assert (res := part2(test_input)) == 525152, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 1909291258644


if __name__ == '__main__':
    main()
