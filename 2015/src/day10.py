import re
import sys
import os

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402


# Puzzle description: https://adventofcode.com/2015/day/10

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None


def next_seq(seq):
    result = ""
    previous = None
    count = 0
    for c in seq:
        if c != previous:
            if previous is not None:
                result += str(count) + previous
            previous = c
            count = 1
        else:
            count += 1

    return result + str(count) + previous


from functools import reduce

# slower regex version
def next_seq_regex(seq):
    # find runs of identical digits
    sequences = re.findall(r'((\d)\2*)', seq)

    result = ""
    for s in sequences:
        result += str(len(s[0])) + s[1]

    return result

def solve(seq, steps=1):
    #  for _ in range(steps):
        #  seq = next_seq(seq)
    #  return seq
    
    # slightly faster functional version
    return reduce(lambda acc, _: next_seq(acc), range(steps), seq)


def main():
    input = "3113322113"

    assert (res := solve("1")) == "11", f'Actual: {res}'
    assert (res := solve("11")) == "21", f'Actual: {res}'
    assert (res := solve("21")) == "1211", f'Actual: {res}'
    assert (res := solve("1211")) == "111221", f'Actual: {res}'
    assert (res := solve("111221")) == "312211", f'Actual: {res}'
    assert (res := solve("1", 5)) == "312211", f'Actual: {res}'

    print(f'Part 1 {len(solve(input, 40))}')  # 329356
    print(f'Part 2 {len(solve(input, 50))}')  # 4666278


if __name__ == '__main__':
    main()
