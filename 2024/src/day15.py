import sys
import os
import copy

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2024/day/15

WALL = '#'
FREE = '.'
BOX = 'O'
BOX2 = '[]'
ROBOT = '@'

DEBUG = False
print_debug = print if DEBUG else lambda *a, **k: None


def read_input(input_file):
    with open(input_file, "r") as file:
        input = file.read().split('\n\n')

    grid = input[0].split('\n')
    directions = [ARROWS_TO_DIRECTION2[arrow]
                  for arrow in input[1].replace('\n', '')]

    pos = find_in_grid(grid, ROBOT)
    assert len(pos) == 1, f'Found multiple start positions: {pos}'

    return (grid, pos[0], directions)


def part2_grid(grid):
    result = []
    for r in range(len(grid)):
        row = ''
        for c in range(len(grid[0])):
            v = grid[r][c]
            if v == BOX:
                row += BOX2
            elif v == WALL:
                row += 2*WALL
            elif v == FREE:
                row += 2*FREE
            elif v == ROBOT:
                row += ROBOT + FREE
            else:
                raise ValueError(v)

        result.append(row)

    return result, find_in_grid(result, ROBOT)


def checksum(grid):
    result = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] in [BOX, BOX2[0]]:
                result += (r*100) + c

    return result


def update_grid_row(grid, pos, value):
    grid[pos[0]] = replace(grid[pos[0]], pos[1], value)


def update_grid(grid, from_pos, to_pos, value):
    update_grid_row(grid, from_pos, FREE)
    update_grid_row(grid, to_pos, value)


# part 1
def move(grid, from_pos, dir, obj):
    to_pos = add_pos(from_pos, dir)
    if tile(grid, to_pos) == WALL:
        return from_pos

    if tile(grid, to_pos) == BOX:
        move(grid, to_pos, dir, BOX)

    if tile(grid, to_pos) == FREE:
        update_grid(grid, from_pos, to_pos, obj)
        return to_pos

    return from_pos


# part 2 is conceptually the same as part 1: quit if wall, recurse until we 
# find object(s) that can move, move object(s).
# The new type of box [] causes the complexity.
def move2(grid, from_pos, dir, obj):
    to_pos = [add_pos(p, dir) for p in from_pos]

    # hit wall
    if any(tile(grid, p) == WALL for p in to_pos):  
        return from_pos

    # for boxes or robot can't move 
    if obj in BOX2 or not all(tile(grid, p) == FREE for p in to_pos):
        if dir in [NORTH, SOUTH]:
            to_pos = [p for p in to_pos if tile(grid, p) != FREE]
            to_pos.sort(key=lambda p: p[1])
            left, right = to_pos[0], to_pos[-1]

            # check if we have solitary [ or ]
            if tile(grid, left) == BOX2[1]:
                to_pos.insert(0, (left[0], left[1]-1))
            if tile(grid, right) == BOX2[0]:
                to_pos.append((right[0], right[1]+1))

            # recurse only if there's still no space to move
            if not all(tile(grid, add_pos(p, dir)) == FREE for p in from_pos if tile(grid, p) != FREE):
                move2(grid, to_pos, dir, obj)

    # E/W processing is as part 1
    if dir in [EAST, WEST]:  
        assert len(
            to_pos) == 1, f'Expecing one pos, found multiple pos: {to_pos}'
        if tile(grid, to_pos[0]) in BOX2:
            move2(grid, to_pos, dir, tile(grid, to_pos[0]))

    # we have space to move
    if all(tile(grid, p) == FREE for p in to_pos if tile(grid, p) != FREE):
        if dir in [EAST, WEST]:  
            assert len(to_pos) == 1, f'Expecing one pos, found multiple pos: {to_pos}'
            update_grid(grid, from_pos[0], to_pos[0], obj)
            return to_pos
        elif dir in [NORTH, SOUTH]:
            for p in from_pos:
                if tile(grid, p) != FREE:
                    update_grid_row(grid, add_pos(p, dir), tile(grid, p))
                    update_grid_row(grid, p, FREE)

            if obj == ROBOT:
                return [add_pos(from_pos[0], dir)]
            else:
                return to_pos

    return from_pos


def solve(input, move_fn=move):
    grid, pos, directions = input
    grid = copy.deepcopy(grid)

    for dir in directions:
        pos = move_fn(grid, pos, dir, ROBOT)

    return checksum(grid)


def main():
    input = read_input("../data/day15.txt")
    test_input = read_input("../data/day15-test.txt")
    test_input2 = read_input("../data/day15-test2.txt")
    test_input3 = read_input("../data/day15-test3.txt")

    assert (res := solve(test_input)) == 2028, f'Actual: {res}'
    assert (res := solve(test_input2)) == 10092, f'Actual: {res}'
    print(f'Part 1 {solve(input)}')  # 1446158

    assert (res := solve(part2_grid(
        test_input3[0]) + test_input3[2:], move2)) == 618, f'Actual: {res}'
    assert (res := solve(part2_grid(
        test_input2[0]) + test_input2[2:], move2)) == 9021, f'Actual: {res}'
    print(f'Part 2 {solve(part2_grid(input[0]) + input[2:], move2)}') # 1446175


if __name__ == '__main__':
    main()
