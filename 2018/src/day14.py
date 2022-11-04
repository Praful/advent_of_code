import os
import sys
sys.path.append(os.path.relpath("../../shared/python"))
import utils


# Puzzle description: https://adventofcode.com/2018/day/14

# Part2 is not the fastest solution but it was easy to add to the part1 solution. It
# takes about 30s on i7-6700K CPU.


def solve(recipe, input, extract_count, part1=True):
    elf1 = 0
    elf2 = 1
    first = int(input)
    max_recipes = first + extract_count
    sequence = input
    # while len(recipe) < total + 1:
    while True:
        r1 = recipe[elf1]
        r2 = recipe[elf2]
        recipe += str(int(r1) + int(r2))
        elf1 = (elf1 + (1 + int(r1))) % len(recipe)
        elf2 = (elf2 + (1 + int(r2))) % len(recipe)

        if part1:
            if len(recipe) > max_recipes:
                return recipe[first: first + extract_count]

        elif (index := recipe.rfind(sequence, len(recipe) - len(sequence) - 1)) > -1:
            return index


def main():
    input = "430971"
    recipes = "37"

    # assert solve(recipes, "9", 10) == "5158916779"
    # assert solve(recipes, "5", 10) == "0124515891"
    # assert solve(recipes, "18", 10) == "9251071085"
    # assert solve(recipes, "2018", 10) == "5941429882"
    print(f'Part 1 {solve(recipes, input, 10)}')  # 5715102879

    # assert solve(recipes, "51589", 0, False) == 9
    # assert solve(recipes, "01245", 0, False) == 5
    # assert solve(recipes, "92510", 0, False) == 18
    # assert solve(recipes, "59414", 0, False) == 2018
    print(f'Part 2 {solve(recipes, input, 0, False)}')  # 20225706


if __name__ == '__main__':
    main()
