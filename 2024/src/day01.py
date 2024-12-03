import sys
import os

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2024/day/1


def read_input(input_file):
    first_items, second_items = zip(
        *[map(int, item.split()) for item in read_file_str(input_file, True)])
    return first_items, second_items


def part1(first_items, second_items):
    return sum([abs(first - second) for first, second in zip(sorted(first_items), sorted(second_items))])


def part2(first_items, second_items):
    # Create a dictionary to store counts of elements in second list
    count_dict = {second: second_items.count(
        second) for second in set(second_items)}

    #  map:
    #  return sum(map(lambda first: first * count_dict.get(first, 0), first_items))
    #  list comprehension:
    return sum(first * count_dict.get(first, 0) for first in first_items)


def main():
    input = read_input("../data/day01.txt")
    test_input = read_input("../data/day01-test.txt")

    assert (res := part1(*test_input)) == 11, f'Actual: {res}'
    print(f'Part 1 {part1(*input)}')  # 1882714

    assert (res := part2(*test_input)) == 31, f'Actual: {res}'
    print(f'Part 2 {part2(*input)}')  # 19437052


if __name__ == '__main__':
    main()
