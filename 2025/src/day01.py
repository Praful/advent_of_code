import sys
import os

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2025/day/1

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    def movement(m):
        steps = int(m[1:])
        if m[0] == 'L':
            steps = -steps
        return steps

    return list(map(movement, read_file_str(input_file, True)))


def update_dial(current, move, numbers=100):
    result = (current + move)
    clicks = result // numbers

    if current == 0 and clicks < 0:
        clicks += 1

    if result % numbers == 0 and clicks > 0:
        clicks -= 1

    result = result % numbers

    zero_point = 1 if result == 0 else 0

    return (result, abs(clicks), zero_point)


def part1(input, start=50):
    result = 0
    current = start
    for move in input:
        current, _, zero_point = update_dial(current, move)
        result += zero_point

    return result


def part2(input, start=50):
    result = 0
    current = start
    for move in input:
        current, clicks, zero_point = update_dial(current, move)
        result += clicks + zero_point
    return result


def main():
    input = read_input("../data/day01.txt")
    test_input = read_input("../data/day01-test.txt")

    assert (res := part1(test_input)) == 3, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 1118

    assert (res := part2(test_input)) == 6, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 6289


if __name__ == '__main__':
    main()
