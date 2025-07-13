import sys
import os
import itertools

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2015/day/9

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    def parse(s):
        words = s.split(" ")
        return (words[0], words[2]), int(words[4])

    input = read_file_str(input_file, True)
    return dict(map(parse, input))


def solve(input):
    def hop_distance(hop):
        return input.get(hop, input.get((hop[1], hop[0])))

    def route_distance(route):
        return sum(map(hop_distance, itertools.pairwise(route)))

    cities = set().union(*input.keys())
    distances = list(map(route_distance, itertools.permutations(cities)))

    return min(distances), max(distances)


def main():
    input = read_input("../data/day09.txt")
    test_input = read_input("../data/day09-test.txt")

    assert (res := solve(test_input)) == (605, 982), f'Actual: {res}'
    print(f'Part 1 and 2 {solve(input)}')  # (141, 736)


if __name__ == '__main__':
    main()
