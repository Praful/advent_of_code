import re
from collections import defaultdict

from utils import aoc_input_file, read_file_str

# Puzzle description: https://adventofcode.com/2016/day/25

DEBUG = False
print_debug = print if DEBUG else lambda *a, **k: None

# were looking for 0101010101... or 01010101010 since we may quit when
# we have "enough" output.
REGEX_PATTERN = r"^(01)+0?$"


def read_input(input_file):
    input = read_file_str(aoc_input_file(__file__, input_file), True)
    return input


def solve(input, register_a=None):
    result = ""
    registers = defaultdict(int)
    input = input.copy()

    if register_a is not None:
        registers["a"] = register_a

    ptr = 0
    run_length = 0
    # 100000 is a magic number I plucked out of the air to establish
    # a stopping condition that will give us a load of "0101010..."
    while ptr < len(input) and run_length < 100000:
        try:
            print_debug("--------", ptr, input[ptr], registers)
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
                        y = cmd[2]
                        if y.isalpha():
                            y = registers[y]
                        else:
                            y = int(y)
                        ptr += int(y)
                        continue
            elif cmd[0] == "out":
                #  print(registers)
                if cmd[1].isalpha():
                    result += str(registers[cmd[1]])
                else:
                    result += cmd[1]

                if len(result) > 2 and not re.search(REGEX_PATTERN, result):
                    return ""

        except Exception as e:
            # ignore invalid instructions created by tgl
            print(
                f"{type(e).__name__}: ignoring invalid instruction: ptr {ptr}, {registers}"
            )

        run_length += 1
        ptr += 1

    return result


def part1(input):
    for i in range(1000000):
        result = solve(input, i)
        print_debug(i, result)
        if re.search(REGEX_PATTERN, result):
            return i


def main():
    input = read_input("day25.txt")

    print(f"Part 1 {part1(input)}")  # 196


if __name__ == "__main__":
    main()
