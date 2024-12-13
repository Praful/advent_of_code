import sys
import os
import re

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2022/day/13


def read_input(input_file):
    def config(line):
        a = list(map(int, re.findall(r'(\d+)', line)))
        return (a[0], a[1]), (a[2], a[3]), (a[4], a[5])

    with open(input_file, "r") as file:
        input = list(map(config, file.read().split('\n\n')))

    return input


A_COST = 3
B_COST = 1
PRIZE_INCREMENT = 10000000000000


# We're solving two equations for A and B: Axa + Bxb = Px and Aya + Byb = Py
# where xa is the x value of button A, xb is the x value of button B, and so on
# see day13.jpg for derivation
def button_press_cost(A, B, P):
    a_presses = (B[0]*P[1] - B[1]*P[0])/(B[0]*A[1] - B[1]*A[0])
    b_presses = (A[0]*P[1] - A[1]*P[0])/(A[0]*B[1] - A[1]*B[0])

    if a_presses//1 == a_presses and b_presses//1 == b_presses:
        return A_COST * int(a_presses) + B_COST * int(b_presses)
    else:
        return 0


def solve(input, increment=0):
    return sum(button_press_cost(a, b, (p[0]+increment, p[1]+increment)) for a, b, p in input)


def main():
    input = read_input("../data/day13.txt")
    test_input = read_input("../data/day13-test.txt")

    assert (res := solve(test_input)) == 480, f'Actual: {res}' # part 1 
    print(f'Part 1 {solve(input)}')  # 36954
    print(f'Part 2 {solve(input, PRIZE_INCREMENT)}') # 79352015273424


if __name__ == '__main__':
    main()
