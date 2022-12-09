import os
import sys
sys.path.append(os.path.relpath("../../shared/python"))
import utils

# Puzzle description: https://adventofcode.com/2022/day/3


def value(c):
    if c.isupper():
        return ord(c) - ord('A') + 27
    else:
        return ord(c) - ord('a') + 1


def priority(rucksacks):
    result = set(rucksacks[0])
    for i in range(1, len(rucksacks)):
        result = result.intersection(set(rucksacks[i]))

    return value(result.pop())


def priority1(rucksack):
    mid = len(rucksack) // 2
    return priority([rucksack[0:mid], rucksack[mid:]])


def part1(input):
    return sum(map(priority1, input))


def part2(input):
    return sum(priority(input[slice(i, i + 3, 1)]) for i in range(0, len(input), 3))


def read_input(input_file):
    return utils.read_file_str(input_file, True)


def main():
    input = read_input("../data/day03.txt")
    test_input = read_input("../data/day03-test.txt")

    assert part1(test_input) == 157
    print(f'Part 1 {part1(input)}')  # 8176

    assert part2(test_input) == 70
    print(f'Part 2 {part2(input)}')  # 2689


if __name__ == '__main__':
    main()
