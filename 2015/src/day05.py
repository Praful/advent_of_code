import re
import os
import sys

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2015/day/5


def read_input(input_file):
    input = read_file_str(input_file, True)
    return input


def has_adjacent_duplicates(s):
    return bool(re.search(r"(.)\1", s))


def has_at_least_three_vowels(s):
    return bool(re.search(r"(.*[aeiouAEIOU].*){3,}", s))


def has_repeating_pair(s):
    return bool(re.search(r"(..).*\1", s))


def has_repeat_with_one_between(s):
    return bool(re.search(r"(.).\1", s))


def is_nice1(s):
    if s.count('ab') > 0 or s.count('cd') > 0 or s.count('pq') > 0 or s.count('xy') > 0:
        return False

    if not has_adjacent_duplicates(s):
        return False

    if not has_at_least_three_vowels(s):
        return False

    return True


def is_nice2(s):
    if not has_repeating_pair(s):
        return False

    if not has_repeat_with_one_between(s):
        return False

    return True


def solve(input, nice=is_nice1):
    return sum(nice(s) for s in input)


def main():
    input = read_input("../data/day05.txt")
    test_input = read_input("../data/day05-test.txt")
    test_input2 = read_input("../data/day05-test2.txt")

    assert (res := solve(test_input)) == 2, f'Actual: {res}'
    print(f'Part 1 {solve(input)}')  # 258

    assert (res := solve(test_input2, is_nice2)) == 2, f'Actual: {res}'
    print(f'Part 2 {solve(input, is_nice2)}')  # 53


if __name__ == '__main__':
    main()
