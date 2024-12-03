import sys
import os
import re

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2024/day/3


def read_input(input_file):
    input = read_file_str(input_file, True)
    return ' '.join(input)


def sum_of_products(s):
    match = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', s)

    if match:
        return sum(int(a) * int(b) for [a, b] in match)

    return 0


def part1(input):
    return sum_of_products(input)


def part2(input):
    # for regex, look for do() followed by don't() or end of line; everything
    # between will be what we want (ie one or more mul(n,m)) or empty
    # This reduces part2 to part1.

    #  result = 0
    #  this works but uses capture group for don't(), which is returned as well as what we want
    #  match = re.findall(r'do\(\)(.*?)(don\'t\(\)|$)', memory)
    #  for m in match:
    #  result += sum(product(s) for s in m)
    #  return result

    # this uses positive lookahead to exclude don't() from result
    # use (.*?) for non-greeedy capture
    match = re.findall(r'do\(\)(.*?)(?=don\'t\(\)|$)', 'do()' + input)

    return sum(sum_of_products(m) for m in match)


def main():
    input = read_input("../data/day03.txt")
    test_input = read_input("../data/day03-test.txt")
    test_input2 = read_input("../data/day03-test2.txt")

    assert (res := part1(test_input)) == 161, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 184576302

    assert (res := part2(test_input2)) == 48, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 118173507


if __name__ == '__main__':
    main()
