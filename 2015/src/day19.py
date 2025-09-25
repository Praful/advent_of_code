import sys
import os
import re

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2015/day/19

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def parse(s):
    e = s.split('=>')
    return (e[0].strip(), e[1].strip())


# return list of tuples (from, to) and molecule
def read_input(input_file):
    with open(input_file, "r") as f:
        content = f.read()

    block = content.strip().split("\n\n")
    replacements = list(map(parse, block[0].split("\n")))

    return replacements, block[1]


def part1(replacements, molecule):
    new_molecules = set()
    for (k, v) in replacements:
        for m in re.finditer(k, molecule):
            new_molecule = molecule[:m.start()] + v + molecule[m.end():]
            new_molecules.add(new_molecule)

    return len(new_molecules)


# work backwards, starting with original target, replacing until we're left
# with all e's.
def part2(replacements, molecule):
    result = 0

    while set(molecule) != {'e'}:
        for (k, v) in replacements:
            if v in molecule:
                molecule = molecule.replace(v, k, 1)
                result += 1

    return result


def main():
    input = read_input("../data/day19.txt")
    test_input = read_input("../data/day19-test.txt")
    test_input2 = read_input("../data/day19-test2.txt")
    test_input3 = read_input("../data/day19-test3.txt")
    test_input4 = read_input("../data/day19-test4.txt")

    assert (res := part1(*test_input)) == 4, f'Actual: {res}'
    assert (res := part1(*test_input2)) == 7, f'Actual: {res}'
    print(f'Part 1 {part1(*input)}')  # 535

    assert (res := part2(*test_input3)) == 3, f'Actual: {res}'
    assert (res := part2(*test_input4)) == 6, f'Actual: {res}'
    print(f'Part 2 {part2(*input)}')  # 212


if __name__ == '__main__':
    main()
