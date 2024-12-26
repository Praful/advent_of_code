import sys
import os
import re
from pprint import pprint

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2024/day/17

DEBUG = False
print_debug = print if DEBUG else lambda *a, **k: None


class Computer:
    def __init__(self):
        self.A = 0
        self.B = 0
        self.C = 0
        self.output = []


#  Program: 0,1,5,4,3,0
#

    def __str__(self):
        return f'A: {self.A}\nB: {self.B}\nC {self.C}\nOutput {self.output}'

    def run(self, A, B, C, program):
        self.A = A
        self.B = B
        self.C = C
        self.output = []

        instr = 0
        while instr < len(program):
            opcode = program[instr]
            operand = program[instr+1]

            match opcode:
                case 0:
                    self.adv(operand)
                    instr += 2
                case 1:
                    self.bxl(operand)
                    instr += 2
                case 2:
                    self.bst(operand)
                    instr += 2
                case 3:
                    if (res := self.jnz(operand)) is None:
                        instr += 2
                    else:
                        instr = res
                case 4:
                    self.bxc(operand)
                    instr += 2
                case 5:
                    self.out(operand)
                    instr += 2
                case 6:
                    self.bdv(operand)
                    instr += 2
                case 7:
                    self.cdv(operand)
                    instr += 2
                case _:
                    raise ValueError(
                        f'Invalid opcode {opcode} at {instr}', opcode)

        return self.output

    def combo(self, operand):
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.A
            case 5:
                return self.B
            case 6:
                return self.C
            case 7:
                raise ValueError(
                    f'Invalid operand {operand} for combo', operand)
            case _:
                raise ValueError(
                    f'Invalid operand {operand} for combo', operand)

    def divide_power(self, operand):
        return self.A // (2 ** self.combo(operand))

    def adv(self, operand):  # 0
        self.A = self.divide_power(operand)

    def bxl(self, operand):  # 1
        self.B = self.B ^ operand

    def bst(self, operand):  # 2
        self.B = self.combo(operand) % 8

    def jnz(self, operand):  # 3
        if self.A == 0:
            return None
        else:
            return operand

    def bxc(self, operand):  # 4
        self.B = self.B ^ self.C

    def out(self, operand):  # 5
        result = self.combo(operand) % 8
        self.output.append(result)

    def bdv(self, operand):  # 6
        self.B = self.divide_power(operand)

    def cdv(self, operand):  # 7
        self.C = self.divide_power(operand)


def read_input(input_file):
    def num(s): return int(re.findall(r'(\d+)', s)[0])

    input = read_file_str(input_file, True)

    A = num(input[0])
    B = num(input[1])
    C = num(input[2])
    program = list(map(int, (input[4].split(' ')[1]).split(',')))

    return [A, B, C, program]


def part1(input):
    computer = Computer()
    return ",".join(map(str, computer.run(*input)))


#  Program: 2,4,1,7,7,5,0,3,1,7,4,1,5,5,3,0
# The last three bits of A determine the output; so we find the right-hand digit
# of the program then shift A three bits and try another value 0-7; we
# continue this until we've found all values in program.
def part2(input, A, compare_index):
    _, B, C, program = input
    result = set()
    computer = Computer()

    for n in range(8):
        A2 = (A << 3) | n
        output = computer.run(A2, B, C, program)
        if output == program[-compare_index:]:
            if output == program:
                result.add(A2)
            else:
                possible = part2(input, A2, compare_index+1)
                if possible:
                    result.add(possible)

    if len(result) > 0:
        return min(result)
    else:
        return 0


def main():
    input = read_input("../data/day17.txt")
    test_input = read_input("../data/day17-test.txt")
    #  solve(0, 1, input)

    part1((0, 0, 9, [2, 6]))
    part1((10, 0, 0, [5, 0, 5, 1, 5, 4]))
    part1((2024, 0, 0, [0, 1, 5, 4, 3, 0]))

    assert (res := part1(test_input)
            ) == '4,6,3,5,6,3,5,2,1,0', f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 1,0,2,0,5,7,2,1,3

    print(f'Part 2 {part2(input, 0, 1)}')  # 265652340990875


if __name__ == '__main__':
    main()
