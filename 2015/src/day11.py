import sys
import os
import re
import string

# for profiling
from cProfile import Profile
from pstats import Stats, SortKey

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2015/day/11

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


FORBIDDEN = {'i', 'o', 'l'}
VALID_STRAIGHTS = [
    string.ascii_lowercase[i:i+3]
    for i in range(len(string.ascii_lowercase) - 2)
    if not set(string.ascii_lowercase[i:i+3]) & FORBIDDEN
]


def contains_forbidden_chars(s):
    return bool(set(s) & FORBIDDEN)


def has_valid_straight(s):
    return any(triplet in s for triplet in VALID_STRAIGHTS)


def has_two_non_overlapping_pairs(s):
    #  (.)\1         # First pair: eg 'aa'; captures the char in group 1
    #  .*?           # Non-greedy match of anything between
    #  (?!\1)        # Check next char is NOT the same as first pair ie no overlapping
    #  (.)\2         # Second pair: must not be overlapping but can be same as first pair eg aaaa
    return re.search(r'(.)\1.*?(?!\1)(.)\2', s) is not None


def next_password(s):
    i = len(s) - 1
    while True:
        if s[i] == 'z':
            # wrap z to a
            s = s[:i] + 'a' + s[i+1:]
            i -= 1
        else:
            # increment
            s = s[:i] + chr(ord(s[i]) + 1) + s[i+1:]
            return s


def is_valid_password(s):
    return (not contains_forbidden_chars(s) and
            has_valid_straight(s) and
            has_two_non_overlapping_pairs(s))


def solve(input):
    result = input
    while True:
        result = next_password(result)
        if is_valid_password(result):
            break

    return result


def main():
    input = "hxbxwxba"

    assert is_valid_password("hijklmmn") == False
    assert is_valid_password("abbceffg") == False
    assert is_valid_password("abbcegjk") == False
    assert (res := solve("abcdefgh")) == "abcdffaa", f'Actual: {res}'
    assert (res := solve("ghijklmn")) == "ghjaabcc", f'Actual: {res}'

    part1_password = solve(input)

    print(f'Part 1 {part1_password}')  # hxbxxyzz
    print(f'Part 2 {solve(part1_password)}')  # hxcaabcc


if __name__ == '__main__':
    main()
