import re
import os
import sys

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2023/day/08


def read_input(input_file):
    input = read_file_str(input_file, True)
    instructions = input[0]
    nodes = {}
    for i in range(2, len(input)):
        k, v1, v2 = re.findall(r'\w+', input[i])
        nodes[k] = (v1, v2)

    return (instructions, nodes)


LR_MAP = {'L': 0, 'R': 1}


def solve(input, start_node, end_func):
    def left_right(): return LR_MAP[instructions[steps % instr_len]]

    instructions, nodes = input
    instr_len = len(instructions)
    steps = 0
    next_node = start_node
    while not end_func(next_node):
        next_node = nodes[next_node][left_right()]
        steps += 1

    return steps


def part1(input): return solve(input, 'AAA', lambda n: n == 'ZZZ')


def part2(input):
    # There is a curious property of the input data that allows us to use lcm to solve.
    # (An alternative is to use the Chinese Remainder Theorem.)
    # For starting nodes S1, S2, ..., Sn (which end in 'A'), there is a unique end point
    # E1, ..., En (which ends in 'Z'). The steps to get from S1, S2, ..., Sn to
    # E1, E2, ..., En are different, say N1, ..., Nn. There is a cycle so eg S1 goes to E1
    # after N1 steps. Then after another N1 steps, S1 goes to E1 again. The same for the
    # rest. This allows us to work out the number of steps to get to E1, E2, ..., En
    # independently. Then we can use the lcm to work out the number of steps
    # to get to E1, E2, ..., En at the same time.

    def steps(n): return solve(input, n, lambda n: n.endswith('Z'))

    start_nodes = [k for k in input[1].keys() if k.endswith('A')]
    return lcm(map(steps, start_nodes))


def main():
    input = read_input("../data/day08.txt")
    test_input1 = read_input("../data/day08-test-1.txt")
    test_input2 = read_input("../data/day08-test-2.txt")

    assert (res := part1(test_input1)) == 2, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 18727

    assert (res := part2(test_input2)) == 6, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 18024643846273


if __name__ == '__main__':
    main()
