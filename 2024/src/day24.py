import sys
import os
from operator import __and__, __xor__, __or__

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2024/day/24

DEBUG = False
print_debug = print if DEBUG else lambda *a, **k: None

operators = {
    'AND': __and__,
    'XOR': __xor__,
    'OR': __or__
}


def read_input(input_file):
    with open(input_file, "r") as file:
        input = file.read().split('\n\n')

    values = {a: int(b) for line in input[0].split('\n')
              for a, b in [line.split(': ')]}

    # [0:-1] to exclude empty last element
    gates = [tuple(a) for line in input[1].split('\n')[0:-1]
             for a in [line.split(' ')]]

    return (values, gates)


#  gate = [intput1, operator, intput2, output]
INPUT1 = 0
OPERATOR = 1
INPUT2 = 2
OUTPUT = 4


def evaluate(gate, values):
    if not all([gate[INPUT1] in values, gate[INPUT2] in values]):
        return None

    operator = operators[gate[OPERATOR]]
    return operator(values[gate[INPUT1]], values[gate[INPUT2]])


def pad(n, prefix='z'): return f'{prefix}{n:02}'  # eg z00, z01, z02, etc


# return eg zn,.., z02, z01
def output(values, prefix='z'):

    result = [str(values[pad(n, prefix)])
              for n in range(100) if pad(n, prefix) in values]
    return int(''.join(result[::-1]), 2)  # ::-1 to reverse


def part1(input):
    values, gates = input
    done = set()
    while len(done) != len(gates):
        for gate in gates:
            if gate in done:
                continue

            if (result := evaluate(gate, values)) is not None:
                values[gate[OUTPUT]] = result
                done.add(gate)

    return output(values)


# Part 2 tells you that the the gates are adding X and Y. It turns out that it's using
# a full adder with carry.
# See here: https://www.geeksforgeeks.org/digital-logic/implementation-of-full-adder-using-half-adders/
#
# This pseudo code is the full_adder the gates implement where x and y are the ith bits. Carry in is
# the carry out of previous calculation.
#
# function full_adder(x, y, carry_in):
#   z = x XOR y XOR carry_in
#   carry_out = (x AND y) | (carry_in AND (x XOR y))
#   return z, carry_out
#
# This breaks down to the following in the input data:
#
#   temp1 = x XOR y               (1)
#   z = temp1 XOR carry_in        (2)
#   temp2 = x AND y               (3)
#   temp3 = carry_in AND temp1    (4)
#   carry_out = temp2 OR temp3    (5)
#   return z, carry_out
#
#
#  For the above adder to work, the following must be true, which is what we check for in
#  part2() code below:
#
#  1. XOR should have x and y as inputs (1) or z as output (2).
#  2. The input of an OR gate (5) should be the output of an AND gate (either 3 or 4).
#  3. There are edge cases for the most and least significant bits:
#     - in (2) there is no carry in (special case for x00+y00)
#     - the most significant bit of z (z45) is the output of an OR operation not XOR.

def part2(input):
    _, gates = input

    def bad_z_condition(
        g): return g[OUTPUT][0] == 'z' and g[OPERATOR] != 'XOR' and g[OUTPUT] != 'z45'

    def bad_xor_condition(g): return g[OPERATOR] == 'XOR' and \
        not ((g[INPUT1][0] in 'xy' and
              g[INPUT2][0] in 'xy') or g[OUTPUT][0] == 'z')

    def operands(g): return {g[INPUT1], g[INPUT2]}

    def and_output_condition(g): return g[OPERATOR] == 'AND' and \
        g[INPUT1] != 'x00' and g[INPUT2] != 'y00'

    bad_z = {g[OUTPUT] for g in gates if bad_z_condition(g)}
    bad_xor = {g[OUTPUT] for g in gates if bad_xor_condition(g)}

    or_inputs = {op for g in gates if g[OPERATOR] == "OR" for op in operands(g)}
    and_outputs = {g[OUTPUT] for g in gates if and_output_condition(g)}

    result = bad_z | bad_xor | (or_inputs ^ and_outputs)

    return ','.join(sorted(result))


def main():
    input = read_input("../data/day24.txt")
    test_input = read_input("../data/day24-test.txt")
    test_input2 = read_input("../data/day24-test2.txt")

    assert (res := part1(test_input)) == 4, f'Actual: {res}'
    assert (res := part1(test_input2)) == 2024, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 56278503604006

    print(f'Part 2 {part2(input)}')  # bhd,brk,dhg,dpd,nbf,z06,z23,z38


if __name__ == '__main__':
    main()
