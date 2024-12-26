import sys
import os

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2024/day/19

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    input = read_file_str(input_file, True)
    return set(input[0].split(', ')), input[2:]  # towels, designs


def design_possible(towels, design, index):
    if index == len(design):
        return True

    for towel in towels:
        if towel == design[index:index+len(towel)]:
            if design_possible(towels, design, index+len(towel)):
                return True

    return False


def design_possible_count(towels, design, cache):
    if design == "":
        return 1

    if (c := cache.get(design, None)) is not None:
        return c

    result = 0
    for towel in towels:
        if towel == design[:len(towel)]:
            result += design_possible_count(towels, design[len(towel):], cache)

    cache[design] = result
    return result


def part1(towels, designs):
    return sum(1 for d in designs if design_possible(towels, d, 0))


def part2(towels, designs):
    return sum(design_possible_count(towels, d, {}) for d in designs)


def main():
    input = read_input("../data/day19.txt")
    test_input = read_input("../data/day19-test.txt")

    assert (res := part1(*test_input)) == 6, f'Actual: {res}'
    print(f'Part 1 {part1(*input)}')  # 363

    assert (res := part2(*test_input)) == 16, f'Actual: {res}'
    print(f'Part 2 {part2(*input)}')  # 642535800868438


if __name__ == '__main__':
    main()
