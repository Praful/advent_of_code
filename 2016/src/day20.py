from utils import aoc_input_file, extract_ints, read_file_str

# Puzzle description: https://adventofcode.com/2016/day/20

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    input = read_file_str(aoc_input_file(__file__, input_file), True)
    return sorted([extract_ints(line) for line in input])


def solve(input, max_valid=0, part2=False):
    result = 0
    highest = input[0][1]

    for n in input:
        if n[0] <= highest + 1:
            highest = max(highest, n[1])
        else:
            if not part2:
                return n[0] - 1
            else:
                result += n[0] - highest - 1
                highest = n[1]

    result += max_valid - highest

    return result


def main():
    input = read_input("day20.txt")
    test_input = read_input("day20-test.txt")

    assert (res := solve(test_input)) == 3, f"Actual: {res}"
    print(f"Part 1 {solve(input)}")  # 4793564

    assert (res := solve(test_input, 9, True)) == 2, f"Actual: {res}"
    print(f"Part 2 {solve(input, 4294967295, True)}")  # 146


if __name__ == "__main__":
    main()
