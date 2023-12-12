import os
import sys

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2023/day/10


#  See https://www.w3.org/TR/xml-entity-names/025.html
def to_ascii_line(c):
    if c == 'S':
        #  return 'S'
        return f"{COLOUR_BLACK}{COLOUR_GREEN_BACKGROUND}S{COLOUR_RESET}"
    if c == 'F':
        return u'\u250C'
    if c == 'J':
        return u'\u2518'
    if c == 'L':
        return u'\u2514'
    if c == '|':
        return u'\u2502'
    if c == '-':
        return u'\u2500'
    if c == '7':
        return u'\u2510'


def print_visualisation(field, loop, outside=None):
    GROUND = '.'
    for y in range(len(field)):
        for x in range(len(field[y])):
            if (x, y) in loop:
                print(to_ascii_line(field[y][x]), end='')
            else:
                if outside is not None and (x, y) not in outside:
                    print(f'{COLOUR_RED_BACKGROUND}{GROUND}{COLOUR_RESET}', end='')
                else:
                    print(GROUND, end='')
        print()


def read_input(input_file):
    input = read_file_str(input_file, True)

    start = (0, 0)
    for y, line in enumerate(input):
        if 'S' in line:
            start = (line.index('S'), y)
            break

    return input, start


def whats_s(field, x, y):
    # work out what the starting pipe S is

    # check which directions we can move
    north = field[y-1][x] in '|7F'
    east = field[y][x+1] in '-J7'
    south = field[y+1][x] in '|LJ'
    west = field[y][x-1] in '-LF'

    if north and west:
        return 'J'
    if north and east:
        return 'L'
    if south and west:
        return '7'
    if south and east:
        return 'F'
    if south and north:
        return '|'
    if west and east:
        return '-'

    raise Exception("Can't work out starting posiiton (S)!")


def next_pipe(field, previous, x, y):
    def append(x, y):
        if 0 <= x < len(field[0]) and 0 <= y < len(field):
            if (x, y) != previous:
                result.append((x, y))

    pipe = field[y][x]
    if pipe == 'S':
        pipe = whats_s(field, x, y)

    result = []
    match pipe:
        case 'F':
            if field[y][x+1] in '-7J':
                append(x+1, y)
            if field[y+1][x] in '|LJ':
                append(x, y+1)
        case '-':
            if field[y][x+1] in '-J7':
                append(x+1, y)
            if field[y][x-1] in '-FL':
                append(x-1, y)
        case '7':
            if field[y][x-1] in '-LF':
                append(x-1, y)
            if field[y+1][x] in '|LJ':
                append(x, y+1)
        case '|':
            if field[y+1][x] in '|LJ':
                append(x, y+1)
            if field[y-1][x] in '|F7':
                append(x, y-1)
        case 'J':
            if field[y-1][x] in '|7F':
                append(x, y-1)
            if field[y][x-1] in '-LF':
                append(x-1, y)
        case 'L':
            if field[y][x+1] in '-7J':
                append(x+1, y)
            if field[y-1][x] in '|7F':
                append(x, y-1)

    if previous and len(result) > 1:
        raise Exception('More than one next pipe!')

    return result[0] if result else None


def part1(input):
    loop = set()
    loop.clear()
    field = input[0]
    start = previous = input[1]

    # pick a direction
    current = next_pipe(field, None, *start)
    steps = 1

    loop.add(start)
    loop.add(current)

    while current:
        previous, current = current, next_pipe(field, previous, *current)
        if current:
            loop.add(current)
            steps += 1

    # to visualise pipes
    #  print_loop(field, loop)

    return (steps+1)//2, loop


def part2(input):
    # Using even/odd rule  https://en.wikipedia.org/wiki/Even%E2%80%93odd_rule

    def is_ground(x, y): return not (x, y) in loop

    field = input[0]
    _, loop = part1(input)
    outside = set()

    for y in range(len(field)):
        inside = False
        JL_pipe = False

        for x in range(len(field[y])):
            tile = field[y][x]

            if tile == 'S':
                tile = whats_s(field, x, y)

            if not is_ground(x, y):
                if tile == '|':
                    inside = not inside
                elif tile == 'L':
                    JL_pipe = True
                elif tile == 'F':
                    JL_pipe = False
                elif tile == 'J':
                    if not JL_pipe:
                        inside = not inside
                    JL_pipe = False
                elif tile == '7':
                    if JL_pipe:
                        inside = not inside
                    JL_pipe = False

            if not inside:
                outside.add((x, y))

    # to visualise pipes
    #  print_loop(field, loop, outside | loop)

    return (len(field) * len(field[0])) - len(outside | loop)


def main():
    input = read_input("../data/day10.txt")

    test_input1 = read_input("../data/day10-test-1.txt")
    test_input1a = read_input("../data/day10-test-1a.txt")
    test_input2 = read_input("../data/day10-test-2.txt")
    test_input2a = read_input("../data/day10-test-2a.txt")
    test_input3 = read_input("../data/day10-test-3.txt")
    test_input4 = read_input("../data/day10-test-4.txt")
    test_input5 = read_input("../data/day10-test-5.txt")

    assert (res := part1(test_input1)[0]) == 4, f'Actual: {res}'

    assert (res := part1(test_input1a)[0]) == 4, f'Actual: {res}'

    assert (res := part1(test_input2)[0]) == 8, f'Actual: {res}'
    assert (res := part1(test_input2a)[0]) == 8, f'Actual: {res}'

    print(f'Part 1 {part1(input)[0]}')  # 6842

    assert (res := part2(test_input3)) == 4, f'Actual: {res}'
    assert (res := part2(test_input4)) == 8, f'Actual: {res}'
    assert (res := part2(test_input5)) == 10, f'Actual: {res}'

    print(f'Part 2 {part2(input)}')  # 393


if __name__ == '__main__':
    main()
