from utils import aoc_input_file, extract_ints, read_file_str

# Puzzle description: https://adventofcode.com/2015/day/25

DEBUG = False
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    input = read_file_str(aoc_input_file(__file__, input_file), True)
    return extract_ints(input[0])


def test():
    print("rows")
    for r in range(1, 11):
        print(r, row_pos(r))

    print("-----------------------")

    print("cols")
    for c in range(1, 11):
        print(c, col_pos(c))

    print(row_col_diagonal(2, 3))
    print(row_col_diagonal(8, 4))
    print(row_col_diagonal(5, 7))


def next_code(n):
    return (n * 252533) % 33554393


# this gets col pos for row r
def col_pos(c, r=1, start=0):
    return sum(range(r + 1, r + c)) + start


# this gets row pos for column 1 only
def row_pos(r):
    return sum(range(1, r)) + 1


# given r, c find the diagonal position
def row_col_diagonal(r, c):
    return col_pos(c, r, row_pos(r))


def part1(input, code=20151125):
    r, c = input

    pos = row_col_diagonal(r, c)

    result = code

    for _ in range(1, pos):
        result = next_code(result)

    return result


def main():
    if DEBUG:
        test()

    input = read_input("day25.txt")

    assert (res := part1([5, 1])) == 77061, f"Actual: {res}"
    assert (res := part1([6, 5])) == 1534922, f"Actual: {res}"

    print(f"Part 1 {part1(input)}")  # 9132360


if __name__ == "__main__":
    main()
