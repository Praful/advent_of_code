import copy
from math import isqrt

from utils import aoc_input_file, read_file_str

# Puzzle description: https://adventofcode.com/2018/day/19

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


def part1(input):
    registers = [0] * 6
    #  registers = [1, 0, 0, 0, 0, 0]
    ip_reg, program = input
    ip = 0

    while 0 <= ip < len(program):
        opcode, args = program[ip]

        print_debug(ip, opcode, args, registers, "-------------------")

        registers = operation(opcode, args, registers)
        registers[ip_reg] += 1
        ip = registers[ip_reg]

    print_debug(ip, program, registers)
    return registers[0]


# This is an optimised version of what the original program with opcodes does for part 2.
def sum_divisors(n):
    total = 0

    for d in range(1, isqrt(n) + 1):
        if n % d == 0:
            total += d

            if d != n // d:
                total += n // d

    return total


# Looking at the debug output, the code consists of two loops which are finding the
# sum of divisors of register 1 once it stabilizes: 10551343 in our case.
#
# The program is executing instructions 3, 4, 5 (sometimes), 6 (sometimes),
# 7 (sometimes), 8, 9, 10, 11. Specfically:
#
#  r1 is the number being examined.
#  r5 and r4 are potential factors.
#  r2 is a temporary register used for comparisons.
#  r4 is the loop counter.
#
#  The equivalent Python code is:
#
#    r5 = 1
#
#    while r5 <= r1:
#        r4 = 1
#
#        while r4 <= r1:
#            if r5 * r4 == r1:
#                r0 += r5
#
#            r4 += 1
#
#        r5 += 1
#
# The test r5*r4 == r1 is checking if r5 is a factor of r1. If it is, it's added to r0.
#
def part2(input):
    return sum_divisors(10551343)


def main():
    input = read_input("day19.txt")
    #  test_input = read_input("day19-test.txt")

    #  assert (res := part1(test_input)) == 0, f"Actual: {res}"
    print(f"Part 1 {part1(input)}")  # 1008

    print(f"Part 2 {part2(input)}")  # 11534976


if __name__ == "__main__":
    main()
