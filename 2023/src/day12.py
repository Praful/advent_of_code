import re
import os
import sys
from itertools import product
from functools import lru_cache

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


@lru_cache(maxsize=400)
def matches2(record, damages):
    # Part 2 fast method using recursion and cache (memoization).

    def more_damaged_springs(): return len(damages) > 1

    def found_damaged_springs():
        return re.findall(r'^[\#\?]{%i}' % next_grp, record)

    def valid_next_spring(): return not(
        (len(record) < next_grp + 1) or record[next_grp] == '#')

    if not damages:
        return 0 if '#' in record else 1

    if not record:
        return 0

    result = 0
    next_ch = record[0]
    next_grp = damages[0]

    if next_ch == '#':
        if found_damaged_springs():
            if more_damaged_springs():
                if valid_next_spring():
                    result += matches2(record[next_grp+1:], damages[1:])
                else:
                    return 0
            else:
                result += matches2(record[next_grp:], damages[1:])

    elif next_ch == '.':
        result += matches2(record[1:], damages)

    elif next_ch == '?':
        result += matches2(record.replace('?', '#', 1), damages) + \
            matches2(record.replace('?', '.', 1), damages)

    return result


def unfold(input):
    return (('?'.join([record] * 5), damages * 5) for record, damages in input)


def part1(input):
    # part 1 slow method
    #  return sum(matches1(record, damages) for record, damages in input)

    return sum(matches2(record, damages) for record, damages in input)


def part2(input):
    return part1(unfold(input))


def main():
    input = read_input("../data/day12.txt")
    test_input = read_input("../data/day12-test.txt")

    assert (res := part1(test_input)) == 21, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 7260

    assert (res := part2(test_input)) == 525152, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 1909291258644


if __name__ == '__main__':
    main()
