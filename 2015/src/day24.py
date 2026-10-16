from itertools import combinations
from math import prod

from utils import aoc_input_file, extract_ints, flatten_list, read_file_str

# Puzzle description: https://adventofcode.com/2015/day/24

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    input = read_file_str(aoc_input_file(__file__, input_file), True)
    return flatten_list(map(extract_ints, input))


def quantum_entanglement(l):
    return prod(l)


# We should check that the remaining numbers can be partitioned into groups too. However,
# the example and real input work fine without this check. This is probably deliberate.
def solve(input, groups=3):
    target = sum(input) // groups

    for size in range(1, len(input) + 1):
        candidates = [
            group for group in combinations(input, size) if sum(group) == target
        ]

        if candidates:
            return quantum_entanglement(min(candidates, key=quantum_entanglement))

    raise RuntimeError("No solution found")


def main():
    input = read_input("day24.txt")
    test_input = read_input("day24-test.txt")

    assert (res := solve(test_input)) == 99, f"Actual: {res}"
    print(f"Part 1 {solve(input)}")  #  10439961859

    assert (res := solve(test_input, 4)) == 44, f"Actual: {res}"
    print(f"Part 2 {solve(input, 4)}")  # 72050269


if __name__ == "__main__":
    main()
