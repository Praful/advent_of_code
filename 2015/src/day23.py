from utils import aoc_input_file, read_file_str

# Puzzle description: https://adventofcode.com/2015/day/23

DEBUG = False
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    input = read_file_str(aoc_input_file(__file__, input_file), True)
    return input


def solve(input, reg_a=0):
    ptr = 0
    registers = {"a": reg_a, "b": 0}

    while ptr < len(input):
        instruction = input[ptr].split(" ")
        match instruction[0]:
            case "hlf":
                registers[instruction[1]] //= 2
                ptr += 1
            case "tpl":
                registers[instruction[1]] *= 3
                ptr += 1
            case "inc":
                registers[instruction[1]] += 1
                ptr += 1
            case "jmp":
                ptr += int(instruction[1])
            case "jie":
                if registers[instruction[1][0]] % 2 == 0:
                    ptr += int(instruction[2])
                else:
                    ptr += 1
            case "jio":
                if registers[instruction[1][0]] == 1:
                    ptr += int(instruction[2])
                else:
                    ptr += 1

        print_debug(ptr, instruction, registers)
    return registers["b"]


def main():
    input = read_input("day23.txt")
    test_input = read_input("day23-test.txt")

    assert (res := solve(test_input)) == 0, f"Actual: {res}"
    print(f"Part 1 {solve(input)}")  # 184
    print(f"Part 2 {solve(input, 1)}")  # 231


if __name__ == "__main__":
    main()
