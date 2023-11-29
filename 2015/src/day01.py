from utils import *
import os
import sys
sys.path.append(os.path.relpath("../../shared/python"))

# Puzzle description: https://adventofcode.com/2015/day/1


def read_input(input_file):
    input = read_file_str(input_file, True)
    return input[0]


def part1(input):
    return input.count('(') - input.count(')')


def part2(input):
    floor = 0
    for i in range(len(input)):
        if input[i] == '(':
            floor += 1
        elif input[i] == ')':
            floor -= 1

        if floor == -1:
            return i+1

    return 0


def main():
    input = read_input("../data/day01.txt")

    assert (res := part1('(())')) == 0, f'Actual: {res}'
    assert (res := part1('))(((((')) == 3, f'Actual: {res}'

    print(f'Part 1 {part1(input)}')  # 138

    assert (res := part2(')')) == 1, f'Actual: {res}'
    assert (res := part2('()())')) == 5, f'Actual: {res}'

    print(f'Part 2 {part2(input)}')  # 1771


if __name__ == '__main__':
    main()
