from pstats import Stats, SortKey
from cProfile import Profile
import sys
import os

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2022/day/6

FREE = '.'
OBJECT = '#'


def read_input(input_file):
    input = read_file_str(input_file, True)
    direction = ""
    position = None
    for r, row in enumerate(input):
        for c, _ in enumerate(row):
            if row[c] in ARROWS_TO_DIRECTION.keys():
                direction = row[c]
                position = (r, c)
                input[r] = replace(input[r], c, FREE)
                break
        if position is not None:
            break

    return input, DIRECTION_DELTAS[ARROWS_TO_DIRECTION[direction]], position


def is_free(pos, lab):
    return lab[pos[0]][pos[1]] == FREE


def is_object(pos, lab):
    return lab[pos[0]][pos[1]] == OBJECT


def part1(input):
    lab, starting_direction, starting_position = input

    guard_position = starting_position
    guard_direction = starting_direction
    visited = set([starting_position])

    while True:
        next_position = next_neighbour2(guard_position, guard_direction)
        if not in_grid(next_position, lab):
            break
        elif is_free(next_position, lab):
            guard_position = next_position
            visited.add(guard_position)
        elif is_object(next_position, lab):
            guard_direction = ROTATE[guard_direction]
        else:
            assert False, f'Unexpected pos {next_position}'

    return len(visited), visited


# For part 2, put an object on the places visited in part1 instead of putting one on
# every square, which works but is slow
def part2(input, visited_part1):
    result = 0
    lab, starting_direction, starting_position = input

    for new_object_pos in visited_part1:
        if new_object_pos == starting_position or is_object(new_object_pos, lab):
            continue

        guard_position = starting_position
        guard_direction = starting_direction
        visited = set()

        while True:
            next_position = next_neighbour2(guard_position, guard_direction)
            if not in_grid(next_position, lab):
                break
            elif is_object(next_position, lab) or next_position == new_object_pos:
                cur_pos_dir = (guard_position, guard_direction)

                if cur_pos_dir in visited:  # loop detected
                    result += 1
                    break
                else:
                    visited.add(cur_pos_dir)
                    guard_direction = ROTATE[guard_direction]
            elif is_free(next_position, lab):
                guard_position = next_position
            else:
                assert False, f'Unexpected pos {next_position}'

    return result


def main():
    input = read_input("../data/day06.txt")
    test_input = read_input("../data/day06-test.txt")

    test_result, test_visited = part1(test_input)
    assert test_result == 41, f'Actual: {test_result}'
    result, visited = part1(input)
    print(f'Part 1 {result}')  # 5409

    assert (res := part2(test_input, test_visited)) == 6, f'Actual: {res}'
    print(f'Part 2 {part2(input, visited)}')  # 2022


if __name__ == '__main__':
    main()
