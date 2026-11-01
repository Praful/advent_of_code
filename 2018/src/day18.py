import types

from utils import (
    aoc_input_file,
    neighbours,
    print_grid,
    read_file_str,
    tile,
)

# Puzzle description: https://adventofcode.com/2018/day/18

DEBUG = False
print_debug = print if DEBUG else lambda *a, **k: None

# required since constants not allowed in match statement
Acre = types.SimpleNamespace()
Acre.OPEN_GROUND = "."
Acre.TREES = "|"
Acre.LUMBERYARD = "#"


def read_input(input_file):
    input = read_file_str(aoc_input_file(__file__, input_file), True)
    return input


def solve(input, duration=10):
    minute = 0
    landscape = input
    seen = {}

    while minute < duration:
        print_debug("Minute", minute, "---------------")
        if DEBUG:
            print_grid(landscape)

        state = tuple(tuple(row) for row in landscape)

        if state in seen:
            cycle_start = seen[state]
            cycle_length = minute - cycle_start
            print_debug(cycle_length)
            minute += ((duration - minute) // cycle_length) * cycle_length
        else:
            seen[state] = minute

        minute += 1

        landscape = generate(landscape)

    trees = 0
    lumberyards = 0
    for row in landscape:
        for acre in row:
            match acre:
                case Acre.TREES:
                    trees += 1
                case Acre.LUMBERYARD:
                    lumberyards += 1

    return trees * lumberyards


def generate(landscape):
    is_tree = lambda g, p: tile(g, p) == Acre.TREES
    is_lumberyard = lambda g, p: tile(g, p) == Acre.LUMBERYARD

    def item_count(r, c, condition):
        return len(neighbours((r, c), landscape, True, condition, True))

    new_landscape = []
    for ir, row in enumerate(landscape):
        new_row = []
        for ic, acre in enumerate(row):
            match acre:
                case Acre.OPEN_GROUND:
                    if item_count(ir, ic, is_tree) > 2:
                        new_row.append(Acre.TREES)
                    else:
                        new_row.append(acre)

                case Acre.TREES:
                    if item_count(ir, ic, is_lumberyard) > 2:
                        new_row.append(Acre.LUMBERYARD)
                    else:
                        new_row.append(acre)

                case Acre.LUMBERYARD:
                    if (
                        item_count(ir, ic, is_lumberyard) > 0
                        and item_count(ir, ic, is_tree) > 0
                    ):
                        new_row.append(acre)
                    else:
                        new_row.append(Acre.OPEN_GROUND)
                case _:
                    raise RuntimeError(f"Unknown char {acre} at ({ir}, {ic})")

        new_landscape.append("".join(new_row))

    return new_landscape


def main():
    input = read_input("day18.txt")
    test_input = read_input("day18-test.txt")

    assert (res := solve(test_input)) == 1147, f"Actual: {res}"
    print(f"Part 1 {solve(input)}")  # 543312

    print(f"Part 2 {solve(input, duration=1_000_000_000)}")  # 199064


if __name__ == "__main__":
    main()
