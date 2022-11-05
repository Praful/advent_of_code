import os
import sys
sys.path.append(os.path.relpath("../../shared/python"))
import utils


# Puzzle description: https://adventofcode.com/2018/day/14

# Part2 is not the fastest solution but it was easy to add to the part1 solution. It
# takes about 20s on i7-6700K CPU.


def solve(recipe, input, extract_count, part1=True):
    elf1 = 0
    elf2 = 1
    first = int(input)
    max_recipes = first + extract_count
    target = input
    target_len = len(target)

    while True:
        r1 = int(recipe[elf1])
        r2 = int(recipe[elf2])
        recipe += str(r1 + r2)
        recipe_len = len(recipe)
        elf1 = (elf1 + (1 + r1)) % recipe_len
        elf2 = (elf2 + (1 + r2)) % recipe_len

        if part1:
            if recipe_len > max_recipes:
                return recipe[first: first + extract_count]
        elif recipe[recipe_len - target_len:recipe_len] == target:
            return recipe_len - target_len


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
