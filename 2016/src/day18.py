from utils import aoc_input_file, read_file_str

# Puzzle description: https://adventofcode.com/2016/day/18

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None

SAFE = "."
TRAP = "^"


def read_input(input_file):
    input = read_file_str(aoc_input_file(__file__, input_file), True)
    return input[0]


def generate_new_tile(row, pos):
    left = row[pos - 1] if pos > 0 else SAFE
    right = row[pos + 1] if pos < len(row) - 1 else SAFE
    centre = row[pos]

    if (
        (left == TRAP and centre == TRAP and right == SAFE)
        or (left == SAFE and centre == TRAP and right == TRAP)
        or (left == TRAP and centre == SAFE and right == SAFE)
        or (left == SAFE and centre == SAFE and right == TRAP)
    ):
        return TRAP
    else:
        return SAFE


def safe_count(row):
    return row.count(SAFE)


def solve(input, row_count):
    row = input
    result = safe_count(row)

    for _ in range(row_count - 1):
        row = "".join(generate_new_tile(row, i) for i in range(len(row)))
        result += safe_count(row)

    return result


def main():
    input = read_input("day18.txt")
    test_input = "..^^."
    test_input2 = ".^^.^.^^^^"

    assert (res := solve(test_input, 3)) == 6, f"Actual: {res}"
    assert (res := solve(test_input2, 10)) == 38, f"Actual: {res}"
    print(f"Part 1 {solve(input, 40)}")  # 1956

    print(f"Part 2 {solve(input, 400_000)}")  # 19995121


if __name__ == "__main__":
    main()
