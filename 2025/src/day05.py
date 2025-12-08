import sys
import os

# for profiling
from cProfile import Profile
from pstats import Stats, SortKey

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2025/day/5

DEBUG = False
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    def parse(s):
        r = s.split('-')
        return range(int(r[0]), int(r[1]))

    input = read_file_str_sections(input_file)

    # return ranges, ids
    return list(map(parse, input[0])), list(map(int, input[1]))


def range_overlaps(r1, r2):
    return r1.start <= r2.stop and r2.start <= r1.stop


def range_union(r1, r2):
    return range(min(r1.start, r2.start), max(r1.stop, r2.stop))


def merge_ranges(ranges):
    candidates = ranges
    result = []

    while candidates:
        remove_indexes = []
        merged_ranges = []

        was_merged = False
        to_check = candidates[0]
        for i in range(1, len(candidates)):
            if range_overlaps(to_check, candidates[i]):
                merged_ranges.append(range_union(to_check, candidates[i]))
                was_merged = True
                remove_indexes.append(0)
                remove_indexes.append(i)
                break

        if not was_merged:
            result.append(to_check)
            remove_indexes.append(0)

        candidates = [candidates[i]
                      for i in range(1, len(candidates)) if i not in remove_indexes]
        candidates += merged_ranges

    return result


def part1(input):
    ranges, ids = input
    result = 0

    for id in ids:
        for r in ranges:
            if r.start <= id <= r.stop:
                result += 1
                break

    return result


def part2(input):
    return sum(r.stop - r.start + 1 for r in merge_ranges(input[0]))


def main():
    input = read_input("../data/day05.txt")
    test_input = read_input("../data/day05-test.txt")

    assert (res := part1(test_input)) == 3, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 517

    assert (res := part2(test_input)) == 14, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 336173027056994


if __name__ == '__main__':
    main()
