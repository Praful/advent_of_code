import copy
from collections import Counter

from utils import aoc_input_file, read_file_str

# Puzzle description: https://adventofcode.com/2018/day/21

DEBUG = False
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    def parse(line):
        opcode = line.split()[0]
        args = list(map(int, line.split()[1:]))
        return opcode, args

    input = read_file_str(aoc_input_file(__file__, input_file), True)
    ip = int(input[0].split()[1])
    program = list(map(parse, input[1:]))
    return ip, program


def operation(opcode, arg, before_registers):
    a, b, c = arg
    result = copy.copy(before_registers)

    match opcode:
        case "addr":
            result[c] = result[a] + result[b]
        case "addi":
            result[c] = result[a] + b
        case "mulr":
            result[c] = result[a] * result[b]
        case "muli":
            result[c] = result[a] * b
        case "banr":
            result[c] = result[a] & result[b]
        case "bani":
            result[c] = result[a] & b
        case "borr":
            result[c] = result[a] | result[b]
        case "bori":
            result[c] = result[a] | b
        case "setr":
            result[c] = result[a]
        case "seti":
            result[c] = a
        case "gtir":
            result[c] = 1 if a > result[b] else 0
        case "gtri":
            result[c] = 1 if result[a] > b else 0
        case "gtrr":
            result[c] = 1 if result[a] > result[b] else 0
        case "eqir":
            result[c] = 1 if a == result[b] else 0
        case "eqri":
            result[c] = 1 if result[a] == b else 0
        case "eqrr":
            result[c] = 1 if result[a] == result[b] else 0

    return result


# This is a translaton of the input program into Python. It
# represents my input and likely won't work for other input.
# However, I've extracted r5 from the program, which may be
# the only variable in inputs. So this may work for others.
def solve(input):
    _, program = input
    r5_original = program[7][1][0]
    r5 = 0
    seen = set()
    prev = 0
    part1 = None

    while True:
        r4 = r5 | 65536
        r5 = r5_original

        while True:
            # store the lowest 8 bits of r4 in r3
            r3 = r4 & 255

            #  select the lowest lowest 24 bits
            r5 = (r5 + r3) & 16777215  # = 0xFFFFFF (from program)
            r5 = (r5 * 65899) & 16777215

            if r4 < 256:
                break

            # this is the inner loop that takes a long time in the input program
            r4 //= 256

        # Instruction 28: halts if r5 == r0 (set r0 to test)
        #  if r5 == r0:
        #  break

        if part1 is None:
            part1 = r5

        if r5 in seen:
            # we're done if loop starts repeating ie when we see
            # the same r5 value again
            return part1, prev
        else:
            seen.add(r5)
            prev = r5


# Function to analyse the input program and find the hotspot.
# Common opcodes executed to find hotspot:
#  (18, 257115)
#  (19, 257114)
#  (20, 257114)
#  (21, 257114)
#  (22, 257102)
#  (24, 257102)
#  (25, 257102)
#  (8, 19)
#  (9, 19)
#  (10, 19)
def analyse(input):
    ip_reg, program = input
    ip = 0

    # count which ops are executed
    counts = Counter()
    n = 0

    for halting_number in range(1):
        registers = [halting_number, 0, 0, 0, 0, 0]
        while 0 <= ip < len(program):
            opcode, args = program[ip]

            print(ip, opcode, args, registers)
            registers = operation(opcode, args, registers)
            if opcode == "eqrr":
                print("-" * 20, registers)

            registers[ip_reg] += 1
            ip = registers[ip_reg]

            #  counts[ip] += 1
            #  n += 1
            #  if n % 10000 == 0:
            #  print(counts.most_common(10))


def main():
    input = read_input("day21.txt")

    #  analyse(input)

    print(f"Part 1 & 2 {solve(input)}")  # (7224964, 13813247)


if __name__ == "__main__":
    main()
