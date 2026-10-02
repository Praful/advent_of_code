from utils import (
    EAST,
    NORTH,
    SOUTH,
    WEST,
    add_pos,
    aoc_input_file,
    in_grid,
    read_file_str,
    tile,
)

# Puzzle description: https://adventofcode.com/2016/day/2

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None

KEYPAD1 = ["123", "456", "789"]

KEYPAD2 = ["  1  ", " 234 ", "56789", " ABC ", "  D  "]

DIR_MAP = {"U": NORTH, "D": SOUTH, "L": WEST, "R": EAST}


def read_input(input_file):
    return read_file_str(aoc_input_file(__file__, input_file), True)


def solve(input, keypad=KEYPAD1, start=(1, 1)):
    result = []

    pos = start
    for line in input:
        for move in line:
            new_pos = add_pos(pos, DIR_MAP[move])
            if in_grid(new_pos, keypad) and tile(keypad, new_pos) != " ":
                pos = new_pos

        result.append(tile(keypad, pos))

    return "".join(result)


def main():
    input = read_input("day02.txt")
    test_input = read_input("day02-test.txt")

    assert (res := solve(test_input)) == "1985", f"Actual: {res}"
    print(f"Part 1 {solve(input)}")  # 52981

    assert (res := solve(test_input, KEYPAD2, (2, 0))) == "5DB3", f"Actual: {res}"
    print(f"Part 2 {solve(input, KEYPAD2, (2, 0))}")  # 74CD2


if __name__ == "__main__":
    main()
