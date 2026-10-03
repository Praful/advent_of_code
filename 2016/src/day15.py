import copy
from math import lcm

from utils import aoc_input_file, extract_ints, read_file_str

# Puzzle description: https://adventofcode.com/2016/day/15

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    input = read_file_str(aoc_input_file(__file__, input_file), True)
    return list(map(extract_ints, input))


# this is an incremental Chinese Remainder Theorem solver; it's much faster
# than the original solve
def solve(input):
    t = 0
    step = 1

    for disc, positions, _, start in input:
        while (t + disc + start) % positions != 0:
            t += step

        step = lcm(step, positions)

    return t


def original_solve(input):
    for t in range(1_000_000_000):
        final_positions = []
        for disc, positions, _, start in input:
            new_pos = (t + disc + start) % positions
            final_positions.append(new_pos == 0)

        if all(final_positions):
            return t

    assert False, "Not found"


def part1(input):
    return solve(input)


def part2(input):
    input2 = copy.deepcopy(input)
    input2.append((len(input) + 1, 11, 0, 0))

    return solve(input2)


def main():
    input = read_input("day15.txt")
    test_input = read_input("day15-test.txt")

    assert (res := part1(test_input)) == 5, f"Actual: {res}"
    print(f"Part 1 {part1(input)}")  # 376777

    print(f"Part 2 {part2(input)}")  # 3903937


if __name__ == "__main__":
    main()
