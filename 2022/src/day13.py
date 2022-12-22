import os
import sys
sys.path.append(os.path.relpath("../../shared/python"))
from utils import *
from itertools import zip_longest
from functools import cmp_to_key

# Puzzle description: https://adventofcode.com/2022/day/13


def read_input(input_file):
    return [eval(l) for l in read_file_str(input_file, True)
            if not is_blank(l)]


# return -1 if left lower than right
#        1 if left higher
#        0 if the same
def compare(left, right):
    if left is None:
        return -1
    if right is None:
        return 1

    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return -1
        elif left > right:
            return 1
        else:
            return 0
    elif isinstance(left, list) and isinstance(right, list):
        for l2, r2 in zip_longest(left, right):
            if (result := compare(l2, r2)) != 0:
                return result
        return 0
    else:
        l2 = [left] if isinstance(left, int) else left
        r2 = [right] if isinstance(right, int) else right
        return compare(l2, r2)


def part1(packets):
    return sum(((i + 1) // 2 + 1) for i in range(0, len(packets), 2)
               if compare(packets[i], packets[i + 1]) == -1)


def part2(packets):
    div1, div2 = [[2]], [[6]]
    sorted_packets = sorted([*packets, div1, div2], key=cmp_to_key(compare))
    return (sorted_packets.index(div1) + 1) * (sorted_packets.index(div2) + 1)


def main():
    input = read_input("../data/day13.txt")
    test_input = read_input("../data/day13-test.txt")

    assert part1(test_input) == 13
    print(f'Part 1 {part1(input)}')  # 5003

    assert part2(test_input) == 140
    print(f'Part 2 {part2(input)}')  # 20280


if __name__ == '__main__':
    main()
