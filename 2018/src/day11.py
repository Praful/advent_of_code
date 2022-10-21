import os
import sys
from tkinter import Y

sys.path.append(os.path.relpath("../../shared/python"))
import utils
import numpy as np
from functools import cache

# Puzzle description: https://adventofcode.com/2018/day/11

# My brute force part1 solution was too slow for part2. So I used a
# recursive method, caching values. This ran in constant time and
# took about 4mins on my PC. Not great but it found the solution.

# On reading the reddit forum, I saw that some people used the
# summed area table algorithm, which I implemented too. That runs in 8s.
# For the calculation for summed area, for some reason I'm off by 1 ie
# to calculate a square area for x,y, I have to use x-1, y-1.
# The init_summed_area() method must be off by one in its initialising
# but it's a straight implementation of the Wikipedia article!
# Having looked at other solutions, I see that they're doing
# similar adjustments before printing out x,y. 🤔


class PowerGrid:
    def __init__(self, dim, serial_number) -> None:
        self.dim, self.serial_number = dim, serial_number
        self.grid = self.init_grid()
        self.summed_area = self.init_summed_area()

    def init_grid(self):
        grid = np.zeros([self.dim, self.dim], dtype=int)
        for x in range(1, self.dim):
            for y in range(1, self.dim):
                grid[x, y] = self.power(x, y)

        return grid

    def power(self, x, y):
        rack_id = x + 10
        result = rack_id * y
        result += self.serial_number
        result *= rack_id

        # Return hundred digit eg 12345 return 3, 98765 returns 7.
        # For numbers less than 100, return 0.
        # See https://stackoverflow.com/questions/32752750/how-to-find-the-numbers-in-the-thousands-hundreds-tens-and-ones-place-in-pyth
        #   thousands = num // 1000
        #   hundreds = (num % 1000) // 100
        #   tens = (num % 100) // 10
        #   units = (num % 10)
        return (((result % 1000) // 100) - 5)

    def init_summed_area(self):
        summed_area = np.zeros([self.dim, self.dim], dtype=int)

        for x in range(1, self.dim):
            for y in range(1, self.dim):
                summed_area[x, y] = self.grid[x, y] + \
                    summed_area[x, y - 1] + summed_area[x - 1, y] - \
                    summed_area[x - 1, y - 1]

        return summed_area

    # for testing summed area algorithm
    def test(self, x, y, square):
        self.print_grid(self.grid, x, y, square)
        self.print_grid(self.summed_area, x, y, square)
        print('total:       ', self.calc_square_value3(x - 1, y - 1, square))
        print('total (exp): ', self.calc_square_value1(x, y, square))

    def print_grid(self, arr, x, y, square):
        for i in range(x, x + square):
            print()
            for j in range(y, y + square):
                print(arr[i, j], ' ', end='')
        print()

    # https://en.wikipedia.org/wiki/Summed-area_table#The_algorithm
    def calc_square_value3(self, x, y, s):
        return self.summed_area[x + s, y + s] + \
            self.summed_area[x, y] - \
            self.summed_area[x + s, y] - \
            self.summed_area[x, y + s]

    # for part2, made use of the fact that the sum of values in
    # a square, say 4x4 is, 3x3 plus the right side and bottom row.
    # Similarly for 3x3: 2x2 plus its right and bottom row
    # In this 4x4 square:
    #   ABCD
    #   EFGH
    #   IJKL
    #   MNOP
    # the total is the sum of the 3x3 square values (ABCEFGIJK)
    # plus DHLP plus MNO.
    @cache
    def calc_square_value2(self, x, y, square):
        if square == 1:
            return self.grid[x, y]

        result = 0

        for j in range(y, y + square):
            result += self.grid[x + square - 1, j]

        for i in range(x, x + square - 1):
            result += self.grid[i, y + square - 1]

        result += self.calc_square_value2(x, y, square - 1)

        return result

    # used in part1 but is too slow for part2
    def calc_square_value1(self, x, y, square=3):
        result = 0

        for i in range(x, x + square):
            for j in range(y, y + square):
                result += self.grid[i, j]

        return result


def part1(serial_number):
    dim = 301
    # dim = 5
    square = 3  # 3x3
    power_grid = PowerGrid(dim, serial_number)

    max = -np.inf
    result = None
    # power_grid.test(5, 6, 3)

    for x in range(1, dim - square):
        for y in range(1, dim - square):
            total = power_grid.calc_square_value1(x, y, square)
            # total = power_grid.calc_square_value2(x, y, square)
            # total = power_grid.calc_square_value3(x - 1, y - 1, square)
            if total > max:
                result = (x, y)
                max = total

    return result


def part2(serial_number):
    dim = 301
    max = -np.inf
    result = None

    power_grid = PowerGrid(dim, serial_number)

    for square in range(1, dim):
        for x in range(1, dim - square):
            for y in range(1, dim - square):
                # total = power_grid.calc_square_value2(x, y, square)
                total = power_grid.calc_square_value3(x - 1, y - 1, square)
                if total > max:
                    result = (x, y, square)
                    max = total
    return result


def main():

    # assert PowerGrid(1,8).power(3, 5) == 4
    # assert PowerGrid(1,57).power(122, 79) == -5
    # assert PowerGrid(1,39).power(217,196) == 0
    # assert PowerGrid(1,71).power(101,153) == 4

    # print(f'Part 1 (test) {part1(18)}')  # 33,45
    # print(f'Part 1 (test) {part1(42)}')  # 21,61
    print(f'Part 1 {part1(2866)}')  # 20,50

    # print(f'Part 2 (test) {part2(18)}')  # 90,269,16
    # print(f'Part 2 (test) {part2(42)}')  # 232,251,12
    print(f'Part 2 {part2(2866)}')  # 238,278,9


if __name__ == '__main__':
    main()
