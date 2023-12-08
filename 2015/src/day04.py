import os
import sys
import hashlib

sys.path.append(os.path.relpath("../../shared/python"))
# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2015/day/4


def md5(x): return hashlib.md5(x.encode('utf-8')).hexdigest()


def solve(input, starts_with="00000"):
    num_zeroes = len(starts_with)
    for i in range(90000000):
        if md5(input + str(i))[:num_zeroes] == starts_with:
            return i

    return 0


def main():

    assert (res := solve("abcdef")) == 609043, f'Actual: {res}'
    assert (res := solve("pqrstuv")) == 1048970, f'Actual: {res}'

    print(f'Part 1 {solve("iwrupvqb")}')  # 346386
    print(f'Part 1 {solve("iwrupvqb", "000000")}')  # 9958218


if __name__ == '__main__':
    main()
