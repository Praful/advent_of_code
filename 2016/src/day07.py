import sys
import os
import re

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2016/day/7

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    input = read_file_str(input_file, True)
    return input

RE_BRACKETED_TEXT = r"\[.*?\]"

def is_aba(s, bab_list):
    s2 = re.sub(RE_BRACKETED_TEXT, " ", s)  # remove bracketed text
    for bab in bab_list:
        aba = bab[1] + bab[0] + bab[1]
        if re.search(rf"{aba}", s2):
            return True

    return False


# this finds overlapping aba patterns, required for part 2 eg xyxy => xyx and yxy
def get_abas(s):
    abas = set()

    for i in range(len(s)-2):
        a, b, c = s[i:i+3]
        if a == c and a != b:
            abas.add(a+b+a)

    return abas


# The algorithm is:
# 1. Find bracketed text
# 2. Find all the BABs in the brackets
# 3. Call is_aba to see if ABA exists outside bracketed text
def supports_ssl(s):
    bab_list = set()

    for m in re.finditer(RE_BRACKETED_TEXT, s):
        bab_list = bab_list | get_abas(m.group(0))

    if len(bab_list) > 0:
        return is_aba(s, bab_list)

    return False


# This would fail for part 1 if there were overlapping ABBAs
# eg abbaab[abba] returns false should be true since baab is not in brackets
# Fortunately, the input doesn't have overlapping abba.
def supports_tls(s):
    # (.) captures the first character.
    # (?!\1)(.) captures a second character, but only if it is not the same as the first.
    # \2\1 requires the next two characters to be the reverse of the captured pair.
    re_abba = r"(.)(?!\1)(.)\2\1"

    return bool(re.search(rf"{re_abba}", s)) and \
        not bool(re.search(rf"\[[a-z]*{re_abba}[a-z]*\]", s))


def part1(input):
    result = 0

    for s in input:
        if supports_tls(s):
            result += 1

    return result


def part2(input):
    result = 0

    for s in input:
        if supports_ssl(s):
            result += 1

    return result


def main():
    input = read_input("../data/day07.txt")
    test_input = read_input("../data/day07-test.txt")
    test_input2 = read_input("../data/day07-test2.txt")

    assert (res := part1(test_input)) == 2, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 115

    assert (res := part2(test_input2)) == 3, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 231


if __name__ == '__main__':
    main()
