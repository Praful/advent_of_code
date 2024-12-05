import sys
import os
from functools import cmp_to_key

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2022/day/5


def read_input(input_file):
    with open(input_file, "r") as file:
        input = file.read().split('\n\n')

    rules = set(input[0].split('\n'))
    updates = [list(map(int, line.split(','))) for line in input[1].split()]

    return (rules, updates)


def middle_page(update):
    return update[len(update)//2]


def is_rule(a, b, rules):
    return f'{a}|{b}' in rules


def is_ordered(rules, update):
    ordered = True
    for n, page in enumerate(update):
        for i in range(n+1, len(update)):
            if not is_rule(page, update[i], rules):
                ordered = False
                break

        if not ordered:
            return False

    return ordered


def solve(input):
    part1 = part2 = 0
    rules, updates = input

    def compare_pages(a, b):
        return -1 if is_rule(a, b, rules) else 1

    for update in updates:
        if is_ordered(rules, update):
            part1 += middle_page(update)
        else:
            part2 += middle_page(sorted(update, key=cmp_to_key(compare_pages)))

    return part1, part2


def main():
    input = read_input("../data/day05.txt")
    test_input = read_input("../data/day05-test.txt")

    part1_test, part2_test = solve(test_input)
    part1, part2 = solve(input)

    assert (res := part1_test) == 143, f'Actual: {res}'
    print(f'Part 1 {part1}')  # 4662

    assert (res := part2_test) == 123, f'Actual: {res}'
    print(f'Part 2 {part2}')  # 5900


if __name__ == '__main__':
    main()
