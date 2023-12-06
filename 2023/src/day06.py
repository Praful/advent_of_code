import re
import os
import sys

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2023/day/06


def read_input(input_file):
    input = read_file_str(input_file, True)
    re.findall(r'\d+', input[0])

    times = list(map(int, input[0].split(':')[1].split()))
    distances = list(map(int, input[1].split(':')[1].split()))
    return (times, distances)


#  def ceiling_division(a, b):
    #  return (a + b - 1) // b


def distance_exceeded(v, d, t):
    # from v = d/t
    return (t-v)*v > d


def part1(input):
    times = input[0]
    distances = input[1]
    result = 1

    for i, t in enumerate(times):
        d = distances[i]
        result *= sum(1 for v in range(t) if distance_exceeded(v, d, t))

    return result


def part2(input):
    t = int(''.join(map(str, input[0])))
    d = int(''.join(map(str, input[1])))

    return sum(1 for v in range(t) if distance_exceeded(v, d, t))


def main():
    input = read_input("../data/day06.txt")
    test_input = read_input("../data/day06-test.txt")

    assert (res := part1(test_input)) == 288, f'Actual: {res}'

    print(f'Part 1 {part1(input)}')  # 170000

    assert (res := part2(test_input)) == 71503, f'Actual: {res}'

    print(f'Part 2 {part2(input)}')  # 20537782


if __name__ == '__main__':
    main()
