import os
import sys
sys.path.append(os.path.relpath("../../shared/python"))
import utils
import copy

# Puzzle description: https://adventofcode.com/2022/day/5


def top_crates(c):
    return ''.join([c[k][-1] for k in sorted(c.keys())])


def part1(input):
    stacks = copy.deepcopy(input[0])
    moves = copy.deepcopy(input[1])

    for move_count, from_, to_ in moves:
        for _ in range(move_count):
            stacks[to_].append(stacks[from_].pop())

    return top_crates(stacks)


def part2(input):
    stacks = copy.deepcopy(input[0])
    moves = copy.deepcopy(input[1])

    for move_count, from_, to_ in moves:
        from_stack = stacks[from_]
        stacks[to_] += from_stack[-move_count:]
        del from_stack[len(from_stack) - move_count:]

    return top_crates(stacks)


def read_input(input_file):
    input = utils.read_file_str(input_file)

    stacks = {}
    moves = []
    for s in input:
        if s.strip().startswith('1'):
            continue
        elif s.startswith('move'):
            ss = s.split(' ')
            moves.append((int(ss[1]), int(ss[3]), int(ss[5])))
        else:
            for i, ic in enumerate(range(1, len(s), 4)):
                crate = s[ic]
                if not utils.is_blank(crate):
                    stack = stacks.get(i + 1, [])
                    stack.insert(0, crate)
                    stacks[i + 1] = stack

    return (stacks, moves)


def main():
    input = read_input("../data/day05.txt")
    test_input = read_input("../data/day05-test.txt")

    assert part1(test_input) == 'CMZ'
    print(f'Part 1 {part1(input)}')  # SPFMVDTZT

    assert part2(test_input) == 'MCD'
    print(f'Part 2 {part2(input)}')  # ZFSJBPRFP


if __name__ == '__main__':
    main()
