import sys
import os
import re

from hashlib import md5

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2016/day/5

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    input = read_file_str(input_file, True)
    return input


def hex_hash(s):
    return md5(s.encode('utf-8')).hexdigest()


def part1(input):
    result = []
    index = 0
    while len(result) < 8:
        h = hex_hash(input + str(index))
        if h[:5] == '00000':
            result.append(h[5])
            #  print(result)

        index += 1

    return ''.join(result)

REGEX_VALID_POS = re.compile(r'([0-7])')

def get_pos(c):
    result = -1
    if REGEX_VALID_POS.match(c) is not None:
        result = int(c)

    return result

def part2(input):
    result = [' '] * 8
    filled = 0
    index = 0
    while filled < 8:
        h = hex_hash(input + str(index))
        if h[:5] == '00000':
            pos = get_pos(h[5])
            if pos > -1 and result[pos] == ' ':
                result[pos] = h[6]
                filled += 1
                #  print(result)

        index += 1

    return ''.join(result)


def main():
    assert (res := part1("abc")) == "18f47a30", f'Actual: {res}'
    print(f'Part 1 {part1("wtnhxymk")}')  # 2414bc77

    assert (res := part2("abc")) == "05ace8e3", f'Actual: {res}'
    print(f'Part 2 {part2("wtnhxymk")}')  # 437e60fc


if __name__ == '__main__':
    main()
