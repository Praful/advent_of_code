import sys
import os

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402
from visualisations import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2022/day/17

EMPTY = '.'
ROCK = '#'
CHAMBER_WIDTH = 7

shape0 = [
    "####",
]

shape1 = [
    ".#.",
    "###",
    ".#.",
]

shape2 = [
    "..#",
    "..#",
    "###",
]

shape3 = [
    "#",
    "#",
    "#",
    "#",
]

shape4 = [
    "##",
    "##",
]

# Create an array to store all shapes
ROCKS = [shape0, shape1, shape2, shape3, shape4]


def read_input(input_file):
    return read_file_str(input_file, True)[0]

DEBUG = False

def debug(*args):
    if DEBUG:
        print(*args, file=sys.stderr)


def can_move(chamber, rock, row, col):
    """
    Check if a piece can be placed at the specified row and column on the board.
    """
    rock_rows = len(rock)
    rock_cols = len(rock[0])

    for r in range(rock_rows):
        for c in range(rock_cols):
            if rock[r][c] == ROCK:
                chamber_row = row + r
                chamber_col = col + c

                if (chamber_row < 0 or chamber_row >= len(chamber) or
                        chamber_col < 0 or chamber_col >= len(chamber[0]) or
                        chamber[chamber_row][chamber_col] == ROCK):
                    return False  # Collision detected
    return True  # No collision detected

def update_chamber(rock, row, col, chamber):
    for r in range(len(rock)):
        for c in range(len(rock[0])):
            if rock[r][c] == ROCK:
                chamber[row + r][col + c] = ROCK


# Returns a tuple of the heights of each column. The distance is calculated
# from the highest placed rock and provides a profile of the placed rocks.
# Used to detect cycles.
def profile(chamber, height):
    result = []
    for c in range(len(chamber[0])):
        col_height = None
        for r in range(height, len(chamber)):
            if chamber[r][c] == ROCK:
                col_height = height - r
                break
        result.append(col_height)

    return tuple(result)

def solve(input, chamber_height=4000, target_rocks=2022):
    START_COL = 2
    START_ROW_FROM_PREVIOUS = 3
    chamber = make_grid(chamber_height, CHAMBER_WIDTH, EMPTY)
    tower_height = last_good_row = chamber_height
    rock_index = next_jet_index = row = added_height = 0
    cycle_found = False

    state_history = {}

    while rock_index < target_rocks:
        rock_id = rock_index % len(ROCKS)
        rock = ROCKS[rock_id]
        col = START_COL
        last_good_col = START_COL
        move_down = False
        tower_height = min(tower_height, last_good_row)
        row = tower_height - START_ROW_FROM_PREVIOUS - len(rock)
        height = chamber_height - row + 1

        if not cycle_found:
            state = (rock_id, next_jet_index % len(input), profile(chamber, row))
            if state in state_history:
                cycle_found = True
                prev_rock_index, prev_height = state_history[state]
                cycle_length = rock_index - prev_rock_index
                cycle_height = height - prev_height
                remaining_rocks = target_rocks - rock_index
                num_cycles_to_skip = remaining_rocks // cycle_length

                # jump ahead, skipping the cycles
                rock_index += cycle_length * num_cycles_to_skip

                assert rock_id == rock_index % len(ROCKS), "rock_id shouldn't change after skipping"

                added_height = cycle_height * num_cycles_to_skip
            else:
                state_history[state] = (rock_index, height)
        

        while True:
            if move_down:
                row += 1
                move_down = False
            else:
                move_down = True
                jet = input[next_jet_index % len(input)]
                next_jet_index += 1
                col = col + (1 if jet == '>' else -1)

            if can_move(chamber, rock, row, col):
                last_good_row = row
                last_good_col = col
                continue
            else:
                # if we couldn't move down, place rock and continue with next rock
                if not move_down:
                    update_chamber(rock, last_good_row, last_good_col, chamber)
                    break
                else:
                    col = last_good_col


        rock_index += 1

    return added_height + chamber_height - row + 1



def part1(input):
    return solve(input)


def part2(input):
    return solve(input, 7000, 1000000000000)

def main():
    input = read_input("../data/day17.txt")
    test_input = read_input("../data/day17-test.txt")

    assert (res := part1(test_input)) == 3068, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 3209

    assert (res := part2(test_input)) == 1514285714288, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 1580758017509


if __name__ == '__main__':
    main()
