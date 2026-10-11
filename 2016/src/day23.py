from collections import defaultdict

from utils import aoc_input_file, read_file_str

# Puzzle description: https://adventofcode.com/2016/day/23

#  DEBUG = True
DEBUG = False
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    input = read_file_str(aoc_input_file(__file__, input_file), True)
    return input


def toggle_instruction(s):
    if "inc" in s:
        return s.replace("inc", "dec")
    elif "dec" in s:
        return s.replace("dec", "inc")
    elif "jnz" in s:
        return s.replace("jnz", "cpy")
    elif "cpy" in s:
        return s.replace("cpy", "jnz")
    elif "tgl" in s:
        return s.replace("tgl", "inc")


# For part2, the program takes too long. The hint in the description points to some
# multiplication optimisation, replacing the repeated increments/decrements.
# In my input, there is a sequence of 6 instructions that are the equivalent of
# two loop, an inner and outer. They are using addition and subtraction to
# multiply registers b and d.
# This optimisation is for my input. It may not work on other input.
def try_optimisation(input, ptr, registers):
    if (
        input[ptr : ptr + 6]
        == ["cpy b c", "inc a", "dec c", "jnz c -2", "dec d", "jnz d -5"]
        and registers["b"] > 0
        and registers["d"] > 0
    ):
        registers["a"] += registers["b"] * registers["d"]
        registers["c"] = 0
        registers["d"] = 0
        return ptr + 6
    else:
        return None


def solve(input, register_a=None):
    registers = defaultdict(int)
    input = input.copy()

    if register_a is not None:
        registers["a"] = register_a

    ptr = 0
    while ptr < len(input):
        try:
            print_debug("--------", ptr, input[ptr], registers)
            new_ptr = try_optimisation(input, ptr, registers)
            if new_ptr is not None:
                ptr = new_ptr
                continue
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
            elif cmd[0] == "tgl":
                i = registers[cmd[1]]
                print_debug(f"toggling {i + ptr}: {input[i + ptr]}")
                new_instruction = toggle_instruction(input[i + ptr])
                print_debug(f"to {new_instruction}")
                input[i + ptr] = new_instruction
        except Exception as e:
            # ignore invalid instructions created by tgl
            print_debug(
                f"{type(e).__name__}: ignoring invalid instruction: ptr {ptr}, {input[ptr]}, {registers}"
            )

        ptr += 1

    return registers["a"]


def main():
    input = read_input("day23.txt")
    test_input = read_input("day23-test.txt")

    assert (res := solve(test_input)) == 3, f"Actual: {res}"
    print(f"Part 1 {solve(input, 7)}")  # 12663

    # While I was working out the optimisation, I ran the program
    # and the answer popped out after about an hour.
    # The optimisation solves part 2 instantly for my input.
    # Afterwards on reddit, I saw someone said that the input is a formula:
    #       math.factorial(e) + (x * y)
    # where e is the number of eggs, and x and y come from the input. My answer is:
    #       12! + (99 * 77)
    # Other input might have different numbers for x and y.
    print(f"Part 2 {solve(input, 12)}")  # 479009223


if __name__ == "__main__":
    main()
