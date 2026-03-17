import sys
import os
import re

sys.path.append(os.path.relpath("../../shared/python"))

# noqa stops autopep8 from reordering this import
from utils import *  # noqa: E402

# Puzzle description: https://adventofcode.com/2022/day/22
# This is not a general solution for part 2. It works only for my input.
# To make it work for another cube, init_navigation_cube() would need to be modified
# to reflect the cube layout of your input.

DEBUG = True
print_debug = print if DEBUG else lambda *a, **k: None

# tiles
WALL = '#'
OPEN = '.'
EMPTY = ' '

FACE_ORIGIN = "topleft"
FACE_WIDTH = 50
R=0
C=1

def parse_path(s):
    return [int(x) if x.isdigit() else x
            for x in re.findall(r'\d{1,2}|[LR]', s)]


def read_input(input_file):
    board, path_str = read_file_str_sections(input_file, False)
    return board, parse_path(path_str[0])


def password(pos, dir):
    dir_facing_map = {Direction.EAST: 0, Direction.SOUTH: 1, Direction.WEST: 2, Direction.NORTH: 3}
    r, c = pos

    return 1000 * (r + 1) + 4 * (c + 1) + dir_facing_map[dir]


def find_start(board):
    for r, row in enumerate(board):
        for c, v in enumerate(row):
            if v == OPEN:
                return (r, c)


def on_board(board, pos):
    r, c = pos
    return 0 <= r < len(board) and 0 <= c < len(board[r])

def next_pos(board, pos, dir):
    new_pos = add_pos(pos, DIRECTION_DELTAS[dir])

    if on_board(board, new_pos):
        if tile(board, new_pos) == OPEN:
            return new_pos
        elif tile(board, new_pos) == WALL:
            return None

    # wraparound required
    match dir:
        case Direction.EAST:
            new_pos = (pos[R], 0)
        case Direction.WEST:
            new_pos = (pos[R], len(board[0]) - 1)
        case Direction.SOUTH:
            new_pos = (0, pos[C])
        case Direction.NORTH:
            new_pos = (len(board) - 1, pos[C])

    while True: 
        if on_board(board, new_pos):
            next_tile = tile(board, new_pos)
            if next_tile == OPEN:
                return new_pos
            elif next_tile == WALL:
                return None
            #  else blank space: continue

        new_pos = add_pos(new_pos, DIRECTION_DELTAS[dir])


def part1(input):
    board, path = input

    pos, dir = (find_start(board), Direction.EAST)

    for p in path:
        if str(p) in 'LR':
            dir = rotate_direction(dir, p == 'L')
        else:
            for _ in range(p):
                new_pos = next_pos(board, pos, dir)
                if new_pos is None:
                    break
                pos = new_pos

    return password(pos, dir)


def init_face(n, e, s, w, pos):
    face = {}
    face[Direction.NORTH] = n
    face[Direction.EAST] = e
    face[Direction.SOUTH] = s
    face[Direction.WEST] = w
    face[FACE_ORIGIN] = pos #r, c
    return face

# for part 2 =============================================
def init_navigation_cube():
    navigation = {}

    # map is (each number represents the face number of cube):
    # .12
    # .3.
    # 45.
    # 6..

    # what happens when we move N, E, S, W: the face we land on, and the direction we're going on 
    # that face; the pos is the absolute top left (row, col) of the face
    
    navigation[1] = init_face((6, Direction.EAST), (2, Direction.EAST), (3, Direction.SOUTH),
                              (4, Direction.EAST), (0, 50))

    navigation[2] = init_face((6, Direction.NORTH), (5, Direction.WEST), (3, Direction.WEST),
                              (1, Direction.WEST), (0, 100))

    navigation[3] = init_face((1, Direction.NORTH), (2, Direction.NORTH), (5, Direction.SOUTH),
                              (4, Direction.SOUTH), (50, 50))

    navigation[4] = init_face((3, Direction.EAST), (5, Direction.EAST), (6, Direction.SOUTH),
                              (1, Direction.EAST), (100, 0))

    navigation[5] = init_face((3, Direction.NORTH), (2, Direction.WEST), (6, Direction.WEST),
                              (4, Direction.WEST), (100, 50))

    navigation[6] = init_face((4, Direction.NORTH), (5, Direction.NORTH), (2, Direction.SOUTH),
                              (1, Direction.SOUTH), (150, 0))

    return navigation

def wrap_around_cube(pos, dir, face_id, navigation):
    r,c = pos
    face_nav = navigation[face_id]
    face_origin = face_nav[FACE_ORIGIN]
    new_face, new_dir = face_nav[dir]

    new_face_origin = navigation[new_face][FACE_ORIGIN] 

    # x = relative position to face origin that cuts across the face
    match dir:
        case Direction.NORTH: 
            x = c - face_origin[C]
        case Direction.EAST:
            x = r - face_origin[R]
        case Direction.SOUTH:
            x = face_origin[C] + FACE_WIDTH - 1 - c
        case Direction.WEST:
            x = face_origin[R] + FACE_WIDTH - 1 - r
        case _:
            assert False, f'Bad starting direction {dir}'
    
    match new_dir:
        case Direction.NORTH:
            new_pos = (new_face_origin[R]+FACE_WIDTH-1, new_face_origin[C] + x)
        case Direction.EAST:
            new_pos = (new_face_origin[R] + x, new_face_origin[C])
        case Direction.SOUTH:
            new_pos = (new_face_origin[R], new_face_origin[C] + FACE_WIDTH - 1 - x)
        case Direction.WEST:
            new_pos = (new_face_origin[R]+ FACE_WIDTH - 1 - x, new_face_origin[C]+FACE_WIDTH-1)
        case _:
            assert False, f'Bad new direction {new_dir}'

    return new_pos, new_dir, new_face


# return true if we're on same face
# return false if we need to move to an adjacent face
def on_face(pos, face_id, navigation):
    face_nav = navigation[face_id]
    face_origin = face_nav[FACE_ORIGIN]

    r, c = pos
    r_range = range(face_origin[0], face_origin[0] + FACE_WIDTH)
    c_range = range(face_origin[1], face_origin[1] + FACE_WIDTH)

    return r in r_range and c in c_range

def next_pos_cube(board, pos, dir, face_id, navigation):
    new_pos = add_pos(pos, DIRECTION_DELTAS[dir])

    if not on_face(new_pos, face_id, navigation):
        new_pos, dir, face_id = wrap_around_cube(pos, dir, face_id, navigation)

    if tile(board, new_pos) == OPEN:
        return new_pos, dir, face_id
    elif tile(board, new_pos) == WALL:
        return None, None, None
    else:
        assert False, f'bad tile {tile(board, new_pos)}'


def part2(input):
    navigation = init_navigation_cube()
    board, path = input

    pos, dir = (find_start(board), Direction.EAST)
    face_id = 1

    for p in path:
        if str(p) in 'LR':
            dir = rotate_direction(dir, p == 'L')
        else:
            for _ in range(p):
                new_pos, new_dir, new_face_id = next_pos_cube(board, pos, dir, face_id, navigation)
                if new_pos is None:
                    break
                pos = new_pos
                dir = new_dir
                face_id = new_face_id

    return password(pos, dir)


def main():
    input = read_input("../data/day22.txt")
    test_input = read_input("../data/day22-test.txt")

    assert (res := part1(test_input)) == 6032, f'Actual: {res}'
    print(f'Part 1 {part1(input)}')  # 73346

    #  assert (res := part2(test_input)) == 5031, f'Actual: {res}'
    print(f'Part 2 {part2(input)}')  # 106392

if __name__ == '__main__':
    main()
