from collections import defaultdict

from utils import aoc_input_file, read_file_str

# Puzzle description: https://adventofcode.com/2016/day/12

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    input = read_file_str(aoc_input_file(__file__, input_file), True)
    return input


def part1(input):
    registers = defaultdict(int)
    ptr = 0
    while ptr < len(input):
        cmd = input[ptr].split()
        if cmd[0] == "cpy":
            if cmd[1].isalpha():
                registers[cmd[2]] = registers[cmd[1]]
            else:
                registers[cmd[2]] = int(cmd[1])
        elif cmd[0] == "inc":
            registers[cmd[1]] += 1
        elif cmd[0] == "dec":
            registers[cmd[1]] -= 1
        elif cmd[0] == "jnz":
            if cmd[1].isalpha():
                if registers[cmd[1]] != 0:
                    ptr += int(cmd[2])
                    continue
            else:
                if cmd[1] != "0":
                    ptr += int(cmd[2])
                    continue
        ptr += 1

    return registers["a"]


def part2(input):
    new_input = ["cpy 1 c"] + input
    return part1(new_input)


def main():
    input = read_input("day12.txt")
    test_input = read_input("day12-test.txt")

    assert (res := part1(test_input)) == 42, f"Actual: {res}"
    print(f"Part 1 {part1(input)}")  # 318083

    print(f"Part 2 {part2(input)}")  # 9227737


if __name__ == "__main__":
    main()
