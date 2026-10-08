import re
from enum import Enum

from utils import aoc_input_file, extract_ints, read_file_str

# Puzzle description: https://adventofcode.com/2016/day/21

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


class Op(Enum):
    SWAP_POS = 0
    SWAP_LETTER = 1
    ROTATE_LEFT = 2
    ROTATE_RIGHT = 3
    ROTATE_BASED = 4
    REVERSE = 5
    MOVE = 6


def parse(s):
    if s.startswith("swap position"):
        pos = extract_ints(s)
        return Op.SWAP_POS, pos[0], pos[1]
    elif s.startswith("swap letter"):
        r = re.search(r"swap letter (\w+) with letter (\w+)", s)
        return Op.SWAP_LETTER, r.group(1), r.group(2)
    elif s.startswith("rotate left"):
        r = re.search(r"rotate left (\d+) step", s)
        return Op.ROTATE_LEFT, int(r.group(1))
    elif s.startswith("rotate right"):
        r = re.search(r"rotate right (\d+) step", s)
        return Op.ROTATE_RIGHT, int(r.group(1))
    elif s.startswith("rotate based"):
        r = re.search(r"rotate based on position of letter (\w+)", s)
        return Op.ROTATE_BASED, r.group(1)
    elif s.startswith("reverse"):
        r = re.search(r"reverse positions (\d+) through (\d+)", s)
        return Op.REVERSE, int(r.group(1)), int(r.group(2))
    elif s.startswith("move"):
        r = re.search(r"move position (\d+) to position (\d+)", s)
        return Op.MOVE, int(r.group(1)), int(r.group(2))
    else:
        raise ValueError(f"Unknown operation: {s}")


def read_input(input_file):
    input = read_file_str(aoc_input_file(__file__, input_file), True)
    return list(map(parse, input))


def swap_pos(s, a, b):
    a, b = min(a, b), max(a, b)
    return s[:a] + s[b] + s[a + 1 : b] + s[a] + s[b + 1 :]


def swap_letters(s, a, b):
    return "".join(b if c == a else a if c == b else c for c in s)


def rotate_right(s, n):
    n %= len(s)
    return s[-n:] + s[:-n] if n else s


def rotate_left(s, n):
    n %= len(s)
    return s[n:] + s[:n]


def rotate_based_on_position(s, a):
    i = s.index(a)
    n = 1 + i + (1 if i >= 4 else 0)
    return rotate_right(s, n)


# for part2
def rotate_based_on_position_inverse(s, a):
    # Try every reverse rotation. We're done when result produces the
    # original s when the original rotate_based is applied to our
    # candidate result
    for r in range(len(s)):
        result = rotate_left(s, r)
        if rotate_based_on_position(result, a) == s:
            return result

    raise ValueError(f"Could not find rotate based inverse for {a} in {s}")


def reverse(s, a, b):
    return s[:a] + s[a : b + 1][::-1] + s[b + 1 :]


def move(s, a, yb):
    chars = list(s)
    chars.insert(yb, chars.pop(a))
    return "".join(chars)


def part1(input, start):
    result = start

    for operation in input:
        match operation[0]:
            case Op.SWAP_POS:
                result = swap_pos(result, operation[1], operation[2])
            case Op.SWAP_LETTER:
                result = swap_letters(result, operation[1], operation[2])
            case Op.ROTATE_LEFT:
                result = rotate_left(result, operation[1])
            case Op.ROTATE_RIGHT:
                result = rotate_right(result, operation[1])
            case Op.ROTATE_BASED:
                result = rotate_based_on_position(result, operation[1])
            case Op.REVERSE:
                result = reverse(result, operation[1], operation[2])
            case Op.MOVE:
                result = move(result, operation[1], operation[2])
            case _:
                raise ValueError(f"Unknown operation: {operation}")

    return result


def part2(input, start):
    result = start

    # the input is reversed and each instruction inversed; this is straight
    # forward for most except ROTATE_BASED
    for operation in reversed(input):
        match operation[0]:
            case Op.SWAP_POS:
                result = swap_pos(result, operation[1], operation[2])
            case Op.SWAP_LETTER:
                result = swap_letters(result, operation[1], operation[2])
            case Op.ROTATE_LEFT:  # reverse rotation
                result = rotate_right(result, operation[1])
            case Op.ROTATE_RIGHT:  # reverse rotation
                result = rotate_left(result, operation[1])
            case Op.ROTATE_BASED:  # special case
                result = rotate_based_on_position_inverse(result, operation[1])
            case Op.REVERSE:
                result = reverse(result, operation[1], operation[2])
            case Op.MOVE:  # switch a and b
                result = move(result, operation[2], operation[1])
            case _:
                raise ValueError(f"Unknown operation: {operation}")

    return result


def main():
    input = read_input("day21.txt")
    test_input = read_input("day21-test.txt")

    assert (res := part1(test_input, "abcde")) == "decab", f"Actual: {res}"
    print(f"Part 1 {part1(input, 'abcdefgh')}")  # bfheacgd

    print(f"Part 2 {part2(input, 'fbgdceah')}")  # gcehdbfa


if __name__ == "__main__":
    main()
