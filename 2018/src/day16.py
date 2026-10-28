import copy
from enum import Enum

from utils import aoc_input_file, extract_ints, read_file_str_sections

# Puzzle description: https://adventofcode.com/2018/day/16

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


# ignore numbers
class OpCodes(Enum):
    ADDR = 0
    ADDI = 1
    MULR = 2
    MULI = 3
    BANR = 4
    BANI = 5
    BORR = 6
    BORI = 7
    SETR = 8
    SETI = 9
    GTIR = 10
    GTRI = 11
    GTRR = 12
    EQIR = 13
    EQRI = 14
    EQRR = 15


class Sample:
    def __init__(self, before, instruction, after):
        self.before = extract_ints(before)
        self.instruction = extract_ints(instruction)
        self.after = extract_ints(after)

    @property
    def a(self):
        return self.instruction[1]

    @property
    def b(self):
        return self.instruction[2]

    @property
    def c(self):
        return self.instruction[3]

    @property
    def opcode(self):
        return self.instruction[0]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"Sample(before={self.before}, instruction={self.instruction}, after={self.after})"


def read_input(input_file):
    input = read_file_str_sections(aoc_input_file(__file__, input_file))

    samples = [Sample(s[0], s[1], s[2]) for s in input if len(s) == 3]
    test_program = [extract_ints(s) for l in input if len(l) > 3 for s in l]

    return samples, test_program


def operation(opcode, a, b, c, before_registers):
    result = copy.copy(before_registers)

    match opcode:
        case OpCodes.ADDR:
            result[c] = result[a] + result[b]
        case OpCodes.ADDI:
            result[c] = result[a] + b
        case OpCodes.MULR:
            result[c] = result[a] * result[b]
        case OpCodes.MULI:
            result[c] = result[a] * b
        case OpCodes.BANR:
            result[c] = result[a] & result[b]
        case OpCodes.BANI:
            result[c] = result[a] & b
        case OpCodes.BORR:
            result[c] = result[a] | result[b]
        case OpCodes.BORI:
            result[c] = result[a] | b
        case OpCodes.SETR:
            result[c] = result[a]
        case OpCodes.SETI:
            result[c] = a
        case OpCodes.GTIR:
            result[c] = 1 if a > result[b] else 0
        case OpCodes.GTRI:
            result[c] = 1 if result[a] > b else 0
        case OpCodes.GTRR:
            result[c] = 1 if result[a] > result[b] else 0
        case OpCodes.EQIR:
            result[c] = 1 if a == result[b] else 0
        case OpCodes.EQRI:
            result[c] = 1 if result[a] == b else 0
        case OpCodes.EQRR:
            result[c] = 1 if result[a] == result[b] else 0

    return result


def part1(input):
    result = 0
    samples, _ = input

    for s in samples:
        match_count = 0
        for opcode in OpCodes:
            if operation(opcode, s.a, s.b, s.c, s.before) == s.after:
                match_count += 1
                if match_count > 2:
                    break

        if match_count > 2:
            result += 1

    return result


# these are the possible opcode mappings for the instructions' opcodes
def possible_opcode_mappings(samples):
    result = {}

    for s in samples:
        matching_opcodes = set()
        for opcode in OpCodes:
            if operation(opcode, s.a, s.b, s.c, s.before) == s.after:
                matching_opcodes.add(opcode)

        if s.opcode not in result:
            result[s.opcode] = matching_opcodes
        else:
            result[s.opcode] = result[s.opcode] & matching_opcodes

    return result


# narrow down the possible mappings to one opcode per instruction opcode
def final_opcode_mapping(possible_opcode_mappings):
    result = {}

    while len(result) < len(OpCodes):
        for key, mapped in possible_opcode_mappings.items():
            if len(mapped) == 1:
                found_opcode = mapped.pop()
                result[key] = found_opcode

                for possible_opcodes in possible_opcode_mappings.values():
                    if found_opcode in possible_opcodes:
                        possible_opcodes.remove(found_opcode)

    return result


def part2(input):
    samples, test_program = input

    opcode_mapping = final_opcode_mapping(possible_opcode_mappings(samples))

    return run_program(test_program, opcode_mapping)


def run_program(test_program, opcode_mapping):
    registers = [0, 0, 0, 0]

    for instruction in test_program:
        opcode = opcode_mapping[instruction[0]]
        registers = operation(
            opcode, instruction[1], instruction[2], instruction[3], registers
        )

    return registers[0]


def main():
    input = read_input("day16.txt")

    print(f"Part 1 {part1(input)}")  # 544
    print(f"Part 2 {part2(input)}")  # 600


if __name__ == "__main__":
    main()
