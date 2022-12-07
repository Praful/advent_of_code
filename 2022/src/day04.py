import os
import sys
sys.path.append(os.path.relpath("../../shared/python"))
import utils
import re

# Puzzle description: https://adventofcode.com/2022/day/4


def check_containment(r):
    return range_subset(r[0], r[1]) or range_subset(r[1], r[0])


def check_overlap(r):
    return len(range_overlap(*r)) > 0


def part1(input):
    return sum([check_containment(e) for e in input])


def part2(input):
    return sum([check_overlap(e) for e in input])


def range_overlap(range1, range2):
    # Assumes range step is always +1
    # https://stackoverflow.com/questions/6821156/how-to-find-range-overlap-in-python
    return range(max(range1[0], range2[0]), min(range1[-1], range2[-1]) + 1)


def range_subset(range1, range2):
    """Whether range1 is a subset of range2."""
    # https://stackoverflow.com/questions/32480423/how-to-check-if-a-range-is-a-part-of-another-range-in-python-3-x
    if not range1:
        return True  # empty range is subset of anything
    if not range2:
        return False  # non-empty range can't be subset of empty range
    if len(range1) > 1 and range1.step % range2.step:
        return False  # must have a single value or integer multiple step
    return range1.start in range2 and range1[-1] in range2


def parse(s):
    # eg s:  2-14,6-8
    match = re.findall(r'(\d*)-(\d*)', s)
    return (range(int(match[0][0]), int(match[0][1]) + 1), range(int(match[1][0]), int(match[1][1]) + 1))


def read_input(input_file):
    return list(map(parse, utils.read_file_str(input_file)))


def main():
    input = read_input("../data/day04.txt")
    # test_input = read_input("../data/day04-test.txt")

    # print(f'Part 1 (test) {part1(test_input)}')  # 2
    print(f'Part 1 {part1(input)}')  # 503

    # print(f'Part 2 (test) {part2(test_input)}')  # 4
    print(f'Part 2 {part2(input)}')  # 827


if __name__ == '__main__':
    main()
